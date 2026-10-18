<#
.SYNOPSIS
Start this StudyLab folder and open it in Vivaldi. No internet or npm needed.
.EXAMPLE
.\Start-CodeLab-Vivaldi.ps1
.EXAMPLE
.\Start-CodeLab-Vivaldi.ps1 -LiveServer
.EXAMPLE
.\Start-CodeLab-Vivaldi.ps1 -Stop
#>
[CmdletBinding()]
param(
    [ValidateRange(1024,65525)][int]$Port = 4173,
    [string]$VivaldiPath,
    [switch]$LiveServer,
    [switch]$NoBrowser,
    [switch]$Stop
)

$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath($PSScriptRoot)
$launcherPath = Join-Path $projectRoot 'Start-CodeLab.py'
$statePath = Join-Path $projectRoot '.codelab-server.json'

function Get-CodeLabHealth([string]$Address) {
    try {
        $health = Invoke-RestMethod -Uri ($Address.TrimEnd('/') + '/__codelab__/health') -TimeoutSec 2
        if ($health.app -eq 'CodeLab' -and [string]::Equals([IO.Path]::GetFullPath($health.root), $projectRoot, [StringComparison]::OrdinalIgnoreCase)) { return $health }
    } catch { }
    return $null
}

function Find-Vivaldi {
    $candidates = @()
    if ($VivaldiPath) { $candidates += $VivaldiPath }
    if ($env:LOCALAPPDATA) { $candidates += Join-Path $env:LOCALAPPDATA 'Vivaldi\Application\vivaldi.exe' }
    if ($env:ProgramFiles) { $candidates += Join-Path $env:ProgramFiles 'Vivaldi\Application\vivaldi.exe' }
    if (${env:ProgramFiles(x86)}) { $candidates += Join-Path ${env:ProgramFiles(x86)} 'Vivaldi\Application\vivaldi.exe' }
    $command = Get-Command vivaldi.exe -ErrorAction SilentlyContinue
    if ($command) { $candidates += $command.Source }
    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate -PathType Leaf) { return [IO.Path]::GetFullPath($candidate) }
    }
    throw 'Vivaldi was not found. Use -VivaldiPath "C:\path\to\vivaldi.exe".'
}

if ($Stop) {
    if (-not (Test-Path -LiteralPath $statePath)) { Write-Host 'No launcher-managed StudyLab server is recorded.'; return }
    $saved = Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
    $health = Get-CodeLabHealth $saved.url
    if (-not $health) { throw 'The recorded server could not be verified. No process was stopped.' }
    $process = Get-CimInstance Win32_Process -Filter ('ProcessId=' + [int]$health.pid)
    if ($health.pid -ne $saved.pid -or -not $process -or $process.CommandLine.IndexOf($launcherPath, [StringComparison]::OrdinalIgnoreCase) -lt 0) {
        throw 'The process does not match this folder launcher. No process was stopped.'
    }
    Stop-Process -Id $health.pid -ErrorAction Stop
    Remove-Item -LiteralPath $statePath
    Write-Host 'StudyLab background server stopped. Vivaldi remains open.'
    return
}

if (-not (Test-Path -LiteralPath (Join-Path $projectRoot 'index.html'))) { throw 'Keep this script in the StudyLab folder beside index.html.' }
if (-not $NoBrowser) { $browserPath = Find-Vivaldi }

if ($LiveServer) {
    if (-not $PSBoundParameters.ContainsKey('Port')) { $Port = 5500 }
    $url = 'http://127.0.0.1:' + $Port + '/'
    try {
        $response = Invoke-WebRequest -Uri ($url + 'assets/runtime-manifest.js') -UseBasicParsing -TimeoutSec 3
        if ($response.StatusCode -ne 200 -or -not $response.Content.StartsWith('window.CODELAB_RUNTIME=')) { throw 'Not StudyLab' }
    } catch { throw 'Start index.html with VS Code Live Server first, then retry -LiveServer (default port 5500).' }
} else {
    $url = $null
    if (Test-Path -LiteralPath $statePath) {
        try { $saved = Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json; if (Get-CodeLabHealth $saved.url) { $url = [string]$saved.url } } catch { }
    }
    if (-not $url) {
        $requested = 'http://127.0.0.1:' + $Port + '/'
        $health = Get-CodeLabHealth $requested
        if ($health) { $url = $requested }
    }
    if (-not $url) {
        $pythonCommand = Get-Command py.exe -ErrorAction SilentlyContinue
        $pythonArguments = @('-3')
        if (-not $pythonCommand) { $pythonCommand = Get-Command python.exe -ErrorAction SilentlyContinue; $pythonArguments = @() }
        if (-not $pythonCommand) { throw 'Python 3 is required for this launcher. You can also use VS Code Live Server.' }
        $selectedPort = $null
        foreach ($candidatePort in $Port..($Port + 10)) {
            $listener = $null
            try { $listener = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, $candidatePort); $listener.Start(); $selectedPort = $candidatePort; break }
            catch { }
            finally { if ($listener) { $listener.Stop() } }
        }
        if (-not $selectedPort) { throw 'No free local port was found. Retry with -Port 6000.' }
        $url = 'http://127.0.0.1:' + $selectedPort + '/'
        $pythonArguments += @('-u', ('"' + $launcherPath + '"'), '--no-browser', '--strict-port', '--port', [string]$selectedPort, '--log-dir', ('"' + $projectRoot + '"'))
        $literalWorkingDirectory = [System.Management.Automation.WildcardPattern]::Escape($projectRoot)
        $server = Start-Process -FilePath $pythonCommand.Source -ArgumentList $pythonArguments -WorkingDirectory $literalWorkingDirectory -WindowStyle Hidden -PassThru
        $health = $null
        for ($attempt = 0; $attempt -lt 40; $attempt++) {
            $health = Get-CodeLabHealth $url
            if ($health) { break }
            $server.Refresh()
            if ($server.HasExited) { throw 'Local server failed. See .codelab-server.stderr.log in this folder.' }
            Start-Sleep -Milliseconds 150
        }
        if (-not $health) { throw 'Local server did not become ready. See .codelab-server.stderr.log.' }
        @{ url = $url; pid = [int]$health.pid; root = $projectRoot } | ConvertTo-Json | Set-Content -LiteralPath $statePath -Encoding UTF8
    }
    Write-Host 'Background server ready. Close this terminal if you like; the server keeps running.'
    Write-Host 'Stop later with: .\Start-CodeLab-Vivaldi.ps1 -Stop'
}

if (-not $NoBrowser) {
    Start-Process -FilePath $browserPath -ArgumentList ($url + 'index.html')
    Write-Host 'Opened StudyLab in Vivaldi.'
}
Write-Host ('StudyLab URL: ' + $url)
