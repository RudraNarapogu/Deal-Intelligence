from pydantic import BaseModel
from typing import Optional

class DealCreate(BaseModel):
    id: str
    name: str
    client_name: str
    stage: Optional[str] = "Discovery"
    budget: Optional[str] = ""
    summary: Optional[str] = ""

class DealResponse(BaseModel):
    id: str
    name: str
    client_name: str
    stage: str
    budget: str
    summary: str
    created_at: str
    updated_at: str
