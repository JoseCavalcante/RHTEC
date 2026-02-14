from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Any
from app.schemas.resume_schema import Resume
from app.services.ingest_service import ingest_resume
from app.services.file_service import extract_text_from_file
from app.services.extraction_service import extract_resume_data
from app.core.exceptions import AppError

router = APIRouter()

@router.post("/resume", tags=["Resumes"])
async def add_resume(resume: Resume) -> Dict[str, str]:
    """
    Manually add a single resume to the system.
    """
    try:
        await ingest_resume(resume)
        return {"msg": "indexed"}
    except AppError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload_resumes", tags=["Resumes"])
async def upload_resumes(files: List[UploadFile] = File(...)) -> List[Dict[str, Any]]:
    """
    Process multiple resume files (PDF/DOCX), extracting data and indexing them.
    """
    results = []
    for file in files:
        try:
            content = await file.read()
            text = extract_text_from_file(content, file.filename)
            
            if text:
                # Extract structured data using LLM
                resume = await extract_resume_data(text)
                
                if resume:
                    await ingest_resume(resume)
                    results.append({
                        "filename": file.filename, 
                        "status": "success", 
                        "candidate": resume.name
                    })
                else:
                    results.append({
                        "filename": file.filename, 
                        "status": "error", 
                        "message": "Failed to extract professional data from text"
                    })
            else:
                results.append({
                    "filename": file.filename, 
                    "status": "error", 
                    "message": "Unsupported file type or empty file"
                })
        except Exception as e:
            results.append({
                "filename": file.filename, 
                "status": "error", 
                "message": str(e)
            })
    return results
