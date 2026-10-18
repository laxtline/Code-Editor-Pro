const {test,expect}=require('@playwright/test');
const HOST='http://127.0.0.1:4176/update-test/';

test('recovery page upgrades an actual legacy cache-first worker, respects other tabs and preserves notes',async({page,context,request})=>{
  await context.addInitScript(()=>{window.CODELAB_DISABLE_MONACO=true;window.CODELAB_DISABLE_PYTHON=true;try{localStorage.setItem('cl_first_visit','false');}catch{}});
  await context.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
  await request.post('http://127.0.0.1:4176/__test__/revision',{data:{revision:'test-after'}});
  await page.goto(HOST+'legacy.html');
  await page.evaluate(async()=>{
    localStorage.setItem('cl_study_notes_py-setup','Existing notes before the CodeLab update');
    await navigator.serviceWorker.register('legacy-worker.js',{scope:'./'});
    await navigator.serviceWorker.ready;
  });
  await page.waitForFunction(()=>!!navigator.serviceWorker.controller);
  const old=await context.newPage();await old.goto(HOST);await expect(old.locator('h1')).toHaveText('CodeLab old cached copy');
  await page.goto(HOST+'update.html');await expect(page.locator('#status')).toContainText('Close other StudyLab tabs');
  expect(await page.evaluate(()=>localStorage.getItem('cl_study_notes_py-setup'))).toBe('Existing notes before the CodeLab update');
  await old.close();await page.getByRole('button',{name:'Check and apply update',exact:true}).click();
  await expect(page).toHaveURL(HOST+'index.html#study');
  await expect(page.locator('.study-summary')).toContainText('145 lessons');
  await expect(page.locator('.logo')).toContainText('StudyLab');
  for(const name of ['Study Material','My Study','Smart Revision'])await expect(page.locator('#navbar').getByRole('button',{name,exact:true})).toBeVisible();
  await page.evaluate(()=>Study.show('python','py-setup'));await expect(page.locator('#study-personal-notes')).toHaveValue('Existing notes before the CodeLab update');
  await page.goto(HOST+'#study');await expect(page.locator('.study-summary')).toContainText('30 courses');
  await context.setOffline(true);await page.reload();await expect(page.locator('.study-summary')).toContainText('30 courses');
});
