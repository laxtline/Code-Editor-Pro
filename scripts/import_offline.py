"""Build a deterministic, dependency-free offline pack from local study repositories.

Usage: python scripts/import_offline.py --source-root C:/path/to/Downloads --download-images
Existing packs remain usable without the original source folders or Python.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from html import unescape
import json
from pathlib import Path
import re
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("premium", "Leetcode-Premium-main", "LeetCode Premium"),
    ("complete", "Complete-LeetCode-Premium-Problems-master", "Complete Premium Problems"),
    ("primer", "leetcode-primer-main", "LeetCode Primer"),
    ("solutions", "LeetCode-Solutions-main", "LeetCode Solutions"),
]
EXTENSIONS = {".py": "python", ".js": "javascript", ".cpp": "cpp", ".c": "c",
              ".java": "java", ".sql": "sql", ".rs": "rust"}


def read(path):
    return path.read_text(encoding="utf-8-sig", errors="replace")


def normalized(title):
    return re.sub(r"[^a-z0-9]", "", title.lower())


def title_case(name):
    return re.sub(r"\s+", " ", re.sub(r"(?<=[a-z])(?=[A-Z])", " ", re.sub(r"[-_]+", " ", name))).strip()


def write_js(path, prefix, data):
    path.write_text(prefix + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")


def build(source_root, download_images=False):
    output = ROOT / "offline"
    output.mkdir(exist_ok=True)
    records, aliases, sources, skipped = {}, {}, [], []

    # Establish IDs from structured folders before matching loose solution files.
    for source, folder, label in SOURCES:
        base = source_root / folder
        if not base.is_dir():
            raise SystemExit(f"Missing source folder: {base}")
        for p in sorted(base.iterdir()):
            match = re.match(r"^(\d+)[- .](.+)", p.name) if p.is_dir() else None
            if not match:
                continue
            number, title = int(match[1]), title_case(match[2])
            doc = p / "README.md"
            if doc.exists():
                heading = re.search(r"<h2>.*?<a[^>]*>(\d+)\.\s*(.*?)</a>", read(doc), re.S)
                if heading:
                    title = unescape(re.sub("<[^>]+>", "", heading[2]))
            aliases[normalized(title)] = f"lc-{number}"
            records.setdefault(f"lc-{number}", dict(key=f"lc-{number}", number=number,
                title=title, difficulty="Unknown", tags=[], documents=[], solutions=[], sources=[]))

    def record_for(number, title):
        key = f"lc-{number}" if number else aliases.get(normalized(title), "topic-" + normalized(title))
        if key not in records:
            records[key] = dict(key=key, number=number, title=title, difficulty="Unknown",
                                tags=[], documents=[], solutions=[], sources=[])
        aliases[normalized(title)] = key
        return records[key]

    image_urls = set()
    def expand_snippets(text, base):
        def expand(match):
            target = (base / match[1]).resolve()
            if target.is_relative_to(base.resolve()) and target.is_file():
                return read(target).rstrip()
            return "[Source snippet not available in this download]"
        return re.sub(r'--8<--\s*"([^"]+)"', expand, text)

    def normalize_mkdocs(text):
        lines, in_callout = [], False
        for line in text.splitlines():
            callout = re.match(r'^(?:\?\?\?|!!!)\+?\s*(.*)$', line)
            if callout:
                quoted = re.search(r'"([^"]+)"', callout[1])
                lines.append('### ' + (quoted[1] if quoted else callout[1]))
                in_callout = True
            elif in_callout and line.startswith('    '):
                lines.append(line[4:])
            else:
                lines.append(line)
                if line.strip():
                    in_callout = False
        return '\n'.join(lines)

    for source, folder, label in SOURCES:
        base = source_root / folder
        source_files = 0
        license_paths = []
        for filename in ("LICENSE", "LICENSE.md", "LICENSE.txt"):
            path = base / filename
            if path.is_file():
                target = output / "licenses" / source / filename
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(read(path), encoding="utf-8")
                license_paths.append(target.relative_to(ROOT).as_posix())
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(base)
            if any(part.startswith(".") or part in ("site", "node_modules", "dist") for part in rel.parts):
                continue
            suffix = path.suffix.lower()
            is_code = suffix in EXTENSIONS
            is_doc = suffix == ".md"
            if not (is_code or is_doc) or len(rel.parts) == 1 and is_doc:
                continue
            if source == "primer" and rel.parts[0] not in ("docs", "solutions"):
                continue
            # Notes without content add no reading value.
            text = read(path).replace('\u200b', '').strip()
            if not text or text == "<!---LeetCode Topics Start-->\n<!---LeetCode Topics End-->":
                continue
            match = re.match(r"^(\d+)[- .](.+)", rel.parts[0])
            if source == "primer":
                match = re.match(r"^(\d+)[- .](.+)", path.stem if is_doc else rel.parts[1])
            if match:
                number, title = int(match[1]), title_case(match[2])
            else:
                if is_doc and path.name.lower() in ("readme.md", "notes.md", "index.md"):
                    continue
                number, title = None, title_case(path.stem)
            if not title or source == "primer" and not match and is_code:
                continue
            record = record_for(number, title)
            if source not in record["sources"]:
                record["sources"].append(source)
            source_files += 1
            if is_code:
                digest = sha256((EXTENSIONS[suffix] + "\n" + text).encode()).hexdigest()
                existing = next((s for s in record["solutions"] if s["hash"] == digest), None)
                provenance = dict(source=source, path=rel.as_posix())
                if existing:
                    existing["origins"].append(provenance)
                else:
                    record["solutions"].append(dict(language=EXTENSIONS[suffix], name=path.name,
                        code=text, hash=digest, origins=[provenance]))
            else:
                text = expand_snippets(normalize_mkdocs(text) if source == 'primer' else text, base)
                # MkDocs metadata is searchable through normal tags instead of front matter.
                front = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
                if front:
                    tags = re.findall(r"^\s*-\s*(.+)$", front[1], re.M)
                    for tag in tags:
                        if tag in ("Easy", "Medium", "Hard"):
                            record["difficulty"] = tag
                        elif tag not in record["tags"]:
                            record["tags"].append(tag)
                    text = text[front.end():]
                difficulty = re.search(r"<h3>(Easy|Medium|Hard)</h3>", text)
                if difficulty:
                    record["difficulty"] = difficulty[1]
                image_urls.update(re.findall(r'<img[^>]+src=["\'](https?://[^"\']+)', text))
                if not any(d["text"] == text for d in record["documents"]):
                    record["documents"].append(dict(source=source, path=rel.as_posix(), text=text))
        sources.append(dict(id=source, label=label, folder=folder, importedFiles=source_files,
                            licenses=license_paths))

    # These are extension programs, not offline problem databases.
    for folder in ("Leetcode-Premium-Unlocker-master", "Leetcode-Premium-Bypass-main"):
        skipped.append(dict(folder=folder, reason="Browser extension depending on online services; no standalone problem dataset."))

    images = {}
    image_dir = output / "images"
    image_dir.mkdir(exist_ok=True)
    def get_image(url):
        parsed = urlparse(url)
        if parsed.hostname != "assets.leetcode.com" or parsed.scheme != "https":
            return url, None
        suffix = Path(parsed.path).suffix.lower()
        if suffix not in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
            return url, None
        target = image_dir / (sha256(url.encode()).hexdigest()[:20] + suffix)
        if not target.exists() and download_images:
            try:
                with urlopen(Request(url, headers={"User-Agent": "CodeLab-Offline-Importer/1.0"}), timeout=20) as response:
                    if not response.headers.get("Content-Type", "").startswith("image/"):
                        return url, None
                    body = response.read(10_000_001)
                    if len(body) > 10_000_000:
                        return url, None
                    target.write_bytes(body)
            except Exception:
                return url, None
        return url, target.relative_to(ROOT).as_posix() if target.exists() else None

    with ThreadPoolExecutor(max_workers=10) as pool:
        for url, local in pool.map(get_image, sorted(image_urls)):
            if local:
                images[url] = local
    references = ROOT / 'data/github-references.json'
    if references.exists():
        reference_data = json.loads(read(references))
        for item in reference_data['entries']:
            key = 'algorithm-' + Path(item['path']).stem.replace('_', '-')
            records[key] = dict(key=key, number=None, title=title_case(Path(item['path']).stem),
                difficulty='Unknown', tags=['Algorithm Reference'], documents=[], sources=['algorithms'],
                solutions=[dict(language='python', name=Path(item['path']).name, code=item['code'],
                    hash=sha256(('python\n'+item['code']).encode()).hexdigest(),
                    origins=[dict(source='algorithms',path=item['path'],url=item['url'],commit=reference_data['commit'])])])
        sources.append(dict(id='algorithms',label='TheAlgorithms / Python (MIT)',folder=reference_data['repository'],
            importedFiles=len(reference_data['entries']),licenses=['offline/licenses/algorithms/LICENSE.md'],
            commit=reference_data['commit']))
    entries = sorted((r for r in records.values() if r["documents"] or r["solutions"]),
                     key=lambda r: (r["number"] is None, r["number"] or 0, r["title"].lower()))
    for record in entries:
        record["documents"].sort(key=lambda d: (Path(d["path"]).name.lower() == "notes.md",))
        for doc in record["documents"]:
            for url in re.findall(r'<img[^>]+src=["\'](https?://[^"\']+)', doc["text"]):
                if url in images:
                    doc["text"] = doc["text"].replace(url, images[url])
    catalog, chunks = [], []
    for offset in range(0, len(entries), 80):
        name = f"offline/pack-{offset // 80:03}.js"
        payload = entries[offset:offset + 80]
        (ROOT / name).write_text("Object.assign(window.CODELAB_OFFLINE_PACKS," +
            json.dumps({r["key"]: r for r in payload}, ensure_ascii=False, separators=(",", ":")) + ");\n", encoding="utf-8")
        chunks.append(name)
        for record in payload:
            catalog.append({k: record[k] for k in ("key", "number", "title", "difficulty", "tags", "sources")} |
                           dict(chunk=name, languages=sorted({s["language"] for s in record["solutions"]}),
                                solutionCount=len(record["solutions"]), hasStatement=bool(record["documents"])))
    data = dict(version=1, entries=catalog, sources=sources, skipped=skipped,
                stats=dict(entries=len(entries), solutions=sum(len(r["solutions"]) for r in entries),
                           documents=sum(len(r["documents"]) for r in entries), images=len(images),
                           missingImages=len(image_urls - images.keys())),
                files=chunks + sorted(set(images.values())) + [p for s in sources for p in s["licenses"]])
    # A content fingerprint also invalidates installed service worker caches.
    from refresh_cache import revision_for
    data["revision"] = revision_for(data)
    write_js(output / "catalog.js", "window.CODELAB_OFFLINE_CATALOG=", data)
    (output / "import-report.json").write_text(json.dumps({k:v for k,v in data.items() if k != "entries"}, indent=2), encoding="utf-8")
    print(json.dumps(data["stats"], indent=2))
    print(f"Wrote {len(chunks)} lazy-loaded packs to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=Path.home() / "Downloads")
    parser.add_argument("--download-images", action="store_true")
    args = parser.parse_args()
    build(args.source_root, args.download_images)
