"""Accurate object detection (Ultralytics YOLO11).

Returns, for every object it sees: a label, category, confidence and a normalised
bounding box (0..1). Boxes only — clean and fast; the Tracker decides which ones
are sure enough to show.
"""

DEFAULT_MODEL = "yolo11l.pt"  # large detection model — accurate; auto-downloaded
DEFAULT_CONF = 0.30           # candidates; the Tracker confirms the confident ones

_TECH = {"laptop", "mouse", "keyboard", "cell phone", "tv", "remote"}
_FOOD = {
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl",
    "banana", "apple", "sandwich", "orange", "broccoli", "carrot",
    "hot dog", "pizza", "donut", "cake",
}
_FURNITURE = {"chair", "couch", "potted plant", "bed", "dining table", "toilet", "bench"}
_OVERRIDES = {"tv": "TV", "cell phone": "Phone", "dining table": "Table"}


def _categorize(label: str) -> str:
    if label == "person":
        return "person"
    if label in _TECH:
        return "tech"
    if label in _FOOD:
        return "food"
    if label in _FURNITURE:
        return "furniture"
    return "object"


def _pretty(label: str) -> str:
    return _OVERRIDES.get(label, label.title())


class Detector:
    def __init__(self, model_name: str = DEFAULT_MODEL, conf: float = DEFAULT_CONF, device: str | None = None):
        self.model_name = model_name
        self.conf = conf
        self.device = device
        self._model = None

    def _pick_device(self) -> str:
        if self.device:
            return self.device
        try:
            import torch

            if torch.backends.mps.is_available():
                return "mps"
        except Exception:
            pass
        return "cpu"

    def load(self) -> None:
        import numpy as np
        from ultralytics import YOLO

        self._model = YOLO(self.model_name)
        self.device = self._pick_device()
        dummy = np.zeros((320, 320, 3), dtype=np.uint8)
        try:
            self._model.predict(dummy, device=self.device, verbose=False, conf=0.5)
        except Exception:
            self.device = "cpu"
            self._model.predict(dummy, device="cpu", verbose=False, conf=0.5)

    def detect(self, frame_bgr) -> list:
        if self._model is None:
            return []
        height, width = frame_bgr.shape[:2]
        results = self._model.predict(
            frame_bgr, conf=self.conf, device=self.device, verbose=False
        )
        result = results[0]
        names = result.names
        boxes = result.boxes

        detections = []
        for i in range(len(boxes)):
            raw = names[int(boxes.cls[i])]
            x1, y1, x2, y2 = (float(v) for v in boxes.xyxy[i].tolist())
            detections.append(
                {
                    "label": _pretty(raw),
                    "category": _categorize(raw),
                    "confidence": float(boxes.conf[i]),
                    "box": {
                        "x1": x1 / width,
                        "y1": y1 / height,
                        "x2": x2 / width,
                        "y2": y2 / height,
                    },
                }
            )
        return detections
