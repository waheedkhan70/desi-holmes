import os, time, json
import redis
from .deps import SessionLocal
from . import crud, models
from services.nlp.nlp_pipeline import extract_entities_and_timeline
from services.cv.cv_stub import detect_on_media
from services.reasoning.reasoner import generate_theories
from sqlalchemy.orm import Session

r = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

def process_job(job):
    db = SessionLocal()
    try:
        cid = job["case_id"]
        case = crud.get_case(db, cid)
        if not case:
            print(f"[worker] case not found {cid}")
            return
        print(f"[worker] processing {cid}")
        # run NLP
        entities, events, timeline = extract_entities_and_timeline(case.narrative)
        # run CV (on media URIs)
        media = [m.uri for m in db.query(models.Media).filter(models.Media.case_id == cid).all()]
        detections = detect_on_media(media)
        # reasoning
        theories = generate_theories(entities, detections, timeline)

        result = {
            "entities": entities,
            "events": events,
            "timeline": timeline,
            "detections": detections,
            "theories": theories,
            "report_url": None
        }
        crud.update_case_result(db, cid, result, status="done")
        print(f"[worker] done {cid}")
    except Exception as e:
        print("[worker] error", e)
    finally:
        db.close()

def run():
    print("[worker] started, listening to desi_jobs")
    while True:
        job = r.brpop("desi_jobs", timeout=5)
        if job:
            _, payload = job
            job_obj = json.loads(payload)
            process_job(job_obj)
        else:
            time.sleep(1)

if __name__ == "__main__":
    run()
