"""Visual question-answering via Claude.

Given the user's question plus the current camera frame and detected objects,
returns a concise natural-language answer.
"""

import base64

import cv2

SYSTEM_PROMPT = (
    "You are IntelliSight's visual assistant. Answer the user's question about what "
    "the camera is currently showing, using the image and the list of detected "
    "objects. Be concise, direct and helpful. If the answer isn't visible in the "
    "image, say so plainly rather than guessing."
)


def _encode(frame_bgr) -> str:
    height, width = frame_bgr.shape[:2]
    if width > 768:
        scale = 768 / width
        frame_bgr = cv2.resize(frame_bgr, (768, int(height * scale)))
    ok, buffer = cv2.imencode(".jpg", frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, 80])
    return base64.b64encode(buffer).decode("ascii")


class AssistantEngine:
    def __init__(self, api_key: str, model: str):
        self._api_key = api_key
        self._model = model
        self._client = None

    def _ensure_client(self):
        if self._client is None:
            from anthropic import Anthropic

            self._client = Anthropic(api_key=self._api_key)

    def answer(self, question: str, frame_bgr, labels) -> str:
        self._ensure_client()
        image_b64 = _encode(frame_bgr)
        detected = ", ".join(dict.fromkeys(labels)) or "none"

        message = self._client.messages.create(
            model=self._model,
            max_tokens=600,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {"type": "base64", "media_type": "image/jpeg", "data": image_b64},
                        },
                        {"type": "text", "text": f"Detected objects: {detected}.\n\nQuestion: {question}"},
                    ],
                }
            ],
        )

        if getattr(message, "stop_reason", None) == "refusal":
            return "I can't help with that one."
        text = " ".join(b.text for b in message.content if b.type == "text").strip()
        return text or "…"
