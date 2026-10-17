const {test,expect}=require('@playwright/test');
const fs=require('node:fs');
const vm=require('node:vm');
test.beforeEach(async({context})=>{
  await context.addInitScript(()=>{window.CODELAB_DISABLE_MONACO=true;try{localStorage.setItem('cl_first_visit','false');}catch{}});
  await context.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.abort());
});

test('syllabus maps all 276 skills to substantive lessons and original visual sets are complete',()=>{
  const box={window:{}};
  for(const file of ['study-data','practice-data'])vm.runInNewContext(fs.readFileSync(`assets/${file}.js`,'utf8'),box);
  const study=box.window.CODELAB_STUDY,bank=box.window.CODELAB_PRACTICE;
  const lessons=study.courses.flatMap(c=>c.lessons);
  expect(study.courses).toHaveLength(30);expect(lessons).toHaveLength(145);
  expect(new Set(study.skills.map(s=>s.number)).size).toBe(276);
  expect(lessons.reduce((n,l)=>n+l.interviews.length,0)).toBe(446);
  for(const skill of study.skills)expect(lessons.some(l=>l.id===skill.lesson)).toBe(true);
  for(const l of lessons){expect(l.body.split(/\s+/).length,l.id).toBeGreaterThanOrEqual(100);expect(l.quiz.options[l.quiz.answer]).toBeTruthy();expect(l.exercise.length).toBeGreaterThan(40);}
  expect(bank.questions.filter(q=>q.visual?.type==='sequence')).toHaveLength(12);
  expect(bank.questions.filter(q=>q.passage)).toHaveLength(12);
  expect(bank.questions.filter(q=>['bar','table'].includes(q.visual?.type))).toHaveLength(12);
});

test('lesson navigation, instant notes, HTML preview, completion and interview search survive reload',async({page},info)=>{
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('/#study/subjects/web');await expect(page.locator('#view-study h1')).toHaveText('Web Development');await expect(page.locator('.study-subject-sequence article')).toHaveCount(12);
  await page.evaluate(()=>Study.show('html','html-start'));
  await expect(page.locator('#view-study h1')).toContainText('Document structure');
  await page.fill('#study-personal-notes','My offline revision note <script>no()</script>');
  await page.reload();await expect(page.locator('#study-personal-notes')).toHaveValue('My offline revision note <script>no()</script>');
  await page.fill('#study-example-code','<h1>Learning offline</h1>');await page.click('#study-run');
  await expect(page.frameLocator('#study-example-preview').locator('h1')).toHaveText('Learning offline');
  await page.click('#study-complete');expect(await page.evaluate(()=>Study.progress()['html-start'].completed)).toBe(true);
  await page.evaluate(()=>Study.show('os','os-memory'));await page.click('#nav-back');
  await expect(page.locator('#view-study h1')).toContainText('Document structure');
  await page.click('#nav-forward');await expect(page.locator('#view-study h1')).toContainText('memory');
  await page.evaluate(()=>Study.interviews('os'));await page.fill('#interview-search','memory');
  expect(await page.locator('#study-interview-list details').count()).toBeGreaterThan(0);
  await page.evaluate(()=>Learning.dashboard());await expect(page.locator('#view-dashboard')).toContainText('1');
  await page.setViewportSize({width:390,height:844});await page.evaluate(()=>Study.show('html','html-start'));
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  await page.screenshot({path:info.outputPath('study-mobile.png'),fullPage:true});
  for(const width of [1536,1920]){await page.setViewportSize({width,height:980});expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);}
  expect(errors).toEqual([]);
});

test('calendar spaced revision advances 1, 3, 7, 14 days, never postpones early review and resets mistakes',async({page})=>{
  await page.clock.setSystemTime(new Date('2026-10-18T06:00:00Z'));await page.goto('/');
  const id=await page.evaluate(()=>Academy.data.questions[0].id);
  const record=async(correct,number)=>page.evaluate(({id,correct,number})=>Learning.record({id:'mcq:'+id,eventId:'test-'+number,source:'mcq',topic:PracticeSession.question(id).topic,correct,timeMs:1200}),{id,correct,number});
  const card=()=>page.evaluate(id=>Store.get('revision_state',{})['mcq:'+id],id);
  await record(false,0);let current=await card();
  expect(await page.evaluate(due=>Learning.day(due),current.due)).toBe('2026-10-19');
  await record(true,1);expect((await card()).due).toBe(current.due);
  for(const [number,interval] of [[2,3],[3,7],[4,14],[5,null]]){
    await page.clock.setSystemTime(new Date(current.due+1000));await record(true,number);current=await card();
    if(interval)expect(await page.evaluate(({due,interval})=>Learning.day(due)===Learning.day(Learning.after(interval)),{due:current.due,interval})).toBe(true);
  }
  expect(current.graduated).toBe(true);await record(false,6);expect((await card()).step).toBe(0);expect((await card()).graduated).toBe(false);
});

test('question timing, unanswered analysis and classic answer/deadline restore are saved',async({page})=>{
  await page.goto('/');await page.evaluate(()=>PracticeSession.begin({title:'Timing check',kind:'practice',learn:false,marks:1,penalty:0,sections:[{label:'Quant',duration:120,ids:Academy.data.questions.slice(0,2).map(q=>q.id)}]}));
  await page.waitForTimeout(1200);await page.evaluate(()=>PracticeSession.answer(PracticeSession.question(PracticeSession.current().ids[0]).answer));
  const deadline=await page.evaluate(()=>PracticeSession.session.deadline);await page.reload();
  expect(await page.evaluate(()=>PracticeSession.session.deadline)).toBe(deadline);
  await page.evaluate(()=>PracticeSession.advance(false));
  await expect(page.locator('.exam-deep-analysis')).toContainText('1 unanswered');
  expect(await page.evaluate(()=>Store.get('practice_history',[])[0].rows[0].timeMs)).toBeGreaterThan(500);
  await page.evaluate(()=>{Navigation.open({view:'written'});Academy.legacyHome.call(WrittenTest);WrittenTest.start();WrittenTest.choose(2);});
  const old=await page.evaluate(()=>({deadline:WrittenTest.deadline,id:WrittenTest.qs[0].id}));
  await page.reload();await page.waitForFunction(()=>WrittenTest.active);
  expect(await page.evaluate(()=>({deadline:WrittenTest.deadline,id:WrittenTest.qs[0].id,answer:WrittenTest.answers[0]}))).toEqual({...old,answer:2});
  await page.click('#nav-back');expect(await page.evaluate(()=>!!Store.get('classic_session',null))).toBe(true);
});

test('all bundled Python and JavaScript examples execute using local engines, including async lessons',async({page})=>{
  await page.goto('/');await page.waitForFunction(()=>Py.ready);
  const results=await page.evaluate(async()=>{
    const rows=[];
    for(const lesson of Study.lessons()){
      const e=lesson.example;if(!e||!['python','javascript'].includes(e.lang))continue;
      const result=e.lang==='python'?await Py.run(e.code,e.stdin,5000):await JsRun.run(e.code,e.stdin,5000);
      rows.push({id:lesson.id,...result,expected:e.expected});
    }return rows;
  });
  expect(results.length).toBeGreaterThan(30);
  for(const r of results){expect(r.stderr,r.id).toBe('');if(r.id!=='react-design')expect(r.stdout.trim(),r.id).toBe(r.expected);}
  for(const id of ['sql-query','sql-advanced','db-transactions']){
    const result=await page.evaluate(async id=>SqlRun.run(Study.lessons().find(l=>l.id===id).example.code),id);expect(result.stderr,id).toBe('');expect(result.stdout.length).toBeGreaterThan(0);
  }
});

test('diagram, passage and table questions render in practice, theory and result explanations',async({page})=>{
  await page.goto('/');
  for(const topic of ['diagram-patterns','reading-evidence','chart-caselets']){
    await page.evaluate(topic=>Academy.theory(topic),topic);
    await expect(page.locator('#theory-lesson .question-visual, #theory-lesson .question-passage')).toHaveCount(1);
    await page.evaluate(topic=>{const q=Academy.data.questions.find(q=>q.topic===topic);PracticeSession.begin({title:'Visual test',kind:'practice',learn:true,marks:1,penalty:0,sections:[{label:topic,duration:null,ids:[q.id]}]});},topic);
    expect(await page.locator('#view-written .question-visual,#view-written .question-passage').count()).toBeGreaterThan(0);
    await page.evaluate(()=>{PracticeSession.answer(PracticeSession.question(PracticeSession.current().ids[0]).answer);PracticeSession.advance(false);});
  }
});

test('normal judged DSA mistakes and accepted retries feed revision and daily practice',async({page})=>{
  await page.goto('/');await page.evaluate(()=>{Router.go('problem',10067);Editor.changeLang('javascript');Editor.instance.setValue('console.log(0)');});
  await page.evaluate(()=>Runner.submit());expect(await page.evaluate(()=>Store.get('revision_state',{})['coding:10067'].reason)).toBe('Incorrect');
  const due=await page.evaluate(()=>Store.get('revision_state',{})['coding:10067'].due);
  await page.evaluate(()=>{Editor.instance.setValue(Questions.byId(10067).referenceCode.javascript);return Runner.submit();});
  expect(await page.evaluate(()=>Store.get('revision_state',{})['coding:10067'].due)).toBe(due);
  expect(await page.evaluate(()=>Learning.daily()[Learning.day()].questions)).toBe(2);
});
