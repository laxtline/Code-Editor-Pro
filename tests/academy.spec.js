const {test,expect}=require('@playwright/test');
const fs=require('node:fs');
const vm=require('node:vm');
const {execFileSync}=require('node:child_process');
const path=require('node:path');
const {pathToFileURL}=require('node:url');

test.beforeEach(async({context})=>{
  await context.addInitScript(()=>{window.CODELAB_DISABLE_MONACO=true;window.CODELAB_DISABLE_PYTHON=true;});
  await context.addInitScript(()=>{try{localStorage.setItem('cl_first_visit','false');}catch{}});
  await context.route('**/*',r=>{const u=new URL(r.request().url());return u.hostname==='127.0.0.1'||u.protocol==='file:'?r.continue():r.abort();});
});

test('original explained bank, roadmap targets and cross-language references are consistent',async()=>{
  const box={window:{}};box.window=box;
  for(const file of ['practice-data','coding-data','advanced-coding','python-data'])vm.runInNewContext(fs.readFileSync(`assets/${file}.js`,'utf8'),box);
  const data=box.CODELAB_PRACTICE;
  expect(data.questions.length).toBeGreaterThanOrEqual(700);
  expect(new Set(data.questions.map(q=>q.q)).size).toBe(data.questions.length);
  for(const q of data.questions){expect(new Set(q.options).size).toBe(4);expect(q.options[q.answer]).toBeDefined();expect(q.explanation.length).toBeGreaterThan(20);expect(q.formula.length).toBeGreaterThan(10);}
  expect(data.roadmaps.map(t=>t.steps.length)).toEqual([10,12,12]);
  expect(data.roadmaps.map(t=>t.steps.reduce((n,s)=>n+s.target,0))).toEqual([140,200,240]);
  expect(box.CODELAB_CODING).toHaveLength(84);
  for(const q of box.CODELAB_CODING){expect(q.referenceCode.python,q.title).toBeTruthy();for(const t of q.testCases){let out;new Function('readline','console',q.referenceCode.javascript)(()=>t.input,{log:x=>{out=x;}});expect(JSON.parse(out),q.title).toEqual(JSON.parse(t.expectedOutput));}}
  const result=execFileSync('python',['tests/verify_python_references.py'],{input:JSON.stringify(box.CODELAB_CODING),encoding:'utf8',maxBuffer:8*1024*1024});
  expect(result).toContain('All Python reference cases passed');
});

test('topic learning, explanations, clear/review, scoring and mistake queue',async({page})=>{
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('/');await page.locator('.mode-btn[data-mode="written"]').click();
  await expect(page.getByRole('heading',{name:'Written Test Practice',exact:true})).toBeVisible();
  await page.selectOption('#prep-section','Quant');await page.selectOption('#prep-topic','percent');await page.fill('#prep-count','3');
  await page.getByRole('button',{name:'Start practice',exact:true}).click();
  const answer=await page.evaluate(()=>PracticeSession.question(PracticeSession.current().ids[0]).answer);
  await page.locator(`.session-option[data-option="${(answer+1)%4}"]`).click();
  await expect(page.locator('.session-explanation')).toContainText('Shortcut:');
  await page.getByRole('button',{name:'Clear response',exact:true}).click();
  expect(await page.evaluate(()=>Object.keys(PracticeSession.current().answers).length)).toBe(0);
  await page.getByRole('button',{name:'Mark for review',exact:true}).click();
  await page.locator(`.session-option[data-option="${(answer+1)%4}"]`).click();
  await page.getByRole('button',{name:'Save & next',exact:true}).click();
  await page.evaluate(()=>PracticeSession.answer(PracticeSession.question(PracticeSession.current().ids[1]).answer));
  await page.evaluate(()=>PracticeSession.advance(false));
  await expect(page.getByRole('heading',{name:'Session complete',exact:true})).toBeVisible();
  expect(await page.evaluate(()=>PracticeSession.result.correct)).toBe(1);
  expect(await page.evaluate(()=>PracticeSession.result.attempted)).toBe(2);
  await page.getByRole('button',{name:'New practice',exact:true}).click();
  await page.getByRole('button',{name:'Retry mistakes',exact:true}).click();
  expect(await page.evaluate(()=>PracticeSession.current().ids.length)).toBe(1);
  expect(errors).toEqual([]);
});

test('timed session resumes the same answers and deadline after reload',async({page})=>{
  await page.goto('/');await page.locator('.mode-btn[data-mode="written"]').click();
  await page.selectOption('#prep-mode','timed');await page.fill('#prep-count','2');await page.fill('#prep-minutes','2');
  await page.getByRole('button',{name:'Start practice',exact:true}).click();await page.locator('.session-option').nth(2).click();
  const deadline=await page.evaluate(()=>PracticeSession.session.deadline);
  await page.reload();await page.waitForFunction(()=>!!PracticeSession.session);
  expect(await page.evaluate(()=>PracticeSession.session.deadline)).toBe(deadline);
  await expect(page.locator('.session-option').nth(2)).toHaveAttribute('aria-pressed','true');
  await page.evaluate(()=>{PracticeSession.session.deadline=Date.now()-10;PracticeSession.tick();});
  await expect(page.getByRole('heading',{name:'Session complete',exact:true})).toBeVisible();
});

test('TCS sections lock and RRB quota/scoring are explicit',async({page})=>{
  await page.goto('/');await page.locator('.mode-btn[data-mode="exam"]').click();
  await page.getByRole('button',{name:/TCS NQT · Foundation \+ Advanced/}).click();
  await expect(page.locator('#view-exam')).toContainText('90');
  await page.selectOption('#profile-size','short');await page.getByRole('button',{name:'Start simulation',exact:true}).click();
  const all=await page.evaluate(()=>PracticeSession.session.sections.flatMap(s=>s.ids));expect(new Set(all).size).toBe(all.length);
  await page.evaluate(()=>PracticeSession.advance(false));
  expect(await page.evaluate(()=>PracticeSession.session.sectionIndex)).toBe(1);
  await expect(page.locator('.session-section-tabs .current')).toContainText('Verbal');
  await page.getByRole('button',{name:'Save & leave',exact:true}).click();
  await page.evaluate(()=>{Store.del('practice_session');Academy.profile('rrb');});
  await page.getByRole('button',{name:'Start simulation',exact:true}).click();
  const counts=await page.evaluate(()=>PracticeSession.current().ids.reduce((o,id)=>{const s=PracticeSession.question(id).section;o[s]=(o[s]||0)+1;return o;},{}));
  expect(counts).toEqual({Quant:30,Logical:30,GeneralAwareness:40});
  await page.evaluate(()=>{const sec=PracticeSession.current();sec.answers[0]=(PracticeSession.question(sec.ids[0]).answer+1)%4;PracticeSession.advance(false);});
  expect(await page.evaluate(()=>PracticeSession.result.score)).toBeCloseTo(-1/3,8);
});

test('offline editor, worker timeout and a judged JSON task work without CDN',async({page})=>{
  await page.goto('/');await page.locator('.mode-btn[data-mode="normal"]').click();
  await expect(page.locator('#pg-monaco .local-code-input')).toBeVisible();
  await page.selectOption('#pg-lang','javascript');
  await page.locator('#pg-monaco .local-code-input').fill('console.log(Number(readline()) * 2);');await page.fill('#pg-stdin','21');
  await page.locator('#view-playground .btn-run').click();await expect(page.locator('#pg-output')).toContainText('42');
  const limit=await page.evaluate(async()=>{try{await JsRun.run('while(true){}','',100);return false;}catch(e){return e.kind==='tle';}});expect(limit).toBe(true);
  await page.evaluate(()=>{App.setMode('advanced');Router.go('problem',10017);Editor.changeLang('javascript');Editor.instance.setValue(Questions.byId(10017).referenceCode.javascript);});
  await page.evaluate(()=>Runner.submit());await expect(page.locator('#tc-result')).toContainText('Accepted');
  expect(await page.evaluate(()=>judgeEqual('[1, 2]','[1,2]',Questions.byId(10017)))).toBe(true);
});

test('Monaco upgrade preserves local drafts and separate HTML/CSS/JS models',async({page,context})=>{
  await context.addInitScript(()=>{window.CODELAB_MONACO_BASE='http://127.0.0.1:4173/node_modules/monaco-editor/min/vs';});
  await page.goto('/');await page.locator('.mode-btn[data-mode="normal"]').click();
  await page.selectOption('#pg-lang','javascript');await page.locator('#pg-monaco .local-code-input').fill('const typedBeforeUpgrade = 42;');
  await page.addScriptTag({url:'/node_modules/monaco-editor/min/vs/loader.js'});await page.evaluate(()=>{window.CODELAB_DISABLE_MONACO=false;EditorTools.initRich();});
  await page.waitForFunction(()=>EditorTools.richReady&&!!Playground.instance.rich);
  expect(await page.evaluate(()=>Playground.instance.getValue())).toBe('const typedBeforeUpgrade = 42;');
  await page.evaluate(()=>{Playground.changeLang('html');Playground.instance.setValue('<h1>saved HTML</h1>');Playground.webTab('css');Playground.instance.setValue('h1 { color: red; }');Playground.webTab('html');});
  expect(await page.evaluate(()=>Playground.instance.getValue())).toBe('<h1>saved HTML</h1>');
  expect(await page.evaluate(()=>Playground.buildSrcDoc())).toContain('h1 { color: red; }');
});

test('all PDF tracks, staged coding resume, and classic tools stay available',async({page})=>{
  await page.goto('/');await page.getByRole('button',{name:/2 · DSA & company roadmaps/}).click();
  await expect(page.locator('#academy-tracks')).toContainText('DSA_Study_Steps.pdf');
  await page.locator('#academy-tracks select').first().selectOption('tech');
  await expect(page.locator('#academy-tracks')).toContainText('240');
  await page.locator('#academy-tracks .academy-step').first().getByRole('button',{name:'Open step'}).click();
  await expect(page.getByRole('heading',{name:'Python DSA Fundamentals & Bit Basics',exact:true})).toBeVisible();
  await page.getByRole('button',{name:'← Problems',exact:true}).click();
  await page.getByRole('button',{name:'Stage 1 coding mock',exact:true}).click();
  await page.selectOption('#lang-select','javascript');await page.locator('#monaco-container .local-code-input').fill('// exam draft');
  await page.evaluate(()=>Academy.snapshotCoding());const deadline=await page.evaluate(()=>Exam.deadline);
  await page.reload();await page.waitForFunction(()=>Exam.active);
  await expect(page.locator('#monaco-container .local-code-input')).toHaveValue('// exam draft');
  expect(await page.evaluate(()=>Exam.deadline)).toBe(deadline);
});

test('theory is searchable and classic written controls still work',async({page})=>{
  await page.goto('/');await page.locator('[data-nav="theory"]').click();await page.fill('#theory-search','compound');
  await page.locator('#theory-topics button').click();await expect(page.locator('#theory-lesson')).toContainText('CI−SI');
  await page.locator('.mode-btn[data-mode="written"]').click();await page.getByRole('button',{name:'Classic practice',exact:true}).click();
  const n=await page.locator('#wt-sections .sec-toggle.active').count();await page.locator('#wt-sections .sec-toggle').first().click();
  await expect(page.locator('#wt-sections .sec-toggle.active')).toHaveCount(n-1);
});

test('missing Python runtime preserves coding submissions without a false wrong-answer verdict',async({page})=>{
  await page.goto('/');
  await page.evaluate(()=>{Academy.startCoding({stage:1,count:1,minutes:45},'Runtime availability check');Editor.changeLang('python');Editor.instance.setValue('print(1)');});
  await page.evaluate(()=>Exam.submitExam(false));
  await expect(page.locator('#view-result .big-score')).toHaveText('Evaluation incomplete');
  await expect(page.locator('#view-result')).toContainText('Not evaluated');
  expect(await page.evaluate(()=>!!Store.get('coding_session',null))).toBe(true);
});

test('single HTML works after moving away from all project assets',async({page},testInfo)=>{
  const target=testInfo.outputPath('portable.html');fs.copyFileSync('CodeLab-Offline.html',target);
  const missing=[];page.on('requestfailed',req=>{if(req.url().startsWith('file:'))missing.push(req.url());});
  await page.goto(pathToFileURL(target).href+'#library/lc-156');
  await expect(page.getByRole('heading',{name:'156. Binary Tree Upside Down',exact:true})).toBeVisible();
  const img=page.locator('#lib-reading img').first();await img.scrollIntoViewIfNeeded();await expect.poll(()=>img.evaluate(el=>el.complete&&el.naturalWidth>0)).toBe(true);
  await page.locator('[data-nav="theory"]').click();await expect(page.getByRole('heading',{name:'Theory, formulas & shortcuts',exact:true})).toBeVisible();
  expect(missing).toEqual([]);
});
