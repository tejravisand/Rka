"""
Runner script to generate the complete Astrological Consultation PDF for Sandeep R
and open in Google Chrome.
"""
import os
import shutil
import subprocess
from datetime import datetime, timedelta
from app.core.kundali import calculate_kundali
from app.engines.sandeep_consultation import SandeepConsultationEngine
from app.reports.sandeep_pdf_generator import generate_sandeep_pdf_report

client_name = "Sandeep R"
birth_dt_local = datetime(2000, 2, 5, 7, 45, 0)
tz_offset = 5.5
dt_utc = birth_dt_local - timedelta(hours=tz_offset)
lat = 12.9982
lon = 77.5530
location = "ESI Hospital, Rajajinagar, Bengaluru, Karnataka, India"

print(f"Calculating Kundali and predictions for {client_name}...")
kundali = calculate_kundali(dt_utc, lat, lon, tz_offset)
dossier = SandeepConsultationEngine.evaluate(kundali)

# Output paths
output_pdf = os.path.abspath(os.path.join("output", "sandeep_r_complete_consultation_dossier.pdf"))

print(f"Generating Consultation PDF at: {output_pdf}...")
generate_sandeep_pdf_report(dossier, output_pdf, location)

artifact_dir = os.environ.get("ANTIGRAVITY_ARTIFACT_DIR")
if artifact_dir and os.path.isdir(artifact_dir):
    shutil.copyfile(output_pdf, os.path.join(artifact_dir, "sandeep_r_complete_consultation_dossier.pdf"))

file_size = os.path.getsize(output_pdf)
print(f"SUCCESS: Consultation PDF for {client_name} generated successfully! ({file_size} bytes)")
print(f"Local Path: {output_pdf}")

# Create desktop shortcut if Desktop folder exists
desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
if os.path.isdir(desktop_dir):
    shortcut_path = os.path.join(desktop_dir, "Sandeep_R_Astrology_Report.url")
    try:
        with open(shortcut_path, "w", encoding="utf-8") as f:
            f.write("[InternetShortcut]\n")
            f.write(f"URL=file:///{output_pdf.replace(os.sep, '/')}\n")
            f.write("IconIndex=0\n")
            f.write(r"IconFile=C:\Program Files\Google\Chrome\Application\chrome.exe" + "\n")
        print(f"Created Desktop Shortcut: {shortcut_path}")
    except Exception as e:
        print(f"Could not create desktop shortcut: {e}")

# Open in Chrome or default browser
chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
]
chrome_bin = next((p for p in chrome_paths if os.path.exists(p)), None)
if chrome_bin:
    print("Launching Google Chrome...")
    subprocess.Popen([chrome_bin, output_pdf])
    print("Opened in Google Chrome!")
else:
    import webbrowser
    webbrowser.open(output_pdf)
