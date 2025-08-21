@echo off
echo ========================================
echo DDoS AI Detection System - Demo Deploy
echo ========================================
echo.

echo [1/3] Adding all changes to Git...
git add .

echo [2/3] Committing changes...
git commit -m "Add interactive demo features: collapsible sidebar, fake data, clickable elements, charts"

echo [3/3] Pushing to GitHub...
git push origin master

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Now run: fly deploy
echo.
echo Your demo will have:
echo - Collapsible sidebar (click the bars icon)
echo - Interactive model performance charts
echo - Clickable dataset analysis
echo - Live traffic monitoring with fake data
echo - Real-time updates every 8 seconds
echo - Search, export, and delete functionality
echo.
pause
