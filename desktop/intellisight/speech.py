"""Text-to-speech using the macOS built-in `say` command (no dependencies)."""

import shutil
import subprocess


class Speech:
    def __init__(self):
        self._say = shutil.which("say")
        self._proc = None

    def available(self) -> bool:
        return self._say is not None

    def speak(self, text: str) -> None:
        if not self._say or not text:
            return
        self.stop()
        try:
            self._proc = subprocess.Popen([self._say, text])
        except Exception:
            self._proc = None

    def stop(self) -> None:
        if self._proc is not None and self._proc.poll() is None:
            try:
                self._proc.terminate()
            except Exception:
                pass
        self._proc = None
