"""Text recognition (OCR) service using EasyOCR.

Like the detector, the EasyOCR reader is loaded lazily on first use (it downloads
its models the first time) and boxes are returned normalised to 0..1 so the
frontend can place them on any display size.
"""

import threading
import time
from functools import lru_cache

import cv2
import numpy as np

from app.config import get_settings


class OCRService:
    def __init__(self) -> None:
        self._settings = get_settings()
        self._reader = None
        self._lock = threading.Lock()

    def _ensure_reader(self) -> None:
        if self._reader is None:
            import easyocr

            self._reader = easyocr.Reader(
                self._settings.ocr_languages_list,
                gpu=False,
                verbose=False,
            )

    def read(self, image_bgr: "np.ndarray | None") -> dict:
        """Read text from a BGR image; return blocks in reading order."""
        if image_bgr is None or getattr(image_bgr, "size", 0) == 0:
            return {"blocks": [], "text": "", "width": 0, "height": 0, "ocr_ms": 0.0}

        h, w = image_bgr.shape[:2]
        with self._lock:
            self._ensure_reader()
            t0 = time.perf_counter()
            raw = self._reader.readtext(image_bgr)
            ocr_ms = (time.perf_counter() - t0) * 1000.0

        blocks = []
        for bbox, text, conf in raw:
            conf = float(conf)
            text = (text or "").strip()
            if not text or conf < self._settings.ocr_conf:
                continue
            xs = [float(p[0]) for p in bbox]
            ys = [float(p[1]) for p in bbox]
            blocks.append(
                {
                    "text": text,
                    "confidence": round(conf, 3),
                    "box": {
                        "x1": round(min(xs) / w, 4),
                        "y1": round(min(ys) / h, 4),
                        "x2": round(max(xs) / w, 4),
                        "y2": round(max(ys) / h, 4),
                    },
                }
            )

        # Reading order: top-to-bottom, then left-to-right.
        blocks.sort(key=lambda b: (b["box"]["y1"], b["box"]["x1"]))
        return {
            "blocks": blocks,
            "text": " ".join(b["text"] for b in blocks),
            "width": w,
            "height": h,
            "ocr_ms": round(ocr_ms, 1),
        }

    def read_jpeg(self, data: bytes) -> dict:
        """Decode a JPEG/PNG byte string and read text from it."""
        arr = np.frombuffer(data, dtype=np.uint8)
        image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return self.read(image)


@lru_cache
def get_ocr() -> OCRService:
    """Return the shared OCR service instance."""
    return OCRService()
