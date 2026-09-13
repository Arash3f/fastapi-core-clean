"""Bootstrap local development: install deps and Git hooks.

Usage (from repo root):
  poetry run python scripts/setup_dev.py
  # or, after poetry install:
  python scripts/setup_dev.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    poetry = shutil.which("poetry")
    if poetry is None:
        print(
            "Poetry is required. Install from https://python-poetry.org/",
            file=sys.stderr,
        )
        return 1

    _run([poetry, "install", "--no-interaction"])

    env_example = ROOT / ".env.example"
    env_file = ROOT / ".env"
    if env_example.exists() and not env_file.exists():
        env_file.write_text(env_example.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Created {env_file.name} from {env_example.name}")

    # Install hooks into .git/hooks for this clone
    _run([poetry, "run", "pre-commit", "install"])
    _run([poetry, "run", "pre-commit", "install", "--hook-type", "pre-push"])
    _run([poetry, "run", "pre-commit", "install", "--hook-type", "commit-msg"])

    print("\nDev setup complete.")
    print("Next: poetry run alembic upgrade head")
    print("Then: poetry run uvicorn app.main:app --reload")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
