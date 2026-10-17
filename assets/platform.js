'use strict';
const RuntimeAssets={
  scripts:new Map(),
  base(kind){
    if(location.protocol!=='file:'&&!window.CODELAB_STANDALONE)return new URL('vendor/runtimes/'+kind+'/',document.baseURI).href;
    return {python:'https://cdn.jsdelivr.net/pyodide/v0.26.2/full/',sql:'https://cdn.jsdelivr.net/npm/sql.js@1.14.0/dist/',monaco:'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/'}[kind];
  },
  script(url){if(!this.scripts.has(url))this.scripts.set(url,new Promise((resolve,reject)=>{const script=document.createElement('script');script.src=url;script.onload=resolve;script.onerror=()=>{this.scripts.delete(url);reject(new Error('Could not load runtime: '+url));};document.head.append(script);}));return this.scripts.get(url);},
  allFiles(){return [...new Set(['./',...CODELAB_RUNTIME.shell,...OfflineLibrary.catalog.files,...CODELAB_RUNTIME.files.map(f=>f.path)])];},
  async saved(){
    if(window.CODELAB_STANDALONE)return 'portable';
    if(location.protocol==='file:')return 'folder';
    if(!('caches' in window))return 'unsupported';
    const name=OfflineLibrary.cacheName();
    if(!(await caches.has(name)))return 'missing';
    const cache=await caches.open(name),keys=new Set((await cache.keys()).map(r=>r.url));
    return this.allFiles().every(f=>keys.has(new URL(f,document.baseURI).href))?'ready':'partial';
  }
};

// Python executes in a stoppable worker and reads both input() and sys.stdin normally.
Object.assign(Py,{
  worker:null,pending:null,sequence:0,
  status(text,ready=false){document.getElementById('py-label').textContent=text;document.getElementById('py-dot').className='dot'+(ready?' ready':'');},
  load(){
    if(this.ready)return Promise.resolve();if(this.loading)return this.loadPromise;
    this.loading=true;this.status('Python loading…');
    this.loadPromise=new Promise((resolve,reject)=>{
      let url;
      try{url=window.CODELAB_PYTHON_WORKER_SOURCE?URL.createObjectURL(new Blob([CODELAB_PYTHON_WORKER_SOURCE],{type:'text/javascript'})):new URL('assets/python-worker.js',document.baseURI).href;this.worker=new Worker(url);}catch(error){this.loading=false;this.status('Python needs localhost / installed app');reject(error);return;}
      const worker=this.worker;
      const timeout=setTimeout(()=>{if(this.worker===worker){worker.terminate();this.worker=null;this.loading=false;this.status('Python unavailable · retry');reject(new Error('Python loading timed out.'));}},45000);
      const finish=()=>{clearTimeout(timeout);if(url.startsWith('blob:'))URL.revokeObjectURL(url);};
      worker.onmessage=({data})=>{
        if(this.worker!==worker)return;
        if(data.type==='ready'){finish();this.loading=false;this.ready=true;this.status('Python ready',true);resolve();}
        else if(data.type==='init-error'){finish();worker.terminate();this.worker=null;this.loading=false;this.ready=false;this.status('Python unavailable · retry');reject(new Error(data.error));}
        else if(data.type==='result'&&this.pending?.id===data.id){const job=this.pending;this.pending=null;clearTimeout(job.timer);job.resolve({stdout:data.stdout,stderr:data.stderr});}
      };
      worker.onerror=event=>{event.preventDefault();finish();this.stop(new Error(event.message||'Python worker failed.'));reject(new Error(event.message||'Python worker failed.'));};
      worker.postMessage({type:'init',base:RuntimeAssets.base('python')});
    });
    // Background startup must not create an unhandled rejection; explicit callers still receive it.
    this.loadPromise.catch(()=>{});return this.loadPromise;
  },
  run(code,stdin,timeoutMs){
    if(!this.ready)return Promise.reject({kind:'notready'});
    if(this.pending)return Promise.reject(new Error('Python is already running. Wait or use Stop run.'));
    return new Promise((resolve,reject)=>{
      const id=++this.sequence,timer=setTimeout(()=>{this.stop({kind:'tle'});if(!window.CODELAB_DISABLE_PYTHON)this.load();},timeoutMs);
      this.pending={id,timer,resolve,reject};this.worker.postMessage({type:'run',id,code,stdin});
    });
  },
  stop(error=new Error('Execution stopped by you.')){this.worker?.terminate();this.worker=null;this.ready=false;this.loading=false;if(this.pending){clearTimeout(this.pending.timer);this.pending.reject(error);this.pending=null;}this.status('Python stopped · reload engine');}
});
SqlRun.load=function(){
  if(this.ready)return Promise.resolve();if(this.loading)return this.loadPromise;this.loading=true;
  this.loadPromise=(async()=>{try{const base=RuntimeAssets.base('sql');if(typeof initSqlJs==='undefined')await RuntimeAssets.script(base+'sql-wasm.js');this.SQL=await initSqlJs({locateFile:file=>base+file});this.ready=true;}finally{this.loading=false;}})();return this.loadPromise;
};

const OfflineAccess={
  installEvent:null,
  init(){
    const button=document.createElement('button');button.className='nav-link offline-access';button.textContent='Online / Offline';button.onclick=()=>this.open();document.querySelector('.nav-left').append(button);
    const modal=document.createElement('div');modal.className='modal-overlay';modal.id='modal-offline-access';document.body.append(modal);
    window.addEventListener('online',()=>this.refresh());window.addEventListener('offline',()=>this.refresh());
    window.addEventListener('beforeinstallprompt',event=>{event.preventDefault();this.installEvent=event;this.refresh();});
    window.addEventListener('appinstalled',()=>{this.installEvent=null;this.refresh();});
  },
  async open(){
    UI.close();const h=Academy.h.bind(Academy),portable=!!window.CODELAB_STANDALONE,file=location.protocol==='file:';
    const size=(CODELAB_RUNTIME.bytes/1048576).toFixed(1);
    document.getElementById('modal-offline-access').innerHTML=`<div class="modal offline-access-modal" role="dialog" aria-modal="true" aria-labelledby="offline-access-title"><div class="modal-head"><h2 id="offline-access-title">Use CodeLab online &amp; offline</h2><button class="x-close" aria-label="Close offline access" onclick="UI.close()">×</button></div><div class="modal-body"><p id="connection-state" class="academy-note" role="status"></p><h3>1. Online website</h3><p>Use the same editor, exams and library on your GitHub Pages website. Progress stays in this browser. Export progress to move it to another device or edition.</p><h3>2. Save this website for offline use</h3><p>While connected, save the full app, questions, library, diagrams and the bundled Python, SQL and Monaco engines (${size} MiB of runtime files). Wait for Ready offline before disconnecting.</p><div class="academy-actions"><button class="btn-primary" onclick="OfflineAccess.save()" ${file||portable?'disabled':''}>Save full app for offline</button><button class="btn-ghost" id="install-codelab" onclick="OfflineAccess.install()">Install app</button></div><p id="offline-save-status" class="lib-status" role="status"></p><h3>3. Download &amp; keep a copy</h3>${portable?'<p>This single HTML already contains the reading library, questions and local text editor. JavaScript works offline. For offline Python/SQL and Monaco, use the full ZIP and its local launcher.</p>':`<div class="academy-actions"><a class="btn-ghost" href="downloads/CodeLab-Offline.zip" download>Download full offline ZIP</a><a class="btn-ghost" href="CodeLab-Offline.html" download>Download single HTML</a></div><p>Full ZIP: extract, then run <code>python Start-CodeLab.py</code> (Python 3 required on the computer). It opens a localhost server; no internet or npm is needed. Single HTML: double-click for MCQs, theory, reading and JavaScript.</p>`}<h3>Execution support</h3><p>Full saved app / local ZIP: Python standard library, JavaScript, HTML/CSS preview and SQL execute offline. C, C++ and Java use the existing online cloud compiler. Additional Python packages are not bundled.</p><div class="academy-actions"><button class="btn-ghost" onclick="DataIO.exportProgress()">Export all progress</button><button class="btn-ghost" onclick="DataIO.importProgress()">Import progress</button><button class="btn-ghost" onclick="Py.load()">Reload Python engine</button></div><p>Saved progress belongs to each browser and origin. Export before clearing browser data. Browser-managed offline files can be evicted; the ZIP provides a separate copy.</p><p id="offline-readiness" role="status">Checking saved files…</p></div><div class="modal-foot"><button class="btn-primary" onclick="UI.close()">Done</button></div></div>`;
    document.getElementById('modal-offline-access').classList.add('show');this.refresh();
    const state=await RuntimeAssets.saved();const status=document.getElementById('offline-readiness');if(status)status.textContent={ready:'Ready offline. Every required file for this version is saved.',partial:'Offline copy is incomplete. Save the full app while connected.',missing:'Full app is not saved on this browser yet.',portable:'Portable single-HTML reading edition.',folder:'Local folder: use Start-CodeLab.py for offline Python and SQL.',unsupported:'Offline installation needs HTTPS or localhost.'}[state];
  },
  refresh(){const status=document.getElementById('connection-state');if(status)status.textContent=(navigator.onLine?'Online':'Offline')+' · '+(window.CODELAB_STANDALONE?'Single HTML':location.protocol==='file:'?'Local folder':'Website / installed app');const install=document.getElementById('install-codelab');if(install){install.disabled=!this.installEvent;install.title=this.installEvent?'Install on this device':'Use your browser menu → Install app / Add to Home Screen when available.';}},
  async save(){await OfflineLibrary.saveOffline();const state=await RuntimeAssets.saved(),el=document.getElementById('offline-readiness');if(el)el.textContent=state==='ready'?'Ready offline. Every required file for this version is saved.':'Offline copy incomplete. Check the save message and retry.';},
  async install(){if(!this.installEvent)return;await this.installEvent.prompt();await this.installEvent.userChoice;this.installEvent=null;this.refresh();}
};
const platformCacheStatus=OfflineLibrary.cacheStatus.bind(OfflineLibrary);
OfflineLibrary.cacheStatus=function(message){platformCacheStatus(message);const el=document.getElementById('offline-save-status');if(el)el.textContent=message;};
window.addEventListener('DOMContentLoaded',()=>OfflineAccess.init());
