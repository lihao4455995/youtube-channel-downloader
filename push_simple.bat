@echo off
echo GitHub Push Helper
echo ==================
echo.

if "%1"=="" (
    echo Usage: push_simple.bat YOUR_GITHUB_USERNAME
    echo Example: push_simple.bat myusername
    pause
    exit /b 1
)

set USERNAME=%1
echo Setting up remote for user: %USERNAME%

git remote add origin https://github.com/%USERNAME%/youtube-channel-downloader.git 2>nul
if %errorlevel% neq 0 (
    echo Remote exists, updating URL...
    git remote set-url origin https://github.com/%USERNAME%/youtube-channel-downloader.git
)

echo.
echo Pushing to GitHub...
git push -u origin master

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! Repository pushed to:
    echo https://github.com/%USERNAME%/youtube-channel-downloader
) else (
    echo.
    echo ERROR! Push failed. Check:
    echo 1. Username is correct
    echo 2. GitHub repository exists
    echo 3. Authentication (use personal access token)
)

echo.
pause