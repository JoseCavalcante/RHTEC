from pydantic import BaseModel
from typing import List, Optional

class Resume(BaseModel):
    name: str
    skills: List[str]
    seniority: Optional[str]
    experience_years: int
    text: str

class UpdateResume(BaseModel):
    name: str
    skills: List[str]
    seniority: Optional[str]
    experience_years: int
    text: str
