"""Copy pinned browser runtimes from npm into the deployable app. No CDN is used at runtime."""
from hashlib import sha256
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SHELL = ['index.html','manifest.webmanifest','assets/icon-192.png','assets/icon-512.png',
         'assets/library.css','assets/library.js','assets/academy.css','assets/academy.js',
         'assets/editor-tools.js','assets/assessment.js','assets/platform.js','assets/python-worker.js',
         'assets/runtime-manifest.js','assets/coding-data.js','assets/advanced-coding.js','assets/python-data.js','assets/practice-data.js',
         'assets/learning.css','assets/study-data.js','assets/study.js','assets/navigation.js','assets/persistence.js','assets/learning.js',
         'vendor/marked.umd.js','vendor/purify.min.js','offline/catalog.js']

def build():
    target = ROOT/'vendor/runtimes'
    target.mkdir(parents=True,exist_ok=True)
    versions = {}
    for name,expected in [('pyodide','0.26.2'),('sql.js','1.14.0'),('monaco-editor','0.45.0')]:
        source = ROOT/'node_modules'/name
        if not source.is_dir():
            raise SystemExit('Missing '+name+'. Run npm ci before bundling runtimes.')
        versions[name] = json.loads((source/'package.json').read_text())['version']
        if versions[name] != expected:
            raise SystemExit(f'Unexpected {name} version: {versions[name]} (expected {expected})')
    python = target/'python';python.mkdir(exist_ok=True)
    for name in ['pyodide.js','pyodide.asm.js','pyodide.asm.wasm','pyodide-lock.json','python_stdlib.zip']:
        shutil.copy2(ROOT/'node_modules/pyodide'/name,python/name)
    sql = target/'sql';sql.mkdir(exist_ok=True)
    for name in ['sql-wasm.js','sql-wasm.wasm']:
        shutil.copy2(ROOT/'node_modules/sql.js/dist'/name,sql/name)
    shutil.copy2(ROOT/'node_modules/sql.js/LICENSE',sql/'LICENSE')
    monaco = target/'monaco';monaco.mkdir(exist_ok=True)
    shutil.copytree(ROOT/'node_modules/monaco-editor/min/vs',monaco/'vs',dirs_exist_ok=True)
    shutil.copy2(ROOT/'node_modules/monaco-editor/LICENSE',monaco/'LICENSE')
    files = [dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=sha256(p.read_bytes()).hexdigest())
             for p in sorted(target.rglob('*')) if p.is_file()]
    data = dict(versions=versions,shell=SHELL,files=files,bytes=sum(p['bytes'] for p in files))
    (ROOT/'assets/runtime-manifest.js').write_text('window.CODELAB_RUNTIME='+json.dumps(data,separators=(',',':'))+';\n',encoding='utf-8')
    print(f'Bundled {len(files)} runtime files: {data["bytes"]/1048576:.2f} MiB (Python, SQL, Monaco).')

if __name__ == '__main__': build()
