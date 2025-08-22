import uuid

def generate_theories(entities, detections, timeline):
    """
    Simple rule-based theory generator:
      - produce 3 templated theories with heuristics
      - score by how much evidence exists (entities + detections)
    Replace with LLM-based structured generator when ready.
    """
    theories = []
    base_score = 0.2 + min(0.6, 0.1 * (len(entities) + sum(len(d["detections"]) for d in detections)))
    # simple templates
    t1 = {"id": str(uuid.uuid4()), "score": round(base_score + 0.15, 2),
          "explanation": {"summary": "Opportunistic theft", "reasons": ["no weapon evidence", "short timeline"]}}
    t2 = {"id": str(uuid.uuid4()), "score": round(base_score, 2),
          "explanation": {"summary": "Planned robbery", "reasons": ["multiple actors possible (witness reports)"]}}
    t3 = {"id": str(uuid.uuid4()), "score": round(max(0.05, base_score - 0.1), 2),
          "explanation": {"summary": "False report / misdirection", "reasons": ["conflicting statements or missing evidence"]}}
    theories.extend([t1, t2, t3])
    # sort by score descending
    theories = sorted(theories, key=lambda x: x["score"], reverse=True)
    return theories
