"""Accurate object segmentation engine (Ultralytics YOLO11-seg).

Returns, for every object it sees: a label, category, confidence, a normalised
bounding box, and a normalised outline polygon (the segmentation contour). All
coordinates are 0..1 so they can be drawn on any display size.
"""

# A larger model = much more accurate than the old nano detector. Segmentation
# ("-seg") gives us the outline of each object, not just a box.
DEFAULT_MODEL = "yolo11l-seg.pt"
DEFAULT_CONF = 0.25  # a bit low so it draws most of what it sees

# COCO label -> IntelliSight category (drives the colour)
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


class SegmentationEngine:
    def __init__(self, model_name: str = DEFAULT_MODEL, conf: float = DEFAULT_CONF, device: str | None = None):
        self.model_name = model_name
        self.conf = conf
        self.device = device  # None -> auto (mps if available, else cpu)
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
        """Load the model and validate the compute device (falls back to CPU)."""
        import numpy as np
        from ultralytics import YOLO

        self._model = YOLO(self.model_name)
        self.device = self._pick_device()

        # Warm up once; if the chosen device fails, fall back to CPU.
        dummy = np.zeros((320, 320, 3), dtype=np.uint8)
        try:
            self._model.predict(dummy, device=self.device, verbose=False, conf=0.5)
        except Exception:
            self.device = "cpu"
            self._model.predict(dummy, device="cpu", verbose=False, conf=0.5)

    def infer(self, frame_bgr) -> list:
        """Run segmentation on a BGR frame → list of detection dicts."""
        if self._model is None:
            return []

        height, width = frame_bgr.shape[:2]
        results = self._model.predict(
            frame_bgr,
            conf=self.conf,
            device=self.device,
            retina_masks=True,
            verbose=False,
        )
        result = results[0]
        names = result.names
        boxes = result.boxes
        masks = result.masks

        detections = []
        for i in range(len(boxes)):
            cls_id = int(boxes.cls[i])
            raw = names[cls_id]
            conf = float(boxes.conf[i])
            x1, y1, x2, y2 = (float(v) for v in boxes.xyxy[i].tolist())

            polygon = None
            if masks is not None and masks.xy is not None and i < len(masks.xy):
                pts = masks.xy[i]
                if len(pts) >= 3:
                    polygon = [[float(px) / width, float(py) / height] for px, py in pts]

            detections.append(
                {
                    "label": _pretty(raw),
                    "raw_label": raw,
                    "category": _categorize(raw),
                    "confidence": round(conf, 3),
                    "box": {
                        "x1": x1 / width,
                        "y1": y1 / height,
                        "x2": x2 / width,
                        "y2": y2 / height,
                    },
                    "polygon": polygon,
                }
            )

        detections.sort(key=lambda d: d["confidence"], reverse=True)
        return detections
