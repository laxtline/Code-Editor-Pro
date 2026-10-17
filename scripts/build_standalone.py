"""Bundle the app, library data and diagrams into a portable single HTML file."""
import base64
import json
import mimetypes
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

def script(text):
    return '<script>'+re.sub(r'</script',r'<\\/script',text,flags=re.I)+'</script>'

def build():
    html=(ROOT/'index.html').read_text(encoding='utf-8')
    html=re.sub(r'<link rel="manifest"[^>]*>', '', html)
    html=html.replace('href="assets/icon-192.png"','href="data:image/png;base64,'+base64.b64encode((ROOT/'assets/icon-192.png').read_bytes()).decode()+'"')
    catalog=json.loads((ROOT/'offline/catalog.js').read_text(encoding='utf-8').removeprefix('window.CODELAB_OFFLINE_CATALOG=').rstrip(';\n'))
    images={p:'data:'+mimetypes.guess_type(p)[0]+';base64,'+base64.b64encode((ROOT/p).read_bytes()).decode() for p in catalog['files'] if p.startswith('offline/images/')}
    preface='window.CODELAB_STANDALONE=true;window.CODELAB_PYTHON_WORKER_SOURCE='+json.dumps((ROOT/'assets/python-worker.js').read_text(encoding='utf-8'))+';window.CODELAB_INLINE_IMAGES='+json.dumps(images,separators=(',',':'))+';window.CODELAB_OFFLINE_PACKS={};\n'
    for p in catalog['files']:
        if p.endswith('.js'):
            preface+=(ROOT/p).read_text(encoding='utf-8')+'\n'
    license_files=[p for p in catalog['files'] if '/licenses/' in p]+['vendor/marked-LICENSE','vendor/dompurify-LICENSE']
    preface+='window.CODELAB_INLINE_LICENSES='+json.dumps({p:(ROOT/p).read_text(encoding='utf-8') for p in license_files},ensure_ascii=False)+';\n'
    def inline_script(match):
        path=match[1]
        if path.startswith(('https:','http:')):
            return match[0]
        text=(ROOT/path).read_text(encoding='utf-8')
        return (script(preface) if path=='assets/library.js' else '')+script(text)
    html=re.sub(r'<script src="([^"]+)"\s*></script>',inline_script,html)
    def inline_style(match):
        css=(ROOT/match[1]).read_text(encoding='utf-8')
        return '<style>'+css+'</style>'
    html=re.sub(r'<link rel="stylesheet" href="([^"\s]+)"\s*/>',inline_style,html)
    html=html.replace('<title>Study Lab —','<title>Study Lab Offline —')
    output=ROOT/'CodeLab-Offline.html';output.write_text(html,encoding='utf-8')
    print(f'Built {output.name}: {output.stat().st_size/1024/1024:.2f} MiB; {len(images)} embedded diagrams.')

if __name__=='__main__':
    build()
