@echo off
cd /d "%~dp0"
echo Opening Sandeep R Master Prediction PDF in Google Chrome...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" "http://localhost:8080/output/sandeep_r_master_prediction_dossier.pdf"
start "" "http://localhost:8080/output/sandeep_r_master_prediction_dossier.pdf"
exit
