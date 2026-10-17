const {test,expect}=require('@playwright/test');
const fs=require('node:fs');
const path=require('node:path');
const net=require('node:net');
const {execFileSync}=require('node:child_process');

test('Windows PowerShell launcher handles occupied ports, spaced folders, reuse and verified stop',async({request})=>{
  test.skip(process.platform!=='win32','Windows-only Vivaldi launcher; packaged browser runtime tests run on every OS.');
  const root=path.resolve('test-results/Launcher space [portable]');fs.mkdirSync(root,{recursive:true});
  for(const name of ['Start-CodeLab.py','Start-CodeLab-Vivaldi.ps1','index.html'])fs.copyFileSync(name,path.join(root,name));
  fs.mkdirSync(path.join(root,'assets'),{recursive:true});fs.copyFileSync('assets/runtime-manifest.js',path.join(root,'assets/runtime-manifest.js'));
  const occupied=net.createServer(socket=>socket.destroy());await new Promise(resolve=>occupied.listen(0,'127.0.0.1',resolve));
  const port=occupied.address().port;expect(port).toBeLessThanOrEqual(65525);
  const launch=path.join(root,'Start-CodeLab-Vivaldi.ps1');
  const run=args=>execFileSync('powershell.exe',['-NoProfile','-File',launch,...args],{encoding:'utf8',timeout:30000});
  let started=false;
  try{
    const output=run(['-NoBrowser','-Port',String(port)]);started=true;expect(output).toContain('Background server ready.');
    const state=()=>JSON.parse(fs.readFileSync(path.join(root,'.codelab-server.json'),'utf8').replace(/^\uFEFF/,''));
    const first=state();expect(new URL(first.url).port).not.toBe(String(port));
    const health=await (await request.get(first.url+'__codelab__/health')).json();expect(health.root.toLowerCase()).toBe(root.toLowerCase());expect(health.pid).toBe(first.pid);
    run(['-NoBrowser']);expect(state().pid).toBe(first.pid);
    run(['-LiveServer','-Port',new URL(first.url).port,'-NoBrowser']);expect(state().pid).toBe(first.pid);
    const stopped=run(['-Stop']);started=false;expect(stopped).toContain('background server stopped');expect(fs.existsSync(path.join(root,'.codelab-server.json'))).toBe(false);
    expect(occupied.listening).toBe(true);
  }finally{if(started)try{run(['-Stop']);}catch{}await new Promise(resolve=>occupied.close(resolve));}
});
