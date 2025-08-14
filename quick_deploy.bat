@echo off
echo ========================================
echo DDoS AI Detection System - Quick Deploy
echo ========================================
echo.

echo This script will help you prepare your project for deployment.
echo.

echo Step 1: Checking if Git is installed...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/
    pause
    exit /b 1
)
echo Git is installed ✓

echo.
echo Step 2: Initializing Git repository...
if not exist .git (
    git init
    echo Git repository initialized ✓
) else (
    echo Git repository already exists ✓
)

echo.
echo Step 3: Adding all files to Git...
git add .
echo Files added to Git ✓

echo.
echo Step 4: Creating initial commit...
git commit -m "Initial commit for deployment"
echo Initial commit created ✓

echo.
echo ========================================
echo READY FOR DEPLOYMENT!
echo ========================================
echo.
echo Next steps:
echo 1. Create a GitHub repository
echo 2. Push your code to GitHub
echo 3. Deploy on Render.com
echo.
echo See DEPLOYMENT_GUIDE.md for detailed instructions.
echo.
pause
