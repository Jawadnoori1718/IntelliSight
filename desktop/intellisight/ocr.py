"""Text recognition (OCR) engine using EasyOCR.

Loaded lazily (downloads its models on first use). Returns text blocks in reading
order, each with normalised coordinates so they can be drawn on any display size.
"""


class OCREngine:
    def __init__(self, languages=("en",), conf: float = 0.30):
        self._languages = list(languages)
        self._conf = conf
        self._reader = None

    def load(self) -> None:
        import easyocr

        # gpu=False → CPU. EasyOCR doesn't use Apple MPS; CPU is ~0.7s/frame,
        # which is fine because we only run OCR about once a second.
        self._reader = easyocr.Reader(self._languages, gpu=False, verbose=False)

    def read(self, frame_bgr) -> list:
        if self._reader is None or frame_bgr is None:
            return []

        height, width = frame_bgr.shape[:2]
        raw = self._reader.readtext(frame_bgr)

        blocks = []
        for bbox, text, conf in raw:
            conf = float(conf)
            text = (text or "").strip()
            if not text or conf < self._conf:
                continue
            xs = [float(p[0]) for p in bbox]
            ys = [float(p[1]) for p in bbox]
            blocks.append(
                {
                    "text": text,
                    "confidence": round(conf, 3),
                    "box": {
                        "x1": min(xs) / width,
                        "y1": min(ys) / height,
                        "x2": max(xs) / width,
                        "y2": max(ys) / height,
                    },
                }
            )

        blocks.sort(key=lambda b: (b["box"]["y1"], b["box"]["x1"]))
        return blocks
