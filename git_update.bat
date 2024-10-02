@echo off

REM Check if there are any changes
git diff --quiet && git diff --staged --quiet
IF %ERRORLEVEL% EQU 0 (
    echo No changes to commit
    exit /B 0
)

REM Stage all changes
git add -A

REM Commit with a default message
set commit_message=Auto-update: %date% %time:~0,8%
git commit -m "%commit_message%"

REM Push to the current branch
git push

REM Print success message
echo Changes pushed successfully!
