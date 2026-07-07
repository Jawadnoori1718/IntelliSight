"""Scene understanding via Claude (multimodal).

Sends the current camera frame plus the detected object labels to Claude and gets
back a short, human-friendly description of the whole scene. Uses structured JSON
output so the result is always cleanly parseable.
"""

import base64
import json

import cv2

SYSTEM_PROMPT = (
    "You are IntelliSight's scene analyst. You are shown a single frame from a "
    "webcam plus a list of objects an object-detector found in it. Describe the "
    "scene naturally and concisely for the person using the app. Base everything "
    "on what is actually visible — do not invent details. Fill in the fields; keep "
    "'description' to one or two sentences."
)

_SCHEMA = {
    "type": "object",
    "properties": {
        "description": {"type": "string"},
        "activity": {"type": "string"},
        "environment": {"type": "string"},
        "lighting": {"type": "string"},
    },
    "required": ["description", "activity", "environment", "lighting"],
    "additionalProperties": False,
}

_FALLBACK = {"description": "Scene could not be described.", "activity": "—", "environment": "—", "lighting": "—"}


class SceneEngine:
    def __init__(self, api_key: str, model: str):
        self._api_key = api_key
        self._model = model
        self._client = None

    def available(self) -> bool:
        return bool(self._api_key)

    def _ensure_client(self):
        if self._client is None:
            from anthropic import Anthropic

            self._client = Anthropic(api_key=self._api_key)

    def _encode(self, frame_bgr) -> str:
        """Downscale + JPEG-encode a frame to base64 (smaller = cheaper & faster)."""
        height, width = frame_bgr.shape[:2]
        target_w = 768
        if width > target_w:
            scale = target_w / width
            frame_bgr = cv2.resize(frame_bgr, (target_w, int(height * scale)))
        ok, buffer = cv2.imencode(".jpg", frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, 80])
        return base64.b64encode(buffer).decode("ascii")

    def describe(self, frame_bgr, labels) -> dict:
        self._ensure_client()
        image_b64 = self._encode(frame_bgr)
        detected = ", ".join(dict.fromkeys(labels)) or "none"

        message = self._client.messages.create(
            model=self._model,
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {"type": "base64", "media_type": "image/jpeg", "data": image_b64},
                        },
                        {"type": "text", "text": f"Objects detected: {detected}. Describe this scene."},
                    ],
                }
            ],
            output_config={"format": {"type": "json_schema", "schema": _SCHEMA}},
        )

        if message.stop_reason == "refusal":
            return dict(_FALLBACK)

        text = next((b.text for b in message.content if b.type == "text"), "")
        try:
            return json.loads(text)
        except (json.JSONDecodeError, TypeError):
            return {**_FALLBACK, "description": text.strip()[:300] or _FALLBACK["description"]}
