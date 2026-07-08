"""Turn the tracker's stable objects into appear / disappear / dwell events.

The tracker already gives each object a stable id and coasts it through brief
misses, so simply diffing the id-set between updates yields debounced events —
no extra flicker handling needed here.
"""

DWELL_SECONDS = 8.0  # how long an object must stay before a 'lingered' event


class EventDetector:
    def __init__(self, dwell_seconds: float = DWELL_SECONDS):
        self.dwell_seconds = dwell_seconds
        self._active = {}  # id -> {label, category, first_seen, dwelled}

    def update(self, detections: list, now: float) -> list:
        """Return new events since the last update. `now` is a monotonic clock."""
        events = []
        seen = {det["id"]: det for det in detections if "id" in det}

        # Appeared — an id we haven't seen before
        for oid, det in seen.items():
            if oid not in self._active:
                self._active[oid] = {
                    "label": det["label"],
                    "category": det["category"],
                    "first_seen": now,
                    "dwelled": False,
                }
                events.append(self._event("appeared", oid))

        # Disappeared — an id that was active but is gone now
        for oid in list(self._active.keys()):
            if oid not in seen:
                events.append(self._event("disappeared", oid))
                del self._active[oid]

        # Lingered — an object that has stayed long enough (once)
        for oid, info in self._active.items():
            if not info["dwelled"] and (now - info["first_seen"]) >= self.dwell_seconds:
                info["dwelled"] = True
                events.append(self._event("lingered", oid))

        return events

    def reset(self) -> None:
        self._active.clear()

    def _event(self, kind: str, oid: int) -> dict:
        info = self._active.get(oid, {})
        return {
            "type": kind,  # appeared | disappeared | lingered
            "id": oid,
            "label": info.get("label", "Object"),
            "category": info.get("category", "object"),
        }
