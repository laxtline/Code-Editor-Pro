"""Local-only fixture: serve two real worker revisions without editing build artifacts."""
import json
import re
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1] / '_site'
revision = 'test-before'

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send_bytes(self, data, content_type='text/plain'):
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        global revision
        if self.path != '/__test__/revision':
            self.send_error(404)
            return
        value = json.loads(self.rfile.read(int(self.headers['Content-Length'])))['revision']
        if value not in ['test-before', 'test-after']:
            self.send_error(400)
            return
        revision = value
        self.send_bytes(b'ok')

    def do_GET(self):
        if not self.path.startswith('/update-test/'):
            self.send_error(404)
            return
        self.path = self.path[len('/update-test'):]
        name = urlsplit(self.path).path
        if name == '/legacy.html':
            self.send_bytes(b'<!doctype html><title>Legacy worker fixture</title><h1>Legacy worker fixture</h1>', 'text/html')
        elif name == '/legacy-worker.js':
            # Reproduce the old cache-first worker, including its cached root.
            self.send_bytes(b'''
const legacyCache='legacy-codelab-test';
self.addEventListener('install',event=>event.waitUntil((async()=>{
  const cache=await caches.open(legacyCache);
  for(const path of ['./','index.html'])await cache.put(new URL(path,self.registration.scope),new Response('<title>CodeLab</title><h1>CodeLab old cached copy</h1>',{headers:{'Content-Type':'text/html'}}));
})()));
self.addEventListener('activate',event=>event.waitUntil(self.clients.claim()));
self.addEventListener('fetch',event=>{
  const url=new URL(event.request.url);url.search='';url.hash='';
  if(['./','index.html'].some(path=>url.href===new URL(path,self.registration.scope).href))event.respondWith(caches.open(legacyCache).then(cache=>cache.match(url.href)));
});
''', 'application/javascript')
        elif name in ['/', '/index.html']:
            html=(ROOT/'index.html').read_text(encoding='utf-8')
            html=re.sub(r'(window\.CODELAB_OFFLINE_CATALOG=\{.*?"revision":")[^"]*(")',lambda match:match[1]+revision+match[2],html,count=1,flags=re.S)
            self.send_bytes(html.encode('utf-8'), 'text/html')
        elif name == '/offline/catalog.js':
            catalog = json.loads((ROOT/'offline/catalog.js').read_text(encoding='utf-8').removeprefix('window.CODELAB_OFFLINE_CATALOG=').rstrip(';\n'))
            catalog['revision'] = revision
            self.send_bytes(('window.CODELAB_OFFLINE_CATALOG='+json.dumps(catalog)+';').encode(), 'application/javascript')
        elif name == '/sw.js':
            self.send_bytes((ROOT/'sw.js').read_bytes()+('\n// '+revision).encode(), 'application/javascript')
        else:
            super().do_GET()

ThreadingHTTPServer.request_queue_size = 128
ThreadingHTTPServer(('127.0.0.1', 4176), partial(Handler, directory=str(ROOT))).serve_forever()
