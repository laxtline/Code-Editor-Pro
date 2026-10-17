# CodeLab - isi folder se online aur offline use

App, questions, diagrams, Python/SQL engines aur editor isi folder mein hain.
`assets/`, `vendor/` aur `offline/` ko saath rakho. Installed copy ko internet ki zarurat nahi hai for the supported offline features.

## Option 1: VS Code Live Server

1. VS Code mein **File > Open Folder** se poora `Code-Editor-Pro` folder kholo.
2. `index.html` par right-click > **Open with Live Server**.
3. Vivaldi mein `http://127.0.0.1:5500/index.html` kholo. Is computer ki project settings Vivaldi ke liye configured hain.
4. Ab internet disconnect karke practice kar sakte ho. VS Code aur Live Server running rehne chahiye.

Live Server already running ho aur Vivaldi kholna ho to isi folder ke PowerShell terminal mein:

```powershell
.\Start-CodeLab-Vivaldi.ps1 -LiveServer
```

Live Server alag port use kare to `-LiveServer -Port 5501` use karo.

## Option 2: PowerShell se direct Vivaldi

Is project folder ke terminal mein:

```powershell
.\Start-CodeLab-Vivaldi.ps1
```

Ya kisi bhi PowerShell folder se:

```powershell
& "D:\Coding\Code-Editor-Pro\Start-CodeLab-Vivaldi.ps1"
```

Script Vivaldi auto-detect karta hai aur localhost server background mein start karta hai.
Python 3 installed hona chahiye; npm/internet/VS Code ki zarurat nahi hai.
Terminal close kar sakte ho; server background mein running rahega.
Same launcher dobara run karne par existing verified server reuse hota hai.
Default port 4173 hai; busy hua to next available port use hota hai. Printed URL ko use karo.

Server band karne ke liye:

```powershell
.\Start-CodeLab-Vivaldi.ps1 -Stop
```

Vivaldi custom/portable location par ho to:

```powershell
.\Start-CodeLab-Vivaldi.ps1 -VivaldiPath "E:\Vivaldi\Application\vivaldi.exe"
```

Browser khole bina server start/check karna ho:

```powershell
.\Start-CodeLab-Vivaldi.ps1 -NoBrowser
```

## Offline mein kya chalega?

- Written tests, aptitude/reasoning/verbal questions, formulas, explanations aur exams.
- Complete bundled Offline Library, diagrams, solutions, notes aur drafts.
- JavaScript, Python ke bundled standard-library modules, SQLite SQL aur HTML/CSS preview.
- Monaco editor, local saving, reports aur Export/Import Progress.
- C/C++/Java cloud compilation aur external reference links ke liye internet chahiye.
- Extra Python packages bundled nahi hain.

`CodeLab-Offline.html` double-click se lightweight MCQ/theory/library/JavaScript edition khol sakte ho.
Full offline Python/SQL/editor ke liye Live Server ya launcher use karo.

## Progress aur backup

Progress browser aur address/port ke hisaab se save hota hai. Vivaldi aur doosre browsers ka progress alag hai.
`127.0.0.1:5500`, `127.0.0.1:4173`, `localhost` aur GitHub Pages alag storage origins hain.
Ek method se doosre par move karte waqt **Export all progress**, phir **Import progress** use karo.

## GitHub se online

GitHub Pages deployment ke baad online app bhi same features use karegi.
Deployment workflow `.github/workflows/pages.yml` aur instructions `README.md` mein hain.
Online version mein **Online / Offline > Save full app for offline** bhi available hai.
GitHub deployment ka status repository ke Actions tab mein check karo. Local use independent hai.
