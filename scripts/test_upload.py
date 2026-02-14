import requests

API = "http://localhost:8001"
print("Sending dummy resume...")

with open("dummy_resume.docx", "rb") as f:
    files = {"files": ("dummy_resume.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    r = requests.post(f"{API}/upload_resumes", files=files)
    
print(f"Status: {r.status_code}")
print(r.json())

# Check candidates
print("\nVerifying candidate list...")
r = requests.get(f"{API}/candidates")
candidates = r.json()
found = False
for c in candidates:
    if c.get('metadata', {}).get('name') == "Maria Exemplo":
        print("SUCCESS! Found Maria Exemplo.")
        found = True
        break

if not found:
    print("FAILED! Candidate not found.")
