"""Frame-to-frame tracking so boxes are steady and confidence locks in.

An object is only reported once it has been seen consistently for a few frames
above a confidence threshold ("confirmed"). At that moment its confidence is
**locked** and never changes again, and its box is smoothed so it doesn't jitter.
"""

IOU_MATCH = 0.4       # overlap needed to consider two boxes the same object
MIN_CONF = 0.35       # peak confidence needed before we trust an object
CONFIRM_HITS = 3      # consecutive frames before an object is confirmed
MAX_MISSES = 8        # frames an object may disappear before we drop it
SMOOTH = 0.6          # box smoothing (higher = steadier)


def _iou(a: dict, b: dict) -> float:
    x1 = max(a["x1"], b["x1"])
    y1 = max(a["y1"], b["y1"])
    x2 = min(a["x2"], b["x2"])
    y2 = min(a["y2"], b["y2"])
    inter = max(0.0, x2 - x1) * max(0.0, y2 - y1)
    area_a = (a["x2"] - a["x1"]) * (a["y2"] - a["y1"])
    area_b = (b["x2"] - b["x1"]) * (b["y2"] - b["y1"])
    union = area_a + area_b - inter
    return inter / union if union > 0 else 0.0


class _Track:
    def __init__(self, track_id: int, det: dict):
        self.id = track_id
        self.label = det["label"]
        self.category = det["category"]
        self.box = dict(det["box"])
        self.peak = det["confidence"]
        self.conf = det["confidence"]  # displayed; frozen once confirmed
        self.hits = 1
        self.misses = 0
        self.confirmed = False


class Tracker:
    def __init__(self):
        self._tracks = []
        self._next_id = 0

    def update(self, detections: list) -> list:
        matched = set()
        unmatched = []

        for det in detections:
            best, best_iou = None, IOU_MATCH
            for i, track in enumerate(self._tracks):
                if i in matched or track.label != det["label"]:
                    continue
                score = _iou(track.box, det["box"])
                if score >= best_iou:
                    best_iou, best = score, i

            if best is None:
                unmatched.append(det)
            else:
                matched.add(best)
                track = self._tracks[best]
                for key in ("x1", "y1", "x2", "y2"):
                    track.box[key] = SMOOTH * track.box[key] + (1 - SMOOTH) * det["box"][key]
                track.hits += 1
                track.misses = 0
                if not track.confirmed:
                    track.peak = max(track.peak, det["confidence"])
                    if track.hits >= CONFIRM_HITS and track.peak >= MIN_CONF:
                        track.confirmed = True
                        track.conf = track.peak  # LOCK the confidence

        survivors = []
        for i, track in enumerate(self._tracks):
            if i in matched:
                survivors.append(track)
            else:
                track.misses += 1
                if track.misses <= MAX_MISSES:
                    survivors.append(track)

        for det in unmatched:
            self._next_id += 1
            survivors.append(_Track(self._next_id, det))

        self._tracks = survivors

        confirmed = [
            {
                "id": t.id,
                "label": t.label,
                "category": t.category,
                "confidence": round(t.conf, 3),
                "box": dict(t.box),
            }
            for t in self._tracks
            if t.confirmed
        ]
        confirmed.sort(key=lambda d: d["confidence"], reverse=True)
        return confirmed
