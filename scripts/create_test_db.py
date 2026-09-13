"""Create the integration test database if it does not exist."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from app.core.config import settings


def main() -> None:
    conn = psycopg2.connect(
        host=settings.POSTGRES_HOST_TEST,
        user=settings.POSTGRES_USER_TEST,
        password=settings.POSTGRES_PASSWORD_TEST,
        port=settings.POSTGRES_PORT_TEST,
        database="postgres",
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM pg_database WHERE datname=%s",
        (settings.POSTGRES_DB_TEST,),
    )
    if cur.fetchone():
        print(f"Exists {settings.POSTGRES_DB_TEST}")
    else:
        cur.execute(f'CREATE DATABASE "{settings.POSTGRES_DB_TEST}"')
        print(f"Created {settings.POSTGRES_DB_TEST}")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
