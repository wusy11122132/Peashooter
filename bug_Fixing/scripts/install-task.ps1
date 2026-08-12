param(
    [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'
$TaskName = 'Codex BugMail Watcher'
$CleanupTaskName = 'Codex BugMail Var Cleanup'

if ($Uninstall) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Unregister-ScheduledTask -TaskName $CleanupTaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Output "Removed scheduled task: $TaskName"
    Write-Output "Removed scheduled task: $CleanupTaskName"
    exit 0
}

$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root '.venv\Scripts\pythonw.exe'
if (-not (Test-Path -LiteralPath $Python)) {
    throw "Python environment not found: $Python"
}
$Action = New-ScheduledTaskAction -Execute $Python -Argument '-m bugmail run-once' -WorkingDirectory $Root
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 1) -RepetitionDuration (New-TimeSpan -Days 3650)
$CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$Principal = New-ScheduledTaskPrincipal -UserId $CurrentUser -LogonType Interactive -RunLevel Limited
$Settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 30)

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Force | Out-Null
Write-Output "Installed scheduled task: $TaskName (every 1 minute, interactive user only)"
$CleanupScript = Join-Path $PSScriptRoot 'cleanup-var.ps1'
$CleanupAction = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoLogo -NoProfile -NonInteractive -File `"$CleanupScript`""
$CleanupTrigger = New-ScheduledTaskTrigger -Daily -At (Get-Date).Date.AddMinutes(1)
$CleanupSettings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 10)
Register-ScheduledTask -TaskName $CleanupTaskName -Action $CleanupAction -Trigger $CleanupTrigger -Principal $Principal -Settings $CleanupSettings -Force | Out-Null
Write-Output "Installed scheduled task: $CleanupTaskName (daily, retains 3 days)"
