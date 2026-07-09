"""Send notifications to the desktop (macOS Notification Center) and, optionally,
to your phone via the free ntfy.sh service.

Phone push is strictly opt-in: nothing leaves the machine unless the user sets a
topic. Settings persist across launches via QSettings. All sends are best-effort
and never raise into the UI.
"""

import subprocess
import threading
import urllib.request

from PySide6.QtCore import QSettings


class Notifier:
    def __init__(self):
        self._settings = QSettings("BigBrother", "BigBrother")
        self.desktop_enabled = self._settings.value("notify/desktop", True, type=bool)
        self.ntfy_topic = self._settings.value("notify/ntfy", "", type=str)

    # ── settings ──
    def set_desktop(self, enabled: bool) -> None:
        self.desktop_enabled = bool(enabled)
        self._settings.setValue("notify/desktop", self.desktop_enabled)

    def set_topic(self, topic: str) -> None:
        self.ntfy_topic = (topic or "").strip()
        self._settings.setValue("notify/ntfy", self.ntfy_topic)

    # ── sending ──
    def send(self, title: str, message: str) -> None:
        if self.desktop_enabled:
            self._desktop(title, message)
        if self.ntfy_topic:
            self._ntfy(self.ntfy_topic, title, message)

    def _desktop(self, title: str, message: str) -> None:
        safe_title = title.replace('"', "'")
        safe_message = message.replace('"', "'")
        try:
            subprocess.Popen(
                ["osascript", "-e",
                 f'display notification "{safe_message}" with title "{safe_title}"']
            )
        except Exception:
            pass

    def _ntfy(self, topic: str, title: str, message: str) -> None:
        def worker():
            try:
                request = urllib.request.Request(
                    f"https://ntfy.sh/{topic}",
                    data=message.encode("utf-8"),
                    headers={"Title": title, "Tags": "eye"},
                    method="POST",
                )
                urllib.request.urlopen(request, timeout=8)
            except Exception:
                pass

        threading.Thread(target=worker, daemon=True).start()
