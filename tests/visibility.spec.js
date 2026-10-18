const {test,expect}=require('@playwright/test');
const HOST='http://127.0.0.1:4174/Code-Editor-Pro/';
test.beforeEach(async({context})=>{
  await context.addInitScript(()=>{window.CODELAB_DISABLE_MONACO=true;window.CODELAB_DISABLE_PYTHON=true;try{localStorage.setItem('cl_first_visit','false');}catch{}});
  await context.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
});

test('three study sections stay visible in every mode and the full library lives inside Advanced',async({page})=>{
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('/');
  for(const mode of ['normal','advanced','exam','written']){
    await page.locator(`.mode-btn[data-mode="${mode}"]`).click();
    for(const label of ['Study Material','My Study','Smart Revision'])await expect(page.locator('#navbar').getByRole('button',{name:label,exact:true})).toBeVisible();
  }
  expect(await page.locator('#navbar [data-nav="library"]').count()).toBe(0);
  await page.locator('#navbar [data-nav="study"]').click();await expect(page.locator('.study-summary')).toContainText('145 lessons');
  await page.locator('#navbar [data-nav="dashboard"]').click();await expect(page.locator('#view-dashboard h1')).toHaveText("Today's study plan");
  await page.locator('#navbar [data-nav="revision"]').click();await expect(page.locator('#view-revision h1')).toHaveText('Smart revision');
  await page.locator('.mode-btn[data-mode="advanced"]').click();await page.getByRole('button',{name:/3 .*Offline Library/}).click();
  await expect(page.locator('#view-library h1')).toHaveText('Offline Library');await expect(page.locator('.mode-btn[data-mode="advanced"]')).toHaveClass(/active/);
  expect(await page.evaluate(()=>OfflineLibrary.catalog.stats.entries)).toBe(1643);
  await page.locator('.advanced-workspace-nav').getByRole('button',{name:'Coding problems',exact:true}).click();await expect(page.locator('#prob-tbody')).toBeVisible();
  await page.setViewportSize({width:390,height:844});
  for(const label of ['Study Material','My Study','Smart Revision'])await expect(page.locator('#navbar').getByRole('button',{name:label,exact:true})).toBeVisible();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);expect(errors).toEqual([]);
});

test('default index refreshes stale cached HTML and scripts, preserves notes and opens all study sections offline',async({page,context})=>{
  await page.goto(HOST);await page.waitForFunction(()=>!!navigator.serviceWorker.controller);
  await page.evaluate(async()=>{
    Store.setRaw('study_notes_py-setup','Keep my existing study notes');
    const cache=await caches.open(OfflineLibrary.cacheName()),old='<title>CodeLab</title><h1>CodeLab old cached copy</h1>';
    for(const path of ['./','index.html'])await cache.put(new URL(path,document.baseURI),new Response(old,{headers:{'Content-Type':'text/html'}}));
    await cache.put(new URL('assets/study.js',document.baseURI),new Response('throw new Error("stale study module");',{headers:{'Content-Type':'text/javascript'}}));
  });
  await context.setOffline(true);await page.goto(HOST);await expect(page.locator('h1')).toHaveText('CodeLab old cached copy');await context.setOffline(false);
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(HOST+'index.html#study');await expect(page.locator('.study-summary')).toContainText('30 courses');
  await page.goto(HOST+'#study');await expect(page.locator('.study-summary')).toContainText('30 courses');
  expect(await page.evaluate(()=>({lessons:Study.lessons().length,answers:Study.lessons().reduce((n,l)=>n+l.interviews.length,0),questions:Academy.data.questions.length}))).toEqual({lessons:145,answers:446,questions:1138});
  expect(await page.evaluate(()=>!!window.CODELAB_STANDALONE)).toBe(false);
  await page.locator('#navbar [data-nav="dashboard"]').click();await expect(page.locator('#view-dashboard h1')).toHaveText("Today's study plan");
  await page.locator('#navbar [data-nav="revision"]').click();await expect(page.locator('#view-revision h1')).toHaveText('Smart revision');
  await page.evaluate(()=>Study.show('python','py-setup'));await expect(page.locator('#study-personal-notes')).toHaveValue('Keep my existing study notes');
  await context.setOffline(true);await page.reload();await expect(page.locator('#study-personal-notes')).toHaveValue('Keep my existing study notes');
  await page.locator('#navbar [data-nav="revision"]').click();await expect(page.locator('#view-revision h1')).toHaveText('Smart revision');expect(errors).toEqual([]);
});
