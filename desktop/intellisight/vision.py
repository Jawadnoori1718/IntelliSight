"""Open-vocabulary object detection (Ultralytics YOLO-World).

Unlike a normal YOLO model (locked to 80 fixed classes), YOLO-World detects
whatever words you give it. Edit VOCABULARY below to add or remove the things
you want IntelliSight to look for. Returns normalised bounding boxes (0..1).
"""

DEFAULT_MODEL = "yolov8x-worldv2.pt"  # open-vocabulary; auto-downloaded (~140 MB)
DEFAULT_CONF = 0.10                   # low floor; the Tracker confirms the sure ones

# ── The things IntelliSight looks for. Add your own words here! ──
VOCABULARY = [
    "person",
    "pen", "pencil", "marker", "highlighter", "eraser", "ruler", "scissors", "stapler",
    "key", "wallet", "glasses", "sunglasses", "watch", "ring",
    "headphones", "earbuds", "airpods", "phone", "laptop", "tablet",
    "computer mouse", "keyboard", "monitor", "remote control", "charger", "cable",
    "power bank", "usb drive", "camera",
    "cup", "mug", "glass", "bottle", "water bottle", "can", "coffee cup",
    "fork", "knife", "spoon", "plate", "bowl",
    "banana", "apple", "orange",
    "book", "notebook", "paper", "envelope",
    "sneaker", "shoe", "sandal", "sock", "hat", "cap", "backpack", "bag", "handbag", "umbrella",
    "chair", "table", "lamp", "clock", "plant", "pillow", "toy", "ball",
    "toothbrush", "toothpaste", "comb", "razor", "lighter", "battery", "tissue box",
]

_TECH = {
    "laptop", "computer mouse", "keyboard", "phone", "tablet", "monitor", "tv",
    "remote control", "headphones", "earbuds", "airpods", "charger", "cable",
    "power bank", "usb drive", "camera",
}
_FOOD = {
    "bottle", "water bottle", "cup", "mug", "glass", "can", "coffee cup", "wine glass",
    "fork", "knife", "spoon", "plate", "bowl", "banana", "apple", "orange",
}
_FURNITURE = {"chair", "table", "lamp", "plant", "pillow", "bed", "couch", "sofa"}


def _categorize(label: str) -> str:
    low = label.lower()
    if low == "person":
        return "person"
    if low in _TECH:
        return "tech"
    if low in _FOOD:
        return "food"
    if low in _FURNITURE:
        return "furniture"
    return "object"


def _pretty(label: str) -> str:
    return label.title()


class Detector:
    def __init__(self, model_name: str = DEFAULT_MODEL, conf: float = DEFAULT_CONF,
                 classes=None, device: str | None = None):
        self.model_name = model_name
        self.conf = conf
        self.classes = list(classes) if classes else list(VOCABULARY)
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
        self._model.set_classes(self.classes)
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
