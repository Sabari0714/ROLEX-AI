from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LOG_DIR = ROOT / "logs"
DB_PATH = DATA_DIR / "rolex.db"
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


def _load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    try:
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
    except OSError:
        pass


_load_dotenv(ROOT / ".env")
# Safe defaults: hosted AI and network retrieval are opt-in.
EXTERNAL_AI_DISABLED = os.getenv("ROLEX_EXTERNAL_AI", "1").lower() in {"1", "true", "yes"}
ALLOW_NETWORK = os.getenv("ROLEX_ALLOW_NETWORK", "0").lower() in {"1", "true", "yes"}
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "").strip()
LOCAL_LLM_ENDPOINT = os.getenv("ROLEX_LOCAL_LLM_ENDPOINT", "").strip()
APP_NAME = "ROLEX AI"
LANGUAGES = ("ta", "en", "tanglish")
MEMORY_LIMIT = 5000
