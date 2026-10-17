"""Test the packaged website at the same path shape as a GitHub Pages project."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from pathlib import Path

root=Path(__file__).resolve().parents[1]/'_site'
ThreadingHTTPServer.request_queue_size=128
if not (root/'index.html').exists():raise SystemExit('Run npm run build:site before npm test.')
class Handler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        if not self.path.startswith('/Code-Editor-Pro/'):
            self.send_error(404);return
        self.path=self.path[len('/Code-Editor-Pro'):]
        super().do_GET()
ThreadingHTTPServer(('127.0.0.1',4174),partial(Handler,directory=str(root))).serve_forever()
