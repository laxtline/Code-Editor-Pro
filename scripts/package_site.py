"""Build a whitelisted Pages artifact and a complete offline ZIP from already generated content."""
from pathlib import Path
import shutil
import zipfile

ROOT=Path(__file__).resolve().parents[1]
STATIC=['index.html','sw.js','manifest.webmanifest','CodeLab-Offline.html','Start-CodeLab.py','local_tools.py','Start-CodeLab.cmd','Start-CodeLab-Vivaldi.ps1','OFFLINE-START-HERE.md','README.md','.vscode/extensions.json','.vscode/tasks.json']

def build():
    target=(ROOT/'_site').resolve()
    if target.parent!=ROOT.resolve() or target.name!='_site':raise SystemExit('Invalid output directory')
    # This is exclusively generated output; never remove a source directory.
    if target.exists():shutil.rmtree(target)
    target.mkdir()
    files=[ROOT/name for name in STATIC]
    for folder in ('assets','vendor','offline'):
        files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file())
    for source in files:
        relative=source.relative_to(ROOT)
        if source.stat().st_size>=100_000_000:raise SystemExit('File exceeds GitHub single-file limit: '+str(relative))
        destination=target/relative;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,destination)
    (target/'.nojekyll').write_text('')
    guide=r'''StudyLab online and offline
==========================
Extract the whole ZIP first.
Windows: double-click Start-CodeLab.cmd.
Vivaldi: run .\Start-CodeLab-Vivaldi.ps1 in PowerShell.
VS Code: open this folder, then open index.html with Live Server.
Detailed steps: OFFLINE-START-HERE.md in this same folder.
Any system with Python 3: python Start-CodeLab.py
Keep the server window open while using the app. It binds to 127.0.0.1 only.
Python (standard library), JavaScript, HTML/CSS preview, SQLite, Monaco, MCQs,
theory and the entire study library work without internet through this local server.
C/C++/Java run offline through this launcher if GCC/Clang or a JDK is installed.
Live Server and hosted Pages use cloud compilation for those languages.
Extra Python packages and desktop sqlite3/GUI modules are not included in browser Python.
Open CodeLab-Offline.html directly for the lightweight reading/MCQ/JavaScript edition.
Progress saves immediately in this browser, online or offline. The launcher also writes
private .codelab-data/progress.json backups. Export/Import transfers between origins/devices.
On the hosted website, choose Online / Offline -> Save full app for offline.
Wait for Ready offline before disconnecting. Use the browser's Install app option if available.
Source and runtime license notices are included in offline/licenses and vendor.
'''
    (target/'README-OFFLINE.txt').write_text(guide,encoding='utf-8')
    downloads=ROOT/'downloads';downloads.mkdir(exist_ok=True)
    output=downloads/'CodeLab-Offline.zip'
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as archive:
        # Portable workspace defaults omit this computer's private Vivaldi installation path.
        archive.writestr('StudyLab/.vscode/settings.json','{"liveServer.settings.host":"127.0.0.1","liveServer.settings.port":5500,"liveServer.settings.root":"/","liveServer.settings.ignoreFiles":["**/.git/**","**/.codelab-data/**","**/.codelab-server*"]}\n')
        for path in sorted(target.rglob('*')):
            if path.is_file():archive.write(path,'StudyLab/'+path.relative_to(target).as_posix())
    (target/'downloads').mkdir();shutil.copy2(output,target/'downloads'/output.name)
    print(f'Pages artifact: {target} ({len(files)} files)')
    print(f'Complete offline ZIP: {output.stat().st_size/1048576:.2f} MiB')

if __name__=='__main__':build()
