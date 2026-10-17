const {test,expect}=require('@playwright/test');
const fs=require('node:fs'),vm=require('node:vm');
const {execFileSync}=require('node:child_process');

test('18 advanced algorithms agree with independent small-input exhaustive oracles in Python and JavaScript',()=>{
  const box={};box.window=box;
  for(const file of ['coding-data','advanced-coding'])vm.runInNewContext(fs.readFileSync(`assets/${file}.js`,'utf8'),box);
  const tasks=box.CODELAB_CODING.filter(q=>q.id>=10067);expect(tasks).toHaveLength(18);
  const add=(id,input,expected)=>tasks.find(q=>q.id===id).testCases.push({input:JSON.stringify(input),expectedOutput:JSON.stringify(expected)});
  let seed=101;const rand=n=>(seed=seed*16807%2147483647)%n;
  const perms=a=>a.length?a.flatMap((x,i)=>perms(a.filter((_,j)=>i!==j)).map(p=>[x,...p])):[[]];
  const reach=(n,edges)=>Array.from({length:n},(_,s)=>{const seen=new Set([s]),queue=[s];for(const u of queue)for(const [a,b]of edges)if(a===u&&!seen.has(b)){seen.add(b);queue.push(b);}return seen;});
  const components=(n,edges)=>{const r=reach(n,edges.flatMap(([a,b])=>[[a,b],[b,a]]));return new Set(r.map(s=>Math.min(...s))).size;};
  for(let run=0;run<25;run++){
    const nums=Array.from({length:rand(9)},()=>rand(11)-5);
    let inv=0;for(let i=0;i<nums.length;i++)for(let j=i+1;j<nums.length;j++)if(nums[i]>nums[j])inv++;add(10067,nums,inv);
    const text=Array.from({length:rand(12)},()=>'abc'[rand(3)]).join(''),pattern=Array.from({length:rand(5)},()=>'abc'[rand(3)]).join('');
    add(10068,{text,pattern},Array.from({length:text.length+1},(_,i)=>i).filter(i=>text.slice(i,i+pattern.length)===pattern));
    const n=1+rand(5),edges=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rand(3)===0)edges.push([u,v,rand(9)-4]);
    // Enumerate every path in a DAG; no relaxation algorithm is used as the oracle.
    const matrix=Array.from({length:n},(_,source)=>{const dist=Array(n).fill(null);function paths(u,cost){if(dist[u]===null||cost<dist[u])dist[u]=cost;for(const[a,b,w]of edges)if(a===u)paths(b,cost+w);}paths(source,0);return dist;});
    const source=rand(n);add(10069,{n,edges,source},{distances:matrix[source],negativeCycle:false});add(10070,{n,edges},matrix);
    const directed=[];for(let u=0;u<n;u++)for(let v=0;v<n;v++)if(rand(4)===0)directed.push([u,v]);
    const r=reach(n,directed),used=new Set(),parts=[];for(let u=0;u<n;u++)if(!used.has(u)){const part=Array.from({length:n},(_,v)=>v).filter(v=>r[u].has(v)&&r[v].has(u));part.forEach(v=>used.add(v));parts.push(part);}add(10071,{n,edges:directed},parts);
    const undirected=directed.slice(0,8),before=components(n,undirected);
    const bridges=undirected.filter((e,i)=>components(n,undirected.filter((_,j)=>j!==i))>before).map(([u,v])=>[Math.min(u,v),Math.max(u,v)]).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);add(10072,{n,edges:undirected},bridges);
    const a=nums.length?nums:[0],minimum=[],sums=[],minOps=[],sumOps=[],minArray=a.slice(),sumArray=a.slice();
    for(let i=0;i<12;i++){const index=rand(a.length),value=rand(11)-5,l=rand(a.length),right=l+rand(a.length-l);if(i%2){minOps.push(['set',index,value]);minArray[index]=value;sumOps.push(['add',index,value]);sumArray[index]+=value;}else{minOps.push(['min',l,right]);minimum.push(Math.min(...minArray.slice(l,right+1)));sumOps.push(['sum',l,right]);sums.push(sumArray.slice(l,right+1).reduce((x,y)=>x+y,0));}}
    add(10073,{nums:a,ops:minOps},minimum);add(10074,{nums:a,ops:sumOps},sums);
    const positive=nums.map(Math.abs),k=rand(8);let matches=0;for(let i=0;i<positive.length;i++){let xor=0;for(let j=i;j<positive.length;j++){xor^=positive[j];if(xor===k)matches++;}}add(10075,{nums:positive,k},matches);
    const dims=Array.from({length:2+rand(5)},()=>1+rand(8));function chain(l,right){if(l===right)return 0;let best=Infinity;for(let split=l;split<right;split++)best=Math.min(best,chain(l,split)+chain(split+1,right)+dims[l]*dims[split+1]*dims[right+1]);return best;}add(10076,dims,chain(0,dims.length-2));
    const balloons=positive.slice(0,6);function burst(a){if(!a.length)return 0;return Math.max(...a.map((x,i)=>(a[i-1]??1)*x*(a[i+1]??1)+burst(a.filter((_,j)=>i!==j))));}add(10077,balloons,burst(balloons));
    function pieces(s){if(!s.length)return 0;let best=Infinity;for(let i=1;i<=s.length;i++){const part=s.slice(0,i);if(part===part.split('').reverse().join(''))best=Math.min(best,1+pieces(s.slice(i)));}return best;}add(10078,text,text.length?pieces(text)-1:0);
    const jobs=Array.from({length:rand(8)},()=>{const start=rand(8);return [start,start+1+rand(5),rand(13)-3];});let profit=0;
    for(let mask=0;mask<(1<<jobs.length);mask++){const selected=jobs.filter((_,i)=>mask&(1<<i));if(selected.every((a,i)=>selected.every((b,j)=>i===j||a[1]<=b[0]||b[1]<=a[0])))profit=Math.max(profit,selected.reduce((n,j)=>n+j[2],0));}add(10079,jobs,profit);
    const words=['aa','ab','ba','bb'].filter(()=>rand(2)),begin='aa',end='bb',queue=[[begin,1]],seen=new Set([begin]);let length=0;for(const [word,d]of queue){if(word===end){length=d;break;}for(const next of words)if(!seen.has(next)&&[...word].filter((c,i)=>c!==next[i]).length===1){seen.add(next);queue.push([next,d+1]);}}add(10080,{begin,end,words},length);
    const alien=Array.from({length:rand(6)},()=>Array.from({length:1+rand(3)},()=>'abc'[rand(3)]).join('')),alphabet=[...new Set(alien.join(''))].sort();
    const valid=perms(alphabet).find(order=>alien.every((word,i)=>{if(!i)return true;const prior=alien[i-1];let j=0;while(j<Math.min(prior.length,word.length)&&prior[j]===word[j])j++;return j===Math.min(prior.length,word.length)?prior.length<=word.length:order.indexOf(prior[j])<order.indexOf(word[j]);}));add(10081,alien,valid?valid.join(''):null);
    const left=rand(5),right=rand(5),pairs=[];for(let u=0;u<left;u++)for(let v=0;v<right;v++)if(rand(2))pairs.push([u,v]);
    function matching(u,used){if(u===left)return 0;let best=matching(u+1,used);for(const[a,b]of pairs)if(a===u&&!used.has(b))best=Math.max(best,1+matching(u+1,new Set([...used,b])));return best;}add(10082,{left,right,edges:pairs},matching(0,new Set()));
    const parents=Array.from({length:n},(_,i)=>i?rand(i+1)-1:-1),queries=Array.from({length:10},()=>[rand(n),rand(n+3)]);add(10083,{parents,queries},queries.map(([u,k])=>{while(k--&&u>=0)u=parents[u];return u;}));
    const bound=rand(500);add(10084,bound,Array.from({length:bound+1},(_,i)=>String(i)).filter(s=>[...s].every((c,i)=>!i||c!==s[i-1])).length);
  }
  for(const q of tasks)for(const c of q.testCases){let out;new Function('readline','console',q.referenceCode.javascript)(()=>c.input,{log:value=>out=value});expect(JSON.parse(out),q.title+' '+c.input).toEqual(JSON.parse(c.expectedOutput));}
  expect(execFileSync('python',['tests/verify_python_references.py'],{input:JSON.stringify(tasks),encoding:'utf8',maxBuffer:8*1024*1024})).toContain('All Python reference cases passed');
});
