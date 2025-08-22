def detect_on_media(media_uris):
    """
    Simple stub: returns empty detections for every media.
    Replace this with YOLOv8/RT-DETR inference that returns:
      [{"media": uri, "label":"knife", "bbox":[x,y,w,h], "score":0.92}, ...]
    """
    detections = []
    for uri in media_uris:
        # placeholder
        detections.append({"media": uri, "detections": []})
    return detections
