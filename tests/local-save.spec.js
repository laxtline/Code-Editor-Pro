const {test,expect}=require('@playwright/test');
const fs=require('node:fs');const path=require('node:path');
const {spawn,execFileSync}=require('node:child_process');

test('local process limits, optional native compilers and same-origin backup API',()=>{
  expect(execFileSync('python',['tests/verify_local_tools.py'],{encoding:'utf8',timeout:120000,maxBuffer:1024*1024})).toBe('');
});

test('two local origins restore folder notes, avoid save ping-pong, retain tombstones and refresh restarted tokens',async({browser,request},info)=>{
  test.setTimeout(120000);
  const root=info.outputPath('local app');fs.mkdirSync(root,{recursive:true});
  // Symlink-free copy excludes all private/user files and never mutates _site.
  for(const name of ['index.html','Start-CodeLab.py','local_tools.py'])fs.copyFileSync(name,path.join(root,name));
  for(const name of ['assets','vendor','offline'])fs.cpSync(name,path.join(root,name),{recursive:true});
  const servers=[];const contexts=[];
  const start=async port=>{
    const child=spawn('python',[path.join(root,'Start-CodeLab.py'),'--no-browser','--strict-port','--port',String(port)],{stdio:'ignore'});servers.push(child);
    await expect.poll(async()=>{try{return (await request.get(`http://127.0.0.1:${port}/__codelab__/capabilities`)).status();}catch{return 0;}}).toBe(200);return child;
  };
  const open=async port=>{
    const context=await browser.newContext();contexts.push(context);
    await context.addInitScript(()=>{window.CODELAB_DISABLE_MONACO=true;window.CODELAB_DISABLE_PYTHON=true;localStorage.setItem('cl_first_visit','false');});
    const page=await context.newPage();await page.goto(`http://127.0.0.1:${port}/index.html#study/html/html-start`);
    await page.waitForFunction(()=>!!LocalBridge.capabilities);return page;
  };
  try{
    let first=await start(4187);await start(4188);const a=await open(4187);
    await a.fill('#study-personal-notes','Folder revision survives another origin');
    await a.evaluate(()=>{Store.set('settings',{...SETTINGS,jdoodleId:'PRIVATE-ID',jdoodleSecret:'PRIVATE-SECRET'});});
    await expect.poll(()=>fs.existsSync(path.join(root,'.codelab-data/progress.json'))&&fs.readFileSync(path.join(root,'.codelab-data/progress.json'),'utf8')).toContain('Folder revision');
    expect(fs.readFileSync(path.join(root,'.codelab-data/progress.json'),'utf8')).not.toContain('PRIVATE-');
    const b=await open(4188);await expect(pageNotes(b)).toHaveValue('Folder revision survives another origin');
    const clock=await b.evaluate(()=>SaveBridge.clock['cl_study_notes_html-start'].updatedAt);
    await b.evaluate(()=>Store.setRaw('study_notes_html-start','Folder revision survives another origin'));
    expect(await b.evaluate(()=>SaveBridge.clock['cl_study_notes_html-start'].updatedAt)).toBe(clock);
    await b.evaluate(()=>{Store.del('study_notes_html-start');return SaveBridge.sync();});
    await a.evaluate(()=>SaveBridge.sync());await expect(pageNotes(a)).toHaveValue('');
    const oldToken=await a.evaluate(()=>LocalBridge.capabilities.token);
    first.kill();await new Promise(resolve=>first.once('exit',resolve));first=await start(4187);
    await a.evaluate(()=>LocalBridge.request('progress'));expect(await a.evaluate(()=>LocalBridge.capabilities.token)).not.toBe(oldToken);
  }finally{
    for(const context of contexts)await context.close();
    for(const child of servers)if(child.exitCode===null)child.kill();
  }
});
function pageNotes(page){return page.locator('#study-personal-notes');}
