"""App configuration — reads from environment variables and an optional .env file.

Put your Claude API key in `desktop/.env` (see `.env.example`) to enable the AI
features (scene understanding, chat, etc.). Everything else has a sensible default.
"""

import os
from pathlib import Path


def _load_env_file() -> dict:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    values = {}
    if env_path.exists():
        try:
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                values[key.strip()] = val.strip().strip('"').strip("'")
        except OSError:
            pass
    return values


_ENV = _load_env_file()


def _get(name: str, default=None):
    return os.environ.get(name) or _ENV.get(name) or default


def get_api_key():
    """The Anthropic API key, from the environment or desktop/.env (or None)."""
    return _get("ANTHROPIC_API_KEY")


# Anthropic recommends the most capable model by default. To trade some quality
# for lower cost / faster responses, set INTELLISIGHT_SCENE_MODEL=claude-haiku-4-5
# in your .env.
SCENE_MODEL = _get("INTELLISIGHT_SCENE_MODEL", "claude-opus-4-8")


def scene_interval_seconds() -> float:
    """How often to ask the AI to re-describe the scene (min 6s)."""
    try:
        return max(6.0, float(_get("INTELLISIGHT_SCENE_INTERVAL", "15")))
    except (TypeError, ValueError):
        return 15.0
