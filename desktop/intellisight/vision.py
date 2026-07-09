"""Open-vocabulary object detection (Ultralytics YOLO-World).

Unlike a normal YOLO model (locked to 80 fixed classes), YOLO-World detects
whatever words you give it. Edit VOCABULARY below to add or remove the things
you want Big Brother to look for. Returns normalised bounding boxes (0..1).
"""

DEFAULT_MODEL = "yolov8x-worldv2.pt"  # open-vocabulary; auto-downloaded (~140 MB)
DEFAULT_CONF = 0.10                   # low floor; the Tracker confirms the sure ones
NMS_IOU = 0.55                        # overlap needed to treat two boxes as competing
NMS_AREA_SIM = 0.82                   # ...and they must be near the SAME SIZE to suppress

# ── The things Big Brother looks for. ──
# A broad list of everyday objects. Add or remove words freely.
# Note: a bigger list covers more, but if you see two similar things get mixed up
# (e.g. pen vs pencil), a shorter, more specific list is more accurate.
VOCABULARY = [
    # People
    "person", "face", "hand",

    # Desk & stationery
    "pen", "pencil", "marker", "highlighter", "crayon", "eraser", "ruler",
    "scissors", "stapler", "tape", "glue stick", "paper clip", "sticky note",
    "notebook", "book", "magazine", "folder", "binder", "envelope", "paper",
    "calculator", "clipboard", "whiteboard", "map",

    # Electronics & tech
    "phone", "laptop", "tablet", "computer mouse", "keyboard", "monitor",
    "television", "remote control", "headphones", "earbuds", "airpods", "speaker",
    "microphone", "webcam", "camera", "charger", "cable", "power bank",
    "usb drive", "hard drive", "router", "game controller", "printer",
    "smartwatch", "e-reader", "light bulb",

    # Kitchen & dining
    "cup", "mug", "glass", "bottle", "water bottle", "can", "thermos", "flask",
    "fork", "knife", "spoon", "chopsticks", "plate", "bowl", "pot", "pan",
    "kettle", "teapot", "cutting board", "wine glass", "jar", "jug", "napkin",
    "straw", "blender", "toaster", "microwave", "coffee maker", "lunch box",

    # Food & drink
    "banana", "apple", "orange", "lemon", "grapes", "strawberry", "tomato",
    "carrot", "potato", "bread", "sandwich", "pizza", "burger", "hot dog",
    "donut", "cake", "cookie", "chocolate", "egg", "cheese", "sushi", "noodles",
    "ice cream", "candy",

    # Personal & accessories
    "key", "keychain", "wallet", "purse", "glasses", "sunglasses", "watch",
    "ring", "necklace", "bracelet", "earrings", "hat", "cap", "scarf", "gloves",
    "belt", "tie", "umbrella", "backpack", "handbag", "suitcase", "face mask",
    "credit card", "id card", "passport", "money", "coin",

    # Clothing & footwear
    "shirt", "t-shirt", "jacket", "coat", "sweater", "hoodie", "jeans", "pants",
    "shorts", "dress", "skirt", "sock", "shoe", "sneaker", "boot", "sandal",
    "slipper",

    # Bathroom & grooming
    "toothbrush", "toothpaste", "comb", "hairbrush", "razor", "soap", "shampoo",
    "towel", "toilet paper", "deodorant", "perfume", "lotion", "makeup",
    "lipstick",

    # Health
    "medicine", "pill bottle", "thermometer", "bandage", "syringe", "stethoscope",
    "inhaler",

    # Home & furniture
    "chair", "table", "desk", "sofa", "bed", "pillow", "blanket", "lamp", "clock",
    "mirror", "picture frame", "vase", "plant", "flower pot", "candle",
    "trash can", "basket", "box", "cushion", "curtain", "rug", "shelf", "fan",
    "heater",

    # Tools & hardware
    "hammer", "screwdriver", "wrench", "pliers", "drill", "saw", "tape measure",
    "nail", "screw", "flashlight", "utility knife", "toolbox", "paintbrush",

    # Toys & hobbies
    "toy", "teddy bear", "doll", "lego", "rubik's cube", "dice", "playing cards",
    "guitar", "piano", "drum", "violin",

    # Sports & outdoor
    "ball", "basketball", "football", "soccer ball", "tennis ball",
    "tennis racket", "baseball bat", "skateboard", "bicycle", "helmet",
    "dumbbell", "yoga mat", "frisbee",

    # Misc
    "lighter", "battery", "tissue box", "spray bottle", "bucket", "broom",
    "sponge", "gift box", "balloon", "watering can",

    # Vehicles (through a window)
    "car", "motorcycle", "bus", "truck",

    # Pets
    "cat", "dog", "bird",
]

_TECH = {
    "laptop", "computer mouse", "keyboard", "phone", "tablet", "monitor",
    "television", "remote control", "headphones", "earbuds", "airpods", "speaker",
    "microphone", "webcam", "camera", "charger", "cable", "power bank",
    "usb drive", "hard drive", "router", "game controller", "printer",
    "smartwatch", "e-reader", "light bulb",
}
_FOOD = {
    "cup", "mug", "glass", "bottle", "water bottle", "can", "thermos", "flask",
    "wine glass", "fork", "knife", "spoon", "chopsticks", "plate", "bowl", "pot",
    "pan", "kettle", "teapot", "jar", "jug", "banana", "apple", "orange", "lemon",
    "grapes", "strawberry", "tomato", "carrot", "potato", "bread", "sandwich",
    "pizza", "burger", "hot dog", "donut", "cake", "cookie", "chocolate", "egg",
    "cheese", "sushi", "noodles", "ice cream", "candy",
}
_FURNITURE = {
    "chair", "table", "desk", "sofa", "bed", "lamp", "shelf", "mirror",
    "picture frame", "vase", "plant", "flower pot", "candle", "curtain", "rug",
}


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


def _same_object(a: dict, b: dict) -> bool:
    """Two boxes are the SAME object (competing labels) only if they overlap a lot
    AND are close to the same size — so a small nested thing (a coat on a person)
    never suppresses the larger real object."""
    if _iou(a, b) < NMS_IOU:
        return False
    area_a = (a["x2"] - a["x1"]) * (a["y2"] - a["y1"])
    area_b = (b["x2"] - b["x1"]) * (b["y2"] - b["y1"])
    if area_a <= 0 or area_b <= 0:
        return False
    return min(area_a, area_b) / max(area_a, area_b) >= NMS_AREA_SIM


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

        # Cross-class NMS: when the model puts two different labels on essentially
        # the same object (same place AND same size), keep only the most confident
        # one (kills mislabels like pen↔toothbrush) — but never drops a distinct
        # object that merely overlaps (a person and their coat).
        detections.sort(key=lambda d: d["confidence"], reverse=True)
        kept = []
        for det in detections:
            if all(not _same_object(det["box"], other["box"]) for other in kept):
                kept.append(det)
        return kept
