from pydantic import BaseModel
from typing import List, Optional, Any

class CaseOptions(BaseModel):
    run_cv: bool = True
    run_nlp: bool = True

class CaseCreate(BaseModel):
    title: str
    narrative: str
    media: List[str] = []
    options: Optional[CaseOptions] = CaseOptions()

class CaseResponse(BaseModel):
    case_id: str
    status: str

class Theory(BaseModel):
    id: str
    score: float
    explanation: Any

class CaseResult(BaseModel):
    entities: List[Any] = []
    events: List[Any] = []
    timeline: List[Any] = []
    detections: List[Any] = []
    theories: List[Theory] = []
    report_url: Optional[str] = None
