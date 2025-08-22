from datetime import datetime
from sqlalchemy.orm import Session
from . import models

def create_case(db: Session, title: str, narrative: str, media_uris: list):
    cid = f"c_{__import__('uuid').uuid4().hex[:8]}"
    case = models.Case(id=cid, title=title, narrative=narrative, status="queued", created_at=datetime.utcnow().isoformat())
    db.add(case)
    db.commit()
    for u in media_uris:
        m = models.Media(id=f"m_{__import__('uuid').uuid4().hex[:8]}", case_id=cid, uri=u, type="image" if u.lower().endswith(('.jpg','.png','.jpeg')) else "video", meta={})
        db.add(m)
    db.commit()
    db.refresh(case)
    return case

def get_case(db: Session, case_id: str):
    return db.get(models.Case, case_id)

def update_case_result(db: Session, case_id: str, result: dict, status: str = "done"):
    case = db.get(models.Case, case_id)
    if not case:
        return None
    case.result = result
    case.status = status
    db.add(case)
    db.commit()
    db.refresh(case)
    return case
