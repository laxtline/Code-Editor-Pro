"""Real loopback API and process-boundary checks; never writes into the hosted build."""
import functools
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from local_tools import LocalTools,bounded_run,MAX_OUTPUT
spec=importlib.util.spec_from_file_location('launcher',ROOT/'Start-CodeLab.py')
launcher=importlib.util.module_from_spec(spec);spec.loader.exec_module(launcher)

class ToolsTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.tools=LocalTools(self.root)
    def tearDown(self):self.temp.cleanup()
    def test_process_input_errors_timeout_and_output_bound(self):
        self.assertEqual(bounded_run([sys.executable,'-c','print(int(input())*2)'],self.root,'21')['stdout'].strip(),'42')
        self.assertEqual(bounded_run([sys.executable,'-c','raise ValueError("bad")'],self.root)['status'],'runtime-error')
        self.assertEqual(bounded_run([sys.executable,'-c','while True: pass'],self.root,timeout=.2)['status'],'timeout')
        result=bounded_run([sys.executable,'-c','print("x"*300000)'],self.root)
        self.assertEqual(result['status'],'output-limit')
        self.assertLessEqual(len(result['stdout'].encode())+len(result['stderr'].encode()),MAX_OUTPUT)
    def test_folder_merge_tombstones_and_credentials(self):
        def merge(value,stamp=1,key='cl_study_notes_html-start'):
            return self.tools.merge_records({'format':1,'records':{key:{'value':value,'updatedAt':stamp,'device':'test'}}})
        merge('first',2);merge('stale',1)
        self.assertEqual(self.tools.read_records()['records']['cl_study_notes_html-start']['value'],'first')
        merge(None,3);self.assertIsNone(self.tools.read_records()['records']['cl_study_notes_html-start']['value'])
        merge(json.dumps({'theme':'dark','jdoodleId':'PRIVATE','jdoodleSecret':'PRIVATE'}),4,'cl_settings')
        self.assertNotIn('PRIVATE',self.tools.path.read_text())
        for key in ['token','../x','cl_sync_device']:
            with self.assertRaises(ValueError):merge('value',5,key)
        for stamp in [float('inf'),float('nan'),True,-1]:
            with self.assertRaises(ValueError):merge('value',stamp)
    def test_available_compilers_execute_and_report_compile_errors(self):
        programs={
            'c':'#include <stdio.h>\nint main(void){int n;scanf("%d",&n);printf("%d",n*2);return 0;}',
            'cpp':'#include <iostream>\nint main(){int n;std::cin>>n;std::cout<<n*2;}',
            'java':'import java.util.*; public class Main {public static void main(String[] a){System.out.print(new Scanner(System.in).nextInt()*2);}}'}
        languages=self.tools.capabilities()['languages']
        if not languages:
            with self.assertRaises(ValueError):self.tools.compile({'language':'c','code':'','stdin':''})
        for language in languages:
            with self.subTest(language=language):
                result=self.tools.compile({'language':language,'code':programs[language],'stdin':'21'})
                self.assertEqual(result['status'],'ok',result);self.assertEqual(result['stdout'].strip(),'42')
                self.assertEqual(self.tools.compile({'language':language,'code':'not valid code!!!'})['status'],'compile-error')
    def test_api_token_origin_private_files_and_restart(self):
        class Quiet(launcher.CodeLabHandler):
            def log_message(self,*args):pass
        server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(self.root)))
        server.tools=self.tools
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        base='http://127.0.0.1:'+str(server.server_port)
        def request(path,token=None,origin=None,data=None):
            headers={'Content-Type':'application/json'}
            if token:headers['X-CodeLab-Token']=token
            if origin:headers['Origin']=origin
            try:
                with urlopen(Request(base+path,headers=headers,data=None if data is None else json.dumps(data).encode()),timeout=5) as response:return response.status,response.read()
            except HTTPError as error:
                try:return error.code,error.read()
                finally:error.close()
        try:
            status,body=request('/__codelab__/capabilities');self.assertEqual(status,200)
            token=json.loads(body)['token'];self.assertEqual(request('/__codelab__/progress')[0],403)
            self.assertEqual(request('/__codelab__/progress',token,'https://example.com')[0],403)
            self.assertEqual(request('/__codelab__/progress',token,data={'format':1,'records':{'cl_study_notes_html-start':{'value':'private','updatedAt':1,'device':'test'}}})[0],200)
            for path in ['/.codelab-data/progress.json','/%2ecodelab-data/progress.json','/.git/config']:
                self.assertEqual(request(path)[0],404)
            self.assertIn('private',request('/__codelab__/progress',token)[1].decode())
            server.tools=LocalTools(self.root);self.assertEqual(request('/__codelab__/progress',token)[0],403)
            self.assertEqual(request('/__codelab__/progress',server.tools.token)[0],200)
        finally:server.shutdown();server.server_close();thread.join(timeout=3)

if __name__=='__main__':unittest.main(verbosity=2)
