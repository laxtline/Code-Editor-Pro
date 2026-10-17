const {test,expect}=require('@playwright/test');
const fs=require('node:fs');
const HOST='http://127.0.0.1:4176/update-test/';
test.use({actionTimeout:10000});

test.beforeEach(async({context})=>{
  await context.addInitScript(()=>{window.CODELAB_DISABLE_MONACO=true;window.CODELAB_DISABLE_PYTHON=true;try{localStorage.setItem('cl_first_visit','false');}catch{}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
});

test('real waiting worker respects active sessions and other tabs, then reloads with saved drafts',async({page,context,request})=>{
  await request.post('http://127.0.0.1:4176/__test__/revision',{data:{revision:'test-before'}});
  await page.goto(HOST);
  await page.waitForFunction(()=>!!navigator.serviceWorker.controller&&!!OfflineUpdates.registration);
  await expect(page.getByRole('button',{name:'Online / Offline',exact:true})).toBeVisible();
  const other=await context.newPage();await other.goto(HOST);
  await page.locator('.mode-btn[data-mode="written"]').click();await page.selectOption('#prep-mode','timed');await page.fill('#prep-count','2');
  await page.getByRole('button',{name:'Start practice',exact:true}).click();await page.locator('.session-option').nth(1).click();
  const saved=await page.evaluate(()=>({deadline:PracticeSession.session.deadline,answers:PracticeSession.current().answers}));
  await request.post('http://127.0.0.1:4176/__test__/revision',{data:{revision:'test-after'}});
  // Practice disables navigation; exercise the update guard directly as well.
  await page.evaluate(()=>OfflineAccess.open());await page.getByRole('button',{name:'Check for updates',exact:true}).click();
  await page.waitForFunction(()=>!!OfflineUpdates.registration.waiting);
  await page.getByRole('button',{name:'Apply update & reload',exact:true}).click();await expect(page.locator('#offline-update-status')).toContainText('Finish or save and leave');
  expect(await page.evaluate(()=>OfflineLibrary.catalog.revision)).toBe('test-before');
  await page.evaluate(()=>{UI.close();PracticeSession.leave();});
  await page.getByRole('button',{name:/Online \/ Offline/}).click();await page.getByRole('button',{name:'Apply update & reload',exact:true}).click();
  await expect(page.locator('#offline-update-status')).toContainText('Close other CodeLab tabs');
  await other.close();
  await page.evaluate(()=>{UI.close();App.setMode('normal');Playground.instance.setValue('print("draft just before update")');});
  await page.getByRole('button',{name:/Online \/ Offline/}).click();
  await Promise.all([page.waitForEvent('load'),page.getByRole('button',{name:'Apply update & reload',exact:true}).click()]);
  await page.waitForFunction(()=>typeof OfflineLibrary!=='undefined'&&OfflineLibrary.catalog.revision==='test-after');
  expect(await page.evaluate(()=>Store.getRaw('pg_code_python',''))).toBe('print("draft just before update")');
  expect(await page.evaluate(()=>({deadline:Store.get('practice_session').deadline,answers:Store.get('practice_session').sections[0].answers}))).toEqual(saved);
  expect(await page.evaluate(()=>caches.keys())).not.toContain('codelab-library-v2-%2Fupdate-test%2F-test-before');
  await context.setOffline(true);await page.reload();await expect(page.locator('.mode-btn[data-mode="written"]')).toBeVisible();
});

test('backup captures immediate drafts, omits credentials, and restores legacy files without stale editor overwrite',async({page})=>{
  await page.goto('/');await page.locator('.mode-btn[data-mode="normal"]').click();
  await page.evaluate(()=>{SETTINGS.jdoodleId='private-client';SETTINGS.jdoodleSecret='private-secret';Store.set('settings',SETTINGS);Playground.instance.setValue('print("last keystroke")');Store.set('solved',[10001]);});
  const downloadPromise=page.waitForEvent('download');await page.evaluate(()=>DataIO.exportProgress());
  const backup=JSON.parse(fs.readFileSync(await (await downloadPromise).path(),'utf8'));
  expect(backup._codelab.format).toBe(1);expect(backup._raw.cl_pg_code_python).toBe('print("last keystroke")');expect(backup.settings).not.toHaveProperty('jdoodleSecret');expect(backup.settings).not.toHaveProperty('jdoodleId');
  const fullStorage=await page.evaluate(()=>{
    const set=Storage.prototype.setItem;Storage.prototype.setItem=()=>{throw new DOMException('Full','QuotaExceededError');};
    try{Playground.instance.setValue('print("recover even with full storage")');const raw=ProgressBackup.create()._raw;let refused=false;try{ProgressBackup.flush(true);}catch{refused=true;}return {draft:raw.cl_pg_code_python,refused};}finally{Storage.prototype.setItem=set;}
  });
  expect(fullStorage).toEqual({draft:'print("recover even with full storage")',refused:true});
  const legacy={solved:[10002],settings:{theme:'light',jdoodleSecret:'never-overwrite'},_raw:{cl_pg_code_python:'print("restored backup")',cl_library_notes_lc1:'review'}};
  const chooser=page.waitForEvent('filechooser');await page.evaluate(()=>DataIO.importProgress());await (await chooser).setFiles({name:'legacy.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(legacy))});
  await expect.poll(()=>page.evaluate(()=>Store.get('solved',[]))).toEqual([10002]);
  expect(await page.evaluate(()=>SETTINGS.jdoodleSecret)).toBe('private-secret');
  expect(await page.evaluate(()=>Playground.instance.getValue())).toBe('print("restored backup")');
  await page.reload();expect(await page.evaluate(()=>Playground.instance.getValue())).toBe('print("restored backup")');
});

test('invalid backups cannot write unrelated keys and quota failures restore previous values',async({page})=>{
  await page.goto('/');
  const result=await page.evaluate(()=>{
    Store.set('solved',[10001]);Store.setRaw('library_notes_lc1','existing notes');
    const bad=[{solved:'wrong shape'},{solved:[2],_raw:{unrelated:'bad'}},{settings:{fontSize:'bad'}},JSON.parse('{"solved":[2],"_raw":{"__proto__":"bad"}}'),{_codelab:{format:99},solved:[2]}];
    const rejected=bad.map(data=>{try{ProgressBackup.restore(data);return false;}catch{return true;}});
    const set=Storage.prototype.setItem;let failed=false;
    Storage.prototype.setItem=function(key,value){if(key==='cl_library_notes_lc1'&&!failed){failed=true;throw new DOMException('Quota exceeded','QuotaExceededError');}return set.call(this,key,value);};
    let error;try{ProgressBackup.restore({solved:[10002],_raw:{cl_library_notes_lc1:'new notes'}});}catch(e){error=e.message;}finally{Storage.prototype.setItem=set;}
    return {rejected,error,solved:Store.get('solved'),notes:Store.getRaw('library_notes_lc1'),unrelated:localStorage.getItem('unrelated')};
  });
  expect(result.rejected).toEqual([true,true,true,true,true]);expect(result.error).toContain('previous progress was restored');expect(result.solved).toEqual([10001]);expect(result.notes).toBe('existing notes');expect(result.unrelated).toBeNull();
});
