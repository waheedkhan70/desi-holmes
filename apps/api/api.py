from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import CaseCreate, CaseResponse, CaseResult
from .deps import SessionLocal, engine
from . import models, crud
import json, os
import redis

router = APIRouter()

# ensure tables
models.Base.metadata.create_all(bind=engine)

r = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        _ = db.execute("SELECT 1").scalar()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/v1/cases", response_model=CaseResponse)
def create_case(payload: CaseCreate, db: Session = Depends(get_db)):
    case = crud.create_case(db, payload.title, payload.narrative, payload.media)
    # enqueue job
    job = {"case_id": case.id, "options": payload.options.dict()}
    r.lpush("desi_jobs", json.dumps(job))
    return {"case_id": case.id, "status": case.status}

@router.get("/v1/cases/{case_id}/results", response_model=CaseResult)
def get_results(case_id: str, db: Session = Depends(get_db)):
    case = crud.get_case(db, case_id)
    if not case:
        raise HTTPException(404, "case not found")
    if not case.result:
        # return empty skeleton
        return CaseResult()
    return case.result
