import asyncio
from pathlib import Path

from httpx import ASGITransport, AsyncClient

from app.infrastructure.database.seed import seed_initial_users
from app.infrastructure.services.security.password_hasher_impl import Argon2PasswordHasher
from app.main import app
from app.presentation.rest.utils.dependencies import get_uow


async def main() -> None:
    await seed_initial_users(uow=get_uow(), password_hasher=Argon2PasswordHasher())
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        health = await client.get("/health")
        assert health.status_code == 200 and health.json()["database"] == "ok"

        swagger = await client.get("/api_docs")
        assert swagger.status_code == 200

        login = await client.post(
            "/auth/login", data={"username": "admin", "password": "admin"}
        )
        assert login.status_code == 200, login.text
        assert login.json()["access_token"]

        gql = await client.post("/graphql", json={"query": "{ __typename }"})
        assert gql.status_code == 200 and gql.json()["data"]["__typename"] == "Query"

    print("OK", Path.cwd().name)


if __name__ == "__main__":
    asyncio.run(main())
