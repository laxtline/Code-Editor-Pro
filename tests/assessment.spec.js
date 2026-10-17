const {test,expect}=require('@playwright/test');
const fs=require('node:fs');
const vm=require('node:vm');
const {execFileSync}=require('node:child_process');

test.beforeEach(async({context})=>{
  await context.addInitScript(()=>{window.CODELAB_DISABLE_MONACO=true;window.CODELAB_DISABLE_PYTHON=true;});
  await context.addInitScript(()=>{try{localStorage.setItem('cl_first_visit','false');}catch{}});
  await context.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
});

async function codingRound(page,ids=[10055,10056]){
  await page.goto('/');
  await page.evaluate(ids=>{App.mode='exam';document.body.dataset.mode='exam';Exam.config={name:'Candidate',company:'Coding feedback test',dur:45,n:ids.length,set:'Staged DSA practice'};Exam.qids=ids;Exam.beginCoding();},ids);
}

test('new data-structure references agree with independent small-input oracles',()=>{
  const box={};box.window=box;
  for(const file of ['coding-data','python-data'])vm.runInNewContext(fs.readFileSync(`assets/${file}.js`,'utf8'),box);
  const items=box.CODELAB_CODING.filter(q=>q.id>=10055);
  expect(items).toHaveLength(12);
  let seed=7123;const rand=n=>{seed=(seed*16807)%2147483647;return seed%n;};
  const add=(id,input,output)=>items.find(q=>q.id===id).testCases.push({input:JSON.stringify(input),expectedOutput:JSON.stringify(output)});
  for(let run=0;run<35;run++){
    const a=Array.from({length:rand(12)},()=>rand(21)-10),b=Array.from({length:rand(8)},()=>rand(21)-10);
    add(10055,a,a.slice().reverse());
    if(a.length){const n=1+rand(a.length);add(10056,{values:a,n},a.filter((_,i)=>i!==a.length-n));}
    const pos=a.length?rand(a.length+1)-1:-1;add(10057,{values:a,pos},pos);
    add(10058,[a.slice().sort((x,y)=>x-y),b.slice().sort((x,y)=>x-y)],a.concat(b).sort((x,y)=>x-y));
    const streams=[a.slice().sort((x,y)=>x-y),[],b.slice().sort((x,y)=>x-y)];add(10059,streams,a.concat(b).sort((x,y)=>x-y));
    const medians=a.map((_,i)=>{const sorted=a.slice(0,i+1).sort((x,y)=>x-y);return i%2?(sorted[i/2-.5]+sorted[i/2+.5])/2:sorted[i/2];});add(10060,a,medians);
    const values=a.map(x=>Math.abs(x)),sum=values.reduce((n,x)=>n+x,0);let possible=false;
    for(let mask=0;mask<(1<<values.length);mask++){let subtotal=0;values.forEach((x,i)=>{if(mask&(1<<i))subtotal+=x;});if(subtotal*2===sum){possible=true;break;}}add(10061,values,possible);
    const text=Array.from({length:rand(14)},()=>'abc'[rand(3)]).join('');let best='';
    for(let i=0;i<text.length;i++)for(let end=i+1;end<=text.length;end++){const piece=text.slice(i,end);if(piece===piece.split('').reverse().join('')&&piece.length>best.length)best=piece;}add(10064,text,best);
    const tree=Array.from({length:1+rand(15)},(_,i)=>i),p=rand(tree.length),q=rand(tree.length),ancestors=new Set();let node=p;
    while(node>=0){ancestors.add(node);node=Math.floor((node-1)/2);}node=q;while(!ancestors.has(node))node=Math.floor((node-1)/2);add(10062,{tree,p,q},node);
    let diameter=0;for(let i=0;i<tree.length;i++)for(let j=0;j<tree.length;j++){let x=i,y=j,d=0;while(x!==y){if(x>y)x=Math.floor((x-1)/2);else y=Math.floor((y-1)/2);d++;}diameter=Math.max(diameter,d);}add(10063,tree,diameter);
    const n=rand(5),edges=[];for(let u=0;u<n;u++)for(let v=0;v<n;v++)if(rand(6)===0)edges.push([u,v]);
    function permutations(a){if(!a.length)return [[]];return a.flatMap((x,i)=>permutations(a.filter((_,j)=>j!==i)).map(t=>[x,...t]));}
    const order=permutations(Array.from({length:n},(_,i)=>i)).find(order=>edges.every(([u,v])=>order.indexOf(u)<order.indexOf(v)))||[];add(10065,{n,edges},order);
    const weighted=edges.slice(0,7).map(([u,v])=>[u,v,rand(11)-5]);
    const components=es=>{let groups=Array.from({length:n},(_,i)=>i);for(const[u,v]of es){let from=groups[v],to=groups[u];groups=groups.map(x=>x===from?to:x);}return new Set(groups).size;};
    const target=components(weighted);let weight=Infinity;
    for(let mask=0;mask<(1<<weighted.length);mask++){const subset=weighted.filter((_,i)=>mask&(1<<i));if(subset.length===n-target&&components(subset)===target)weight=Math.min(weight,subset.reduce((sum,e)=>sum+e[2],0));}
    add(10066,{n,edges:weighted},weight);
  }
  for(const q of items)for(const c of q.testCases){let output;new Function('readline','console',q.referenceCode.javascript)(()=>c.input,{log:x=>output=x});expect(JSON.parse(output),q.title+' '+c.input).toEqual(JSON.parse(c.expectedOutput));}
  const result=execFileSync('python',['tests/verify_python_references.py'],{input:JSON.stringify(items),encoding:'utf8',maxBuffer:8*1024*1024});expect(result).toContain('All Python reference cases passed');
});

test('rapid question changes preserve language, drafts, custom cases and review marks',async({page})=>{
  await codingRound(page,[10055,10056,10057]);
  await page.evaluate(()=>{Editor.changeLang('javascript');Editor.instance.setValue('// first draft');TestPanel.cases=[{input:'[9]',expected:'[9]'}];CodingReview.mark();Exam.goto(1);Editor.changeLang('python');Editor.instance.setValue('# second draft');Exam.goto(0);Exam.goto(1);Exam.goto(0);});
  await expect(page.locator('#monaco-container .local-code-input')).toHaveValue('// first draft');
  await expect(page.locator('#lang-select')).toHaveValue('javascript');
  await expect(page.locator('#case-input')).toHaveValue('[9]');
  await expect(page.locator('#exam-nav .qdot').first()).toHaveClass(/review/);
  const deadline=await page.evaluate(()=>Exam.deadline);
  await page.getByRole('button',{name:'Save & leave',exact:true}).click();
  await page.reload();await page.locator('.mode-btn[data-mode="exam"]').click();
  await page.getByRole('button',{name:'Resume coding round',exact:true}).click();
  await expect(page.locator('#monaco-container .local-code-input')).toHaveValue('// first draft');
  expect(await page.evaluate(()=>Exam.deadline)).toBe(deadline);
  await expect(page.locator('#exam-nav .qdot').first()).toHaveClass(/review/);
  await page.evaluate(()=>Exam.goto(1));await expect(page.locator('#monaco-container .local-code-input')).toHaveValue('# second draft');
  await expect(page.locator('#lang-select')).toHaveValue('python');
});

test('partial coding feedback, submitted code and portable progress history survive reload',async({page})=>{
  await codingRound(page);
  await page.evaluate(async()=>{Editor.changeLang('javascript');Editor.instance.setValue(Questions.byId(10055).referenceCode.javascript);Exam.goto(1);Editor.changeLang('javascript');Editor.instance.setValue('console.log("[]");');await Exam.submitExam(false);});
  await page.getByRole('button',{name:'Review coding feedback',exact:true}).click();
  await expect(page.getByRole('heading',{name:'Coding feedback test',exact:true})).toBeVisible();
  await expect(page.locator('.coding-review-card')).toHaveCount(2);
  const history=await page.evaluate(()=>Store.get('coding_history',[]));
  expect(history).toHaveLength(1);expect(history[0].status).toBe('complete');expect(history[0].finalScore).toBe(63);
  expect(history[0].rows[0].caseResults.every(c=>c.status==='Passed')).toBe(true);
  expect(history[0].rows[1].caseResults.filter(c=>c.status==='Wrong Answer')).toHaveLength(3);
  expect(history[0].submissions[10056].code).toBe('console.log("[]");');
  await page.reload();await page.evaluate(()=>CodingReview.history());await page.getByRole('button',{name:'Review round',exact:true}).click();
  await page.locator('.coding-review-card').nth(1).getByText('Your submitted code', {exact:false}).click();
  await expect(page.locator('.coding-review-card').nth(1)).toContainText('console.log("[]");');
  const exported=await page.evaluate(()=>{let value;window.download=(name,data)=>value=JSON.parse(data);DataIO.exportProgress();return value;});
  expect(exported.coding_history[0].submissions[10056].code).toBe('console.log("[]");');
  await page.setViewportSize({width:390,height:844});expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
});

test('retrying unavailable evaluation updates the same history record without a false score',async({page})=>{
  await codingRound(page,[10055]);
  await page.evaluate(async()=>{Editor.changeLang('python');Editor.instance.setValue('print([])');await Exam.submitExam(false);});
  const first=await page.evaluate(()=>Store.get('coding_history',[])[0]);expect(first.status).toBe('incomplete');expect(first.finalScore).toBeNull();
  expect(first.rows[0].caseResults[0].status).toBe('Not evaluated');
  await page.evaluate(async()=>{const s=Store.get('coding_session');s.codes[10055]={lang:'javascript',code:Questions.byId(10055).referenceCode.javascript,cases:[]};Store.set('coding_session',s);Academy.retryCodingEvaluation();});
  await expect.poll(()=>page.evaluate(()=>Store.get('coding_history',[])[0].status)).toBe('complete');
  const result=await page.evaluate(()=>Store.get('coding_history',[]));expect(result).toHaveLength(1);expect(result[0].id).toBe(first.id);expect(result[0].finalScore).toBe(100);
  expect(await page.evaluate(()=>Store.get('coding_session',null))).toBeNull();
});

test('runtime failures retain unrun cases and evaluation locks the local editor',async({page})=>{
  await codingRound(page,[10055]);
  await page.evaluate(()=>{const exec=Runner.execOne.bind(Runner),gate=new Promise(resolve=>window.releaseEvaluation=resolve);Runner.execOne=async(...args)=>{await gate;return exec(...args);};Editor.changeLang('javascript');Editor.instance.setValue('throw Error("intentional failure");');window.evaluationPromise=Exam.submitExam(false);});
  const area=page.locator('#monaco-container .local-code-input'),before=await area.inputValue();
  await expect(area).not.toBeEditable();await area.focus();await page.keyboard.press('Enter');await page.keyboard.press('Tab');expect(await area.inputValue()).toBe(before);
  await page.evaluate(()=>window.releaseEvaluation());
  await page.evaluate(()=>window.evaluationPromise);
  const result=await page.evaluate(()=>Store.get('coding_history',[])[0]);expect(result.rows[0].caseResults[0].status).toBe('Runtime Error');expect(result.rows[0].caseResults.slice(1).every(c=>c.status==='Not run')).toBe(true);
  expect(await page.evaluate(()=>Progress.isSolved(10055))).toBe(false);
  expect(await page.evaluate(()=>Editor.instance.area.readOnly)).toBe(false);
});

test('contest save/resume retains its deadline and leaderboard completion',async({page})=>{
  await page.goto('/');await page.evaluate(()=>{App.mode='exam';Contest.start(CONTESTS[0].id);Editor.instance.setValue('');});
  const data=await page.evaluate(()=>({id:Exam._contestId,deadline:Exam.deadline}));
  await page.evaluate(()=>CodingReview.leave());await page.reload();await page.evaluate(()=>Academy.resumeCoding());
  expect(await page.evaluate(()=>({id:Exam._contestId,deadline:Exam.deadline,active:Contest.active}))).toEqual({...data,active:true});
  await page.evaluate(async()=>{for(const id of Exam.qids)Exam.codes[id]={lang:'javascript',code:'',cases:[]};Editor.instance.setValue('');await Contest.finish(false);});
  expect(await page.evaluate(id=>Store.get('contest_leaderboard',{})[id].score,data.id)).toBe(0);
  expect(await page.evaluate(()=>Store.get('coding_history',[]).length)).toBe(1);
});

test('mobile coding keeps the clock visible and test inputs above the fixed exam controls',async({page})=>{
  await page.setViewportSize({width:390,height:844});await codingRound(page,[10055,10056,10057]);
  await expect(page.locator('#timer')).toBeVisible();
  await expect.poll(()=>page.evaluate(()=>document.getElementById('view-problem').getBoundingClientRect().bottom<=document.getElementById('exam-nav').getBoundingClientRect().top+1)).toBe(true);
  const editor=page.locator('#monaco-container .local-code-input');expect((await editor.boundingBox()).height).toBeGreaterThan(250);
  const input=page.locator('#case-input');await input.scrollIntoViewIfNeeded();await input.fill('[7,8]');
  const position=await input.boundingBox(),nav=await page.locator('#exam-nav').boundingBox();expect(position.y+position.height).toBeLessThanOrEqual(nav.y+1);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
});
