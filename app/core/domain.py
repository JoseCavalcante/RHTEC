from typing import List

def format_candidate_text(name: str, seniority: str, skills: List[str], summary: str) -> str:
    """
    Centralizes the logic for creating the rich text representation of a candidate
    used for embedding generation.
    
    Format: "Name: <name> | Seniority: <seniority> | Skills: <skills> | Summary: <text>"
    """
    skills_str = ", ".join(skills) if skills else ""
    return f"Name: {name} | Seniority: {seniority} | Skills: {skills_str} | Summary: {summary}"
