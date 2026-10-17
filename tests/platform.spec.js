const {test,expect}=require('@playwright/test');
const fs=require('node:fs');
const path=require('node:path');
const {execFileSync,spawn}=require('node:child_process');
const HOST='http://127.0.0.1:4174/Code-Editor-Pro/';

test.beforeEach(async({context})=>{
  await context.addInitScript(()=>{try{localStorage.setItem('cl_first_visit','false');}catch{}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
});

test('packaged GitHub project path loads local Python, SQL, Monaco and install metadata',async({page,request})=>{
  await page.goto(HOST);
  await page.waitForFunction(()=>Py.ready&&EditorTools.richReady);
  const result=await page.evaluate(async()=>({python:await Py.run('import sys, json\nprint(json.loads(sys.stdin.readline())[0]+int(input()))','[20]\n22\n',5000),sql:await SqlRun.run('SELECT 21*2 AS answer;'),base:RuntimeAssets.base('python')}));
  expect(result.python).toEqual({stdout:'42\n',stderr:''});expect(result.sql.stdout).toContain('42');expect(result.base).toBe(HOST+'vendor/runtimes/python/');
  const manifest=await (await request.get(HOST+'manifest.webmanifest')).json();expect(manifest.scope).toBe('./');expect(manifest.start_url).toBe('./');
  for(const icon of manifest.icons)expect((await request.get(HOST+icon.src)).ok()).toBe(true);
  await page.getByRole('button',{name:'Online / Offline',exact:true}).click();
  await expect(page.getByRole('heading',{name:'Use StudyLab online & offline',exact:true})).toBeVisible();
  await expect(page.getByRole('link',{name:'Download full offline ZIP',exact:true})).toHaveAttribute('href','downloads/CodeLab-Offline.zip');
});

test('Python handles JSON stdin, exceptions, timeout termination and a fresh worker',async({page})=>{
  await page.goto(HOST);await page.waitForFunction(()=>Py.ready);
  const accepted=await page.evaluate(async()=>{const q=Questions.byId(10055);return await Py.run(q.referenceCode.python,q.testCases[0].input,5000);});expect(JSON.parse(accepted.stdout)).toEqual([3,2,1]);expect(accepted.stderr).toBe('');
  const fail=await page.evaluate(()=>Py.run('raise ValueError("expected test error")','',5000));expect(fail.stderr).toContain('ValueError: expected test error');
  expect(await page.evaluate(async()=>{try{await Py.run('while True: pass','',150);return false;}catch(error){return error.kind==='tle';}})).toBe(true);
  await page.waitForFunction(()=>Py.ready);
  expect(await page.evaluate(()=>Py.run('print(6*7)','',5000))).toEqual({stdout:'42\n',stderr:''});
});

test('saved full app boots offline from a new tab with Python, SQL, rich editor and unread library entries',async({page,context})=>{
  await page.goto(HOST+'#library');await page.evaluate(()=>OfflineLibrary.saveOffline());
  await expect(page.locator('#lib-cache-status')).toContainText('Ready offline.');
  expect(await page.evaluate(()=>RuntimeAssets.saved())).toBe('ready');
  await context.setOffline(true);
  const offline=await context.newPage();await offline.goto(HOST+'?offline=1#library/lc-156');
  await expect(offline.getByRole('heading',{name:'156. Binary Tree Upside Down',exact:true})).toBeVisible();
  await offline.waitForFunction(()=>Py.ready&&EditorTools.richReady);
  expect(await offline.evaluate(()=>Py.run('import json, sys\nprint(sum(json.load(sys.stdin)))','[20,22]',5000))).toEqual({stdout:'42\n',stderr:''});
  expect((await offline.evaluate(()=>SqlRun.run('SELECT 42 AS answer;'))).stdout).toContain('42');
  await offline.evaluate(()=>Study.subject('ai'));await expect(offline.locator('#view-study h1')).toHaveText('AI / ML');
  await offline.evaluate(()=>Study.show('python','py-strings'));await offline.fill('#study-personal-notes','Saved while offline');await offline.reload();await expect(offline.locator('#study-personal-notes')).toHaveValue('Saved while offline');
  await offline.getByRole('button',{name:'Online / Offline',exact:true}).click();
  await expect(offline.locator('#offline-readiness')).toContainText('Ready offline.');await expect(offline.locator('#connection-state')).toContainText('Offline');
});

test('offline readiness detects a missing engine file and cache names isolate repository paths',async({page})=>{
  page.on('requestfailed',request=>{if(request.url().includes('127.0.0.1'))console.log('Local request failed:',request.url(),request.failure()?.errorText);});
  await page.goto(HOST+'#library');await page.evaluate(()=>OfflineLibrary.saveOffline());
  await expect(page.locator('#lib-cache-status')).toContainText('Ready offline.');
  expect(await page.evaluate(()=>RuntimeAssets.saved())).toBe('ready');
  await page.evaluate(async()=>{const cache=await caches.open(OfflineLibrary.cacheName());await cache.delete(new URL('vendor/runtimes/python/pyodide.asm.wasm',document.baseURI).href);});
  expect(await page.evaluate(()=>RuntimeAssets.saved())).toBe('partial');
  expect(await page.evaluate(()=>OfflineLibrary.cacheName())).toContain('%2FCode-Editor-Pro%2F');
  await page.getByRole('button',{name:'Online / Offline',exact:true}).click();await expect(page.locator('#offline-readiness')).toContainText('incomplete');
});

test('downloaded ZIP includes all runtime hashes and runs without external network requests',async({page,request})=>{
  const unpack=path.resolve('test-results/offline-runtime-package');fs.mkdirSync(unpack,{recursive:true});
  execFileSync('python',['-m','zipfile','-e','downloads/CodeLab-Offline.zip',unpack]);
  const root=path.join(unpack,'StudyLab');
  expect(fs.existsSync(path.join(root,'.git'))).toBe(false);expect(fs.existsSync(path.join(root,'node_modules'))).toBe(false);
  expect(fs.existsSync(path.join(root,'OFFLINE-START-HERE.md'))).toBe(true);expect(fs.existsSync(path.join(root,'Start-CodeLab-Vivaldi.ps1'))).toBe(true);
  expect(JSON.parse(fs.readFileSync(path.join(root,'.vscode/settings.json'),'utf8'))).not.toHaveProperty('liveServer.settings.AdvanceCustomBrowserCmdLine');
  const check=execFileSync('python',['-c',`import json,hashlib,pathlib;root=pathlib.Path(${JSON.stringify(root)});j=json.loads((root/'assets/runtime-manifest.js').read_text().removeprefix('window.CODELAB_RUNTIME=').rstrip(';\\n'));assert all(hashlib.sha256((root/f['path']).read_bytes()).hexdigest()==f['sha256'] for f in j['files']);print('Verified all bundled runtime hashes')`],{encoding:'utf8'});expect(check).toContain('Verified all bundled runtime hashes');
  const server=spawn('python',[path.join(root,'Start-CodeLab.py'),'--no-browser','--port','4175'],{stdio:'ignore'});
  try{
    await expect.poll(async()=>{try{return (await request.get('http://127.0.0.1:4175/')).ok();}catch{return false;}}).toBe(true);
    await page.goto('http://127.0.0.1:4175/#library');await page.waitForFunction(()=>Py.ready&&EditorTools.richReady);
    expect(await page.evaluate(()=>Py.run('print(42)','',5000))).toEqual({stdout:'42\n',stderr:''});
    expect((await page.evaluate(()=>SqlRun.run('SELECT 42 AS answer;'))).stdout).toContain('42');
    await expect(page.getByRole('heading',{name:'Offline Library',exact:true})).toBeVisible();
  }finally{server.kill();}
});
