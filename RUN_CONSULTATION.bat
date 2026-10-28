@echo off
chcp 65001 > nul
cls
echo ===============================================================================
echo        卐 VEDIC ^& SCIENTIFIC MULTI-METHOD ASTROLOGY PLATFORM 卐
echo   Interactive Consultation: Name, DOB, TOB, Place, Marital Status,
echo   Purpose, 3 Question Choices, Astrological Prediction ^& PDF Generation
echo ===============================================================================
echo.
echo   [1] Run Interactive Console Consultation (Step-by-Step Questions ^& PDF)
echo   [2] Launch Interactive Web Portal (Browser Interface at http://localhost:8080)
echo   [3] Exit
echo.
set /p choice="  Enter your choice [1, 2, or 3, default: 1]: "

if "%choice%"=="" set choice=1
if "%choice%"=="1" goto run_cli
if "%choice%"=="2" goto run_web
if "%choice%"=="3" goto end

:run_cli
echo.
echo Starting Interactive Consultation Wizard...
echo.
python run_consultation.py
pause
goto end

:run_web
echo.
echo Starting Astrological Web Consultation Portal on port 8080...
start "" "http://localhost:8080"
python qa_consultation_app.py --serve --port 8080
goto end

:end
