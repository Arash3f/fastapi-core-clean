"""Export the Strawberry GraphQL schema to schema.graphql."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.presentation.graphql.schema import schema

TARGET = ROOT / "schema.graphql"


def main() -> None:
    TARGET.write_text(schema.as_str().strip() + "\n", encoding="utf-8")
    print(f"Wrote {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
