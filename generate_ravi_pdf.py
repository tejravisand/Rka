"""
Generate PDF consultation report for Ravi Kumar S and open in Google Chrome.
"""
import os
import subprocess
from datetime import datetime, timezone, timedelta
from app.core.kundali import calculate_kundali
from app.reports.pdf_generator import generate_astrological_pdf

# Details for Ravi Kumar S
client_name = "Ravi Kumar S"
birth_dt_local = datetime(1968, 11, 20, 3, 45, 0)
tz_offset = 5.5
dt_utc = birth_dt_local - timedelta(hours=tz_offset)
lat = 13.0068
lon = 77.5713
location = "KC General Hospital, Malleshwaram, Bengaluru, Karnataka, India"

# Output PDF path
pdf_filename = "ravi_kumar_s_kundali_report.pdf"
pdf_path = os.path.abspath(os.path.join("output", pdf_filename))

print(f"Calculating Kundali for {client_name}...")
kundali = calculate_kundali(dt_utc, lat, lon, tz_offset)

print(f"Generating publication-quality PDF at: {pdf_path}")
generate_astrological_pdf(
    kundali=kundali,
    client_name=client_name,
    output_pdf_path=pdf_path,
    location_name=location
)

file_size = os.path.getsize(pdf_path)
print(f"SUCCESS: PDF generated successfully! ({file_size} bytes)")
print(f"File Path: {pdf_path}")

# Open in Google Chrome
chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
]

chrome_bin = None
for p in chrome_paths:
    if os.path.exists(p):
        chrome_bin = p
        break

if chrome_bin:
    print(f"Launching Google Chrome with file URL: {pdf_path}")
    # Run in background without blocking
    subprocess.Popen([chrome_bin, pdf_path])
    print("Opened PDF in Google Chrome!")
else:
    print("Google Chrome path not found directly, attempting default system launcher...")
    os.startfile(pdf_path)
