"""Refresh the offline revision using committed packs; original Downloads folders are not needed."""
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def revision_for(catalog):
    clean = {k:v for k,v in catalog.items() if k != 'revision'}
    digest = sha256(json.dumps(clean,sort_keys=True).encode())
    runtime = json.loads((ROOT/'assets/runtime-manifest.js').read_text(encoding='utf-8').removeprefix('window.CODELAB_RUNTIME=').rstrip(';\n'))
    names = set(runtime['shell']+catalog['files']+['sw.js','assets/runtime-manifest.js'])-{'offline/catalog.js'}
    for name in sorted(names):
        digest.update(name.encode());digest.update((ROOT/name).read_bytes())
    return digest.hexdigest()[:16]

def refresh():
    path = ROOT/'offline/catalog.js'
    catalog = json.loads(path.read_text(encoding='utf-8').removeprefix('window.CODELAB_OFFLINE_CATALOG=').rstrip(';\n'))
    catalog['revision'] = revision_for(catalog)
    path.write_text('window.CODELAB_OFFLINE_CATALOG='+json.dumps(catalog,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    (ROOT/'offline/import-report.json').write_text(json.dumps({k:v for k,v in catalog.items() if k != 'entries'},indent=2),encoding='utf-8')
    print('Offline revision:',catalog['revision'])

if __name__ == '__main__': refresh()
