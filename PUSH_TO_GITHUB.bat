@echo off
cd /d "%~dp0"
echo ======================================================================
echo Pushing Astrological Project to GitHub (tejravisand/astrological)
echo ======================================================================
echo.
echo [Step 1 of 2] Pushing branch 'tejravi'...
git push -u origin tejravi
echo.
echo [Step 2 of 2] Pushing branch 'main'...
git push -u origin main
echo.
echo ======================================================================
echo If you saw a browser popup, make sure to click 'Authorize' to finish!
echo Verify your repository at: https://github.com/tejravisand/astrological
echo ======================================================================
echo.
pause
