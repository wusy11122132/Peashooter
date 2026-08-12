@echo off
chcp 65001 >nul
set "TASK_NAME=Codex BugMail Watcher"

schtasks.exe /Change /TN "%TASK_NAME%" /ENABLE >nul
if errorlevel 1 (
    echo 启动失败：找不到任务或当前用户没有操作权限。
    echo 可先运行 scripts\install-task.ps1 安装任务。
    pause
    exit /b 1
)

echo 已开启内网报错邮件定时检查。
echo 系统将按既定的 1 分钟周期执行，历史邮件时间游标不会重置。
schtasks.exe /Query /TN "%TASK_NAME%" /FO LIST | findstr /I /C:"Status:" /C:"状态:" /C:"Next Run Time:" /C:"下次运行时间:"
pause
