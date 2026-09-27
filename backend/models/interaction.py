from pydantic import BaseModel
from typing import Optional

class InteractionCreate(BaseModel):
    type: str  # e.g., 'meeting', 'email', 'call', 'outcome'
    date: str  # e.g., '2026-09-27'
    title: Optional[str] = ""
    transcript: str
    context: Optional[str] = "sales meeting"

class AskAgentRequest(BaseModel):
    question: str

class ReflectRequest(BaseModel):
    query: str
    context: Optional[str] = "Sales Deal Analysis"
