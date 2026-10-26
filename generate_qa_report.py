"""
Runner script to generate the dedicated Q&A consultation PDF for Ravi Kumar S.
"""
import os
import shutil
import subprocess
from datetime import datetime, timedelta
from app.core.kundali import calculate_kundali
from app.engines.qa_consultation import QAConsultationEngine
from app.reports.qa_pdf_generator import generate_qa_consultation_pdf

# Client details
client_name = "Ravi Kumar S"
birth_dt_local = datetime(1968, 11, 20, 3, 45, 0)
tz_offset = 5.5
dt_utc = birth_dt_local - timedelta(hours=tz_offset)
lat = 13.0068
lon = 77.5713

print(f"Calculating Kundali and Q&A analysis for {client_name}...")
kundali = calculate_kundali(dt_utc, lat, lon, tz_offset)
dossier = QAConsultationEngine.evaluate_ravi_kumar(kundali)

# Output paths
output_pdf = os.path.abspath(os.path.join("output", "ravi_kumar_qa_consultation.pdf"))
artifact_dir = r"C:\Users\Admin\.gemini\antigravity\brain\bf8c0449-bafc-44d0-a5f0-768a5a9cb6ea"
artifact_pdf = os.path.join(artifact_dir, "ravi_kumar_qa_consultation.pdf")

print(f"Generating Q&A Consultation PDF at: {output_pdf}")
generate_qa_consultation_pdf(dossier, output_pdf)

# Copy to artifact folder
shutil.copyfile(output_pdf, artifact_pdf)

file_size = os.path.getsize(output_pdf)
print(f"SUCCESS: Q&A Consultation PDF generated successfully! ({file_size} bytes)")
print(f"Local Path: {output_pdf}")
print(f"Artifact Path: {artifact_pdf}")

# Launch in Chrome
chrome_bin = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if os.path.exists(chrome_bin):
    print("Opening PDF in Google Chrome...")
    subprocess.Popen([chrome_bin, output_pdf])
    print("Opened successfully in Google Chrome!")
