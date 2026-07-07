"""Speech-to-text: record from the mic and transcribe locally with faster-whisper.

The extra packages (sounddevice, faster-whisper) are optional — if they're not
installed, `available()` explains how to add them and the rest of the app is
unaffected.
"""

from PySide6.QtCore import QThread, Signal

SAMPLE_RATE = 16000
_INSTALL_HINT = (
    "Voice input needs a couple of extra packages. In the desktop/ folder run:\n"
    "  brew install portaudio\n"
    "  .venv/bin/pip install -r requirements-voice.txt"
)


class VoiceInput:
    """Records mic audio and transcribes it (both steps are optional/lazy)."""

    def __init__(self):
        self._stream = None
        self._frames = []
        self._model = None

    def available(self):
        try:
            import faster_whisper  # noqa: F401
            import sounddevice  # noqa: F401

            return True, ""
        except Exception:
            return False, _INSTALL_HINT

    def start(self) -> None:
        import sounddevice as sd

        self._frames = []

        def callback(indata, frames, time_info, status):
            self._frames.append(indata.copy())

        self._stream = sd.InputStream(
            samplerate=SAMPLE_RATE, channels=1, dtype="float32", callback=callback
        )
        self._stream.start()

    def stop(self):
        """Stop recording and return the captured audio (mono float32) or None."""
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass
            self._stream = None
        if not self._frames:
            return None
        import numpy as np

        return np.concatenate(self._frames, axis=0).flatten()

    def transcribe(self, audio) -> str:
        from faster_whisper import WhisperModel

        if self._model is None:
            # "base" is a good balance; downloads once (~140 MB) then runs offline.
            self._model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, _ = self._model.transcribe(audio, language="en")
        return " ".join(segment.text for segment in segments).strip()


class TranscribeWorker(QThread):
    """Runs transcription off the UI thread."""

    transcribed = Signal(str)
    error = Signal(str)

    def __init__(self, voice: VoiceInput, audio, parent=None):
        super().__init__(parent)
        self._voice = voice
        self._audio = audio

    def run(self) -> None:
        try:
            self.transcribed.emit(self._voice.transcribe(self._audio))
        except Exception:
            self.error.emit("Sorry — I couldn't transcribe that. Try again.")
