import os
from pathlib import Path

# Ensure settings load with throttle disabled and test DB before app imports.
os.environ.setdefault("APP_ENV", "test")

_env_test = Path(__file__).resolve().parent.parent / ".env.test"
if _env_test.exists():
    from dotenv import load_dotenv

    load_dotenv(_env_test, override=False)
