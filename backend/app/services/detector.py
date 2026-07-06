"""YOLO object detection service.

Wraps an Ultralytics YOLO model. The model is loaded lazily (on first use) so
the server starts instantly and only pays the model-load cost once detection is
actually requested. Returns boxes with coordinates normalised to 0..1 so the
frontend can scale them to any display size.
"""

import threading
import time
from functools import lru_cache

import cv2
import numpy as np
import psutil

from app.config import get_settings

# COCO label -> IntelliSight category (drives the colour shown in the UI).
_TECH = {"laptop", "mouse", "keyboard", "cell phone", "tv", "remote"}
_FOOD = {
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl",
    "banana", "apple", "sandwich", "orange", "broccoli", "carrot",
    "hot dog", "pizza", "donut", "cake",
}
_FURNITURE = {"chair", "couch", "potted plant", "bed", "dining table", "toilet", "bench"}

# A few nicer display names.
_LABEL_OVERRIDES = {"tv": "TV", "cell phone": "Phone", "dining table": "Table"}


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
    return _LABEL_OVERRIDES.get(label, label.title())


class Detector:
    def __init__(self) -> None:
        self._settings = get_settings()
        self._model = None
        self._lock = threading.Lock()

    def _ensure_model(self) -> None:
        if self._model is None:
            # Imported here so torch/ultralytics only load when detection runs.
            from ultralytics import YOLO

            self._model = YOLO(self._settings.yolo_model)

    def detect(self, image_bgr: "np.ndarray | None") -> dict:
        """Run detection on a BGR image and return normalised boxes."""
        if image_bgr is None or getattr(image_bgr, "size", 0) == 0:
            return {
                "detections": [],
                "width": 0,
                "height": 0,
                "inference_ms": 0.0,
                "cpu": 0.0,
                "device": self._settings.detection_device,
            }

        h, w = image_bgr.shape[:2]
        with self._lock:
            self._ensure_model()
            t0 = time.perf_counter()
            results = self._model.predict(
                image_bgr,
                conf=self._settings.detection_conf,
                imgsz=self._settings.detection_imgsz,
                device=self._settings.detection_device,
                verbose=False,
            )
            inference_ms = (time.perf_counter() - t0) * 1000.0

        result = results[0]
        names = result.names
        detections = []
        for box in result.boxes:
            cls_id = int(box.cls[0])
            raw = names[cls_id]
            conf = float(box.conf[0])
            x1, y1, x2, y2 = (float(v) for v in box.xyxy[0].tolist())
            detections.append(
                {
                    "label": _pretty(raw),
                    "raw_label": raw,
                    "category": _categorize(raw),
                    "confidence": round(conf, 3),
                    "box": {
                        "x1": round(x1 / w, 4),
                        "y1": round(y1 / h, 4),
                        "x2": round(x2 / w, 4),
                        "y2": round(y2 / h, 4),
                    },
                }
            )

        detections.sort(key=lambda d: d["confidence"], reverse=True)
        return {
            "detections": detections,
            "width": w,
            "height": h,
            "inference_ms": round(inference_ms, 1),
            "cpu": round(psutil.cpu_percent(interval=None), 1),
            "device": self._settings.detection_device,
        }

    def detect_jpeg(self, data: bytes) -> dict:
        """Decode a JPEG/PNG byte string and detect objects in it."""
        arr = np.frombuffer(data, dtype=np.uint8)
        image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return self.detect(image)


@lru_cache
def get_detector() -> Detector:
    """Return the shared Detector instance."""
    return Detector()
