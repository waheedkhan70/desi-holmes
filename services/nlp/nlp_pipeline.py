import re
from typing import Tuple, List, Dict

def extract_entities_and_timeline(text: str) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Very simple rule-based extraction:
      - entities: suspects, victims based on keywords (Suspect:, Victim:)
      - times: digits/dates
      - locations: "at <place>" / "in <place>"
    Replace with spaCy / fine-tuned NER for production.
    """
    entities = []
    events = []
    timeline = []

    # quick keyword-based extraction
    # find lines like "Suspect: Raj" or "Victim: Amit"
    for m in re.finditer(r"(Suspect|Victim|Witness|Location|Place)\s*:\s*([A-Z][\w\s-]+)", text, re.IGNORECASE):
        ent_type = m.group(1).lower()
        ent_text = m.group(2).strip()
        entities.append({"type": ent_type, "text": ent_text, "score": 0.6})

    # dates/times
    dates = re.findall(r"(\d{1,2}[:]\d{2}\s*(?:AM|PM|am|pm)?)|(\d{1,2}/\d{1,2}/\d{2,4})", text)
    for d in dates:
        dt = [x for x in d if x][0]
        timeline.append({"time": dt, "desc": "mentioned time"})

    # fallback: find capitalized words (possible names/places) - low precision
    caps = re.findall(r"\b([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})*)\b", text)
    for c in caps[:5]:
        entities.append({"type": "possible_name_or_place", "text": c, "score": 0.3})

    # events: simple verbs sentences split
    for sent in re.split(r"[.]\s+", text):
        if len(sent.split()) > 2:
            # crude event: verb detection by common verbs
            if any(verb in sent.lower() for verb in ["stole", "snatch", "shoot", "attack", "hit", "rob", "assault"]):
                events.append({"desc": sent.strip()})

    return entities, events, timeline
