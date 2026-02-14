import io
from typing import Optional
import pypdf
import docx

def extract_text_from_file(file_content: bytes, filename: str) -> Optional[str]:
    """
    Extracts text from PDF or DOCX file content.
    """
    if filename.lower().endswith('.pdf'):
        return _extract_from_pdf(file_content)
    elif filename.lower().endswith('.docx'):
        return _extract_from_docx(file_content)
    else:
        return None

def _extract_from_pdf(file_content: bytes) -> str:
    try:
        pdf_reader = pypdf.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def _extract_from_docx(file_content: bytes) -> str:
    try:
        doc = docx.Document(io.BytesIO(file_content))
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return ""
