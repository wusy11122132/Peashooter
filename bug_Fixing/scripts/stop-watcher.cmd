@echo off
chcp 65001 >nul
set "TASK_NAME=Codex BugMail Watcher"

schtasks.exe /Change /TN "%TASK_NAME%" /DISABLE >nul
if errorlevel 1 (
    echo 关闭失败：找不到任务或当前用户没有操作权限。
    pause
    exit /b 1
)

schtasks.exe /End /TN "%TASK_NAME%" >nul 2>&1
echo 已关闭内网报错邮件定时检查。
echo 邮件时间游标已保留，下次开启后将从原时间点继续。
pause

