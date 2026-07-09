"""Claude vision verification — confirm a nuanced condition on the live frame.

When a rule's cheap local trigger fires, Claude looks at the current frame and
answers the rule's plain-English condition (yes/no) before the action runs.
Strictly rate-limited so an always-on camera can never run up a bill.
"""

import base64
import json
import os

from PySide6.QtCore import QSettings

MODEL = "claude-opus-4-8"
DEFAULT_MAX_PER_HOUR = 60
_MAX_WIDTH = 768
VERIFY_TIMEOUT = 8.0  # seconds — hard bound on the network call so Stop can't hang


def _sdk_available() -> bool:
    try:
        import anthropic  # noqa: F401
        return True
    except Exception:
        return False


class ClaudeClient:
    def __init__(self):
        self._settings = QSettings("BigBrother", "BigBrother")
        self._stored_key = self._settings.value("claude/api_key", "", type=str)
        self.max_per_hour = self._settings.value("claude/max_per_hour", DEFAULT_MAX_PER_HOUR, type=int)
        self._sdk = _sdk_available()
        self._calls = []  # monotonic timestamps of recent calls (main thread only)

    # ── settings ──
    @property
    def api_key(self) -> str:
        return os.environ.get("ANTHROPIC_API_KEY") or self._stored_key

    def key_from_env(self) -> bool:
        return bool(os.environ.get("ANTHROPIC_API_KEY"))

    def stored_key(self) -> str:
        return self._stored_key

    def set_key(self, key: str) -> None:
        self._stored_key = (key or "").strip()
        self._settings.setValue("claude/api_key", self._stored_key)

    def set_max(self, n: int) -> None:
        self.max_per_hour = int(n)
        self._settings.setValue("claude/max_per_hour", self.max_per_hour)

    def sdk_ok(self) -> bool:
        return self._sdk

    def available(self) -> bool:
        return self._sdk and bool(self.api_key)

    def status(self) -> str:
        if not self._sdk:
            return "missing"
        if not self.api_key:
            return "nokey"
        return "ready"

    # ── budget (call on the main thread) ──
    def try_reserve(self, now: float) -> bool:
        cutoff = now - 3600
        self._calls = [t for t in self._calls if t >= cutoff]
        if len(self._calls) >= self.max_per_hour:
            return False
        self._calls.append(now)
        return True

    # ── verification (called off the main thread) ──
    # Returns (answer, reason) where answer is True | False | None.
    # None means "could not verify" (encode/network/parse error) — distinct from a
    # definite "no", so the caller can fail open instead of silently suppressing.
    def verify(self, frame_bgr, question: str):
        try:
            import cv2
            from anthropic import Anthropic

            frame = frame_bgr
            height, width = frame.shape[:2]
            if width > _MAX_WIDTH:
                scale = _MAX_WIDTH / width
                frame = cv2.resize(frame, (_MAX_WIDTH, int(height * scale)))
            ok, buffer = cv2.imencode(".jpg", frame)
            if not ok:
                return None, "encode failed"
            b64 = base64.b64encode(buffer.tobytes()).decode("ascii")

            client = Anthropic(api_key=self.api_key, timeout=VERIFY_TIMEOUT, max_retries=0)
            prompt = (
                "You are a vigilant security-camera assistant. Look at the image and answer "
                "this yes/no question about what is happening in the frame RIGHT NOW.\n"
                f"Question: {question}\n"
                'Reply with ONLY a compact JSON object: '
                '{"answer": true or false, "reason": "<= 12 words"}.'
            )
            response = client.messages.create(
                model=MODEL,
                max_tokens=200,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {
                            "type": "base64", "media_type": "image/jpeg", "data": b64}},
                        {"type": "text", "text": prompt},
                    ],
                }],
            )
            text = "".join(
                block.text for block in response.content if getattr(block, "type", "") == "text"
            ).strip()
            return self._parse(text)
        except Exception as exc:
            return None, f"error: {exc}"[:60]

    @staticmethod
    def _truthy(value):
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(value)
        if isinstance(value, str):
            low = value.strip().lower()
            if low in {"true", "yes", "1"}:
                return True
            if low in {"false", "no", "0"}:
                return False
        return None

    @staticmethod
    def _parse(text: str):
        reason = ""
        answer = None
        try:
            start = text.index("{")
            end = text.rindex("}") + 1
            data = json.loads(text[start:end])
            reason = str(data.get("reason", ""))[:60]
            answer = ClaudeClient._truthy(data.get("answer"))
        except Exception:
            answer = None
        if answer is not None:
            return answer, reason
        low = text.strip().lower()
        if low.startswith("yes"):
            return True, reason
        if low.startswith("no"):
            return False, reason
        return None, reason
