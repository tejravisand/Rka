"""
Generate the Master Unified Consultation Dossier PDF for Ravi Kumar S and launch in Google Chrome.
"""
import os
import shutil
import subprocess
from datetime import datetime, timedelta
from app.core.kundali import calculate_kundali
from app.reports.master_pdf_generator import generate_master_astrological_dossier

client_name = "Ravi Kumar S"
birth_dt_local = datetime(1968, 11, 20, 3, 45, 0)
tz_offset = 5.5
dt_utc = birth_dt_local - timedelta(hours=tz_offset)
lat = 13.0068
lon = 77.5713
location = "KC General Hospital, Malleshwaram, Bengaluru, Karnataka, India"

print(f"Calculating Kundali for {client_name}...")
kundali = calculate_kundali(dt_utc, lat, lon, tz_offset)

output_pdf = os.path.abspath(os.path.join("output", "ravi_kumar_master_consultation_dossier.pdf"))

print(f"Generating Master Unified PDF Dossier at: {output_pdf}...")
generate_master_astrological_dossier(
    kundali=kundali,
    client_name=client_name,
    output_pdf_path=output_pdf,
    location_name=location
)

artifact_dir = os.environ.get("ANTIGRAVITY_ARTIFACT_DIR")
if artifact_dir and os.path.isdir(artifact_dir):
    shutil.copyfile(output_pdf, os.path.join(artifact_dir, "ravi_kumar_master_consultation_dossier.pdf"))

file_size = os.path.getsize(output_pdf)
print(f"SUCCESS: Master PDF generated! ({file_size} bytes)")
print(f"Output File: {output_pdf}")

# Launch in Chrome or default browser
chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
]
chrome_bin = next((p for p in chrome_paths if os.path.exists(p)), None)
if chrome_bin:
    print("Launching Google Chrome with Master PDF...")
    subprocess.Popen([chrome_bin, output_pdf])
    print("Opened in Google Chrome!")
else:
    import webbrowser
    webbrowser.open(output_pdf)
