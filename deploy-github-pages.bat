@echo off
REM FinSense GitHub Pages Deployment Script (Windows)
REM This script helps deploy the frontend to GitHub Pages

echo.
echo 🚀 FinSense GitHub Pages Deployment
echo ====================================
echo.

REM Check if we're in the right directory
if not exist "frontend" (
    echo ❌ Error: frontend directory not found!
    echo Please run this script from the project root directory.
    exit /b 1
)

REM Navigate to frontend
cd frontend

echo 📦 Installing dependencies...
call npm install

echo.
echo 🔨 Building for GitHub Pages...
set GITHUB_PAGES=true
call npm run build

echo.
echo 📤 Deploying to GitHub Pages...

REM Check if gh-pages is installed
npm list gh-pages >nul 2>&1
if errorlevel 1 (
    echo Installing gh-pages...
    call npm install --save-dev gh-pages
)

REM Deploy
call npx gh-pages -d dist

echo.
echo ✅ Deployment complete!
echo.
echo Your site will be available at:
echo https://rakshita-jaiswal.github.io/FinSense
echo.
echo Note: It may take a few minutes for GitHub Pages to update.
echo.
echo To enable GitHub Pages:
echo 1. Go to: https://github.com/rakshita-jaiswal/FinSense/settings/pages
echo 2. Under 'Source', select 'Deploy from a branch'
echo 3. Select branch 'gh-pages' and folder '/ (root)'
echo 4. Click 'Save'
echo.

pause