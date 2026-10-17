const {test,expect}=require('@playwright/test');
const fs=require('node:fs');
const vm=require('node:vm');

test.beforeEach(async({context})=>{
  await context.addInitScript(()=>{window.CODELAB_DISABLE_MONACO=true;window.CODELAB_DISABLE_PYTHON=true;});
  await context.addInitScript(()=>{try{localStorage.setItem('cl_first_visit','false');}catch{}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
});

test('every classic item is explicitly reviewed and known faulty entries are corrected',async({page})=>{
  const box={window:{}};vm.runInNewContext(fs.readFileSync('assets/practice-data.js','utf8'),box);
  const data=box.window.CODELAB_PRACTICE;
  expect(data.questions).toHaveLength(1138);
  expect(data.counts).toMatchObject({original:794,reviewedLegacy:308,reviewedSectional:36,correctedLegacy:32});
  for(const q of [...data.questions.filter(q=>q.legacyOrdinal),...data.aptitudeReviewed]){
    expect(q.explanation.length).toBeGreaterThan(20);expect(q.formula).toBeTruthy();expect(q.options[q.answer]).toBeDefined();
  }
  const correct=(id)=>{const q=data.questions.find(q=>q.id===id);return q.options[q.answer];};
  expect(correct('legacy-034')).toBe('3 days');
  expect(correct('legacy-047')).toBe('23.89');
  expect(correct('legacy-083')).toBe('19.25');
  expect(correct('legacy-086')).toBe('Cannot be determined');
  expect(correct('legacy-092')).toBe('Cannot be determined');
  expect(correct('legacy-254')).toBe('Son');
  expect(correct('legacy-294')).toContain('1-3-4-5-2');
  expect(correct('legacy-304')).toBe('Monday');
  expect(correct('legacy-290')).not.toContain('without logging');
  expect(correct('aptitude-027')).toBe('Accommodate');
  await page.goto('/');
  expect(await page.evaluate(()=>WRITTEN_BANK.every(q=>q.explanation&&q.formula))).toBe(true);
  expect(await page.evaluate(()=>APTITUDE_BANK.every(q=>q.explanation&&q.formula))).toBe(true);
  expect(await page.evaluate(()=>WRITTEN_BANK[303].options[WRITTEN_BANK[303].answer])).toBe('Monday');
});

test('mixed selection spreads topics and sections instead of repeatedly drawing one family',async({page})=>{
  await page.goto('/');
  const result=await page.evaluate(()=>{
    const data=Academy.data.questions;
    return Array.from({length:40},(_,seed)=>{
      const mixed=Academy.sample(data,18,seed+1234);
      const quant=Academy.sample(data.filter(q=>q.section==='Quant'),20,seed+321);
      return {size:mixed.length,sections:mixed.reduce((n,q)=>(n[q.section]=(n[q.section]||0)+1,n),{}),topics:new Set(quant.map(q=>q.topic)).size,ids:new Set(mixed.map(q=>q.id)).size};
    });
  });
  for(const set of result){expect(set.size).toBe(18);expect(Object.values(set.sections)).toEqual([3,3,3,3,3,3]);expect(set.topics).toBe(20);expect(set.ids).toBe(18);}
});

test('displayed choice order, numeric shortcuts and answer scoring survive reload',async({page})=>{
  await page.goto('/');await page.locator('.mode-btn[data-mode="written"]').click();
  await page.selectOption('#prep-collection','classic');await page.fill('#prep-count','20');await page.selectOption('#prep-mode','timed');
  await page.getByRole('button',{name:'Start practice',exact:true}).click();
  const positions=await page.evaluate(()=>PracticeSession.current().ids.map((id,i)=>PracticeSession.current().orders[i].indexOf(PracticeSession.question(id).answer)));
  expect(new Set(positions).size).toBeGreaterThan(1);
  const before=await page.locator('.session-option').allTextContents();
  const displayed=await page.evaluate(()=>PracticeSession.order().indexOf(PracticeSession.question(PracticeSession.current().ids[0]).answer));
  await page.locator('#view-written h1').click();await page.keyboard.press(String(displayed+1));
  await expect(page.locator('.session-option').nth(displayed)).toHaveAttribute('aria-pressed','true');
  await page.reload();await page.waitForFunction(()=>!!PracticeSession.session);
  expect(await page.locator('.session-option').allTextContents()).toEqual(before);
  await expect(page.locator('.session-option').nth(displayed)).toHaveAttribute('aria-pressed','true');
  await page.evaluate(()=>PracticeSession.advance(false));
  expect(await page.evaluate(()=>PracticeSession.result.correct)).toBe(1);
});

test('RRB awareness excludes technical questions and advanced TCS uses hard questions',async({page})=>{
  await page.goto('/');await page.evaluate(()=>Academy.profile('tcs'));
  await page.selectOption('#profile-size','short');await page.getByRole('button',{name:'Start simulation',exact:true}).click();
  expect(await page.evaluate(()=>PracticeSession.session.sections[3].ids.every(id=>PracticeSession.question(id).difficulty==='Hard'))).toBe(true);
  await page.evaluate(()=>{PracticeSession.leave();Store.del('practice_session');Academy.profile('rrb');});
  await page.getByRole('button',{name:'Start simulation',exact:true}).click();
  expect(await page.evaluate(()=>PracticeSession.current().ids.map(id=>PracticeSession.question(id)).filter(q=>q.section==='GeneralAwareness').every(q=>q.examTags.includes('awareness')))).toBe(true);
  expect(await page.evaluate(()=>PracticeSession.current().ids.filter(id=>PracticeSession.question(id).section==='GeneralAwareness').length)).toBe(40);
});

test('classic written and sectional review screens contain worked answers',async({page})=>{
  await page.goto('/');
  await page.evaluate(()=>{App.setMode('written');Academy.legacyHome.call(WrittenTest);WrittenTest.sections=['Quant'];WrittenTest.count=10;WrittenTest.start();WrittenTest.answers[0]=WrittenTest.qs[0].answer;WrittenTest.finish(false);WrittenTest.openReview();});
  await expect(page.locator('#view-written .session-explanation')).toHaveCount(10);
  await page.evaluate(()=>{App.setMode('exam');Exam.config={company:'Classic review',name:'Candidate'};Aptitude.start(3,5,()=>Exam.showAptOnlyResult(),['Quant']);Aptitude.answers[0]=Aptitude.qs[0].answer;Aptitude.finish(false);});
  await page.getByRole('button',{name:'Review worked answers',exact:true}).click();
  expect(await page.evaluate(()=>PracticeSession.result.correct)).toBe(1);
  await expect(page.getByRole('heading',{name:'Session complete',exact:true})).toBeVisible();
  await page.locator('.academy-reviews details').first().click();await expect(page.locator('.session-explanation').first()).toBeVisible();
});

test('corrections are readable in the app',async({page})=>{
  await page.goto('/');await page.locator('.mode-btn[data-mode="written"]').click();
  await page.getByRole('button',{name:'Review corrections',exact:true}).click();
  await expect(page.getByRole('heading',{name:'Classic question corrections',exact:true})).toBeVisible();
  await expect(page.locator('#view-sources details')).toHaveCount(32);
  await page.getByText(/Classic 304:/).click();await expect(page.locator('#view-sources')).toContainText('Tomorrow is Monday');
});
