"""POST rule events as JSON to any URL — the automation bridge.

Used by the 'Send a webhook' rule action to feed events into Home Assistant,
Slack/Discord, MQTT gateways, or your own scripts. Best-effort and off-thread;
never raises into the UI.
"""

import json
import threading
import urllib.request


def send_webhook(url: str, payload: dict) -> None:
    url = (url or "").strip()
    if not url:
        return

    def worker():
        try:
            data = json.dumps(payload).encode("utf-8")
            request = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json", "User-Agent": "BigBrother"},
                method="POST",
            )
            urllib.request.urlopen(request, timeout=8)
        except Exception:
            pass

    threading.Thread(target=worker, daemon=True).start()
