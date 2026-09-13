# Contributing

Thanks for improving this starter.

## Workflow

1. Fork or branch from `develop` / `main`.
2. Keep changes focused and covered by tests.
3. Run quality checks before opening a PR:

```bash
poetry install
poetry run python scripts/setup_dev.py
poetry run ruff check app tests
poetry run ruff format app tests
poetry run mypy app
poetry run bandit -r app -ll
poetry run python scripts/export_schema.py
poetry run pytest
```

4. Use Commitizen for commit messages:

```bash
poetry run cz commit
```

5. Open a pull request against `develop` or `main`.

## Notes

- Do not commit secrets. Use `.env.example` / `.env.test.example` as templates.
- Prefer extending use cases over putting business rules in routers or resolvers.
- Keep REST and GraphQL presentation layers thin and shared over the same application layer.
