
import sys
import uuid
import os
from app.schemas.resume_schema import Resume
from app.services.ingest_service import ingest_resume

try:
    print("Testing ingest_resume with None value in metadata...")
    # Create a resume with seniority=None
    resume = Resume(
        name="Test User",
        skills=["Python"],
        seniority=None,
        experience_years=5,
        text="Sample text"
    )
    
    ingest_resume(resume)
    print("Success!")
except Exception as e:
    print(f"Caught expected error: {e}")
