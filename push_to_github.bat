@echo off
echo ========================================
echo    YouTube Channel Downloader - GitHub Push Tool
echo ========================================
echo.

REM Check if GitHub username is provided
if "%1"=="" (
    echo Usage: push_to_github.bat YOUR_GITHUB_USERNAME
    echo Example: push_to_github.bat myusername
    pause
    exit /b 1
)

set GITHUB_USERNAME=%1
echo Pushing to GitHub user: %GITHUB_USERNAME%
echo.

REM Add remote repository
echo Step 1: Adding remote repository...
git remote add origin https://github.com/%GITHUB_USERNAME%/youtube-channel-downloader.git

if %errorlevel% neq 0 (
    echo Remote repository already exists or failed to add, trying to reset...
    git remote set-url origin https://github.com/%GITHUB_USERNAME%/youtube-channel-downloader.git
)

REM Push to GitHub
echo.
echo Step 2: Pushing to GitHub...
git push -u origin master

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    SUCCESS: Push completed!
    echo    Repository URL: https://github.com/%GITHUB_USERNAME%/youtube-channel-downloader
    echo ========================================
) else (
    echo.
    echo ========================================
    echo    ERROR: Push failed!
    echo    Please check:
    echo    1. GitHub username is correct
    echo    2. Network connection is working
    echo    3. GitHub access permissions
    echo ========================================
)

echo.
pause