import pytest


async def _login(client, username: str = "admin", password: str = "admin"):
    response = await client.post(
        "/auth/login",
        data={"username": username, "password": password},
        headers={"User-Agent": "e2e-test-agent"},
    )
    assert response.status_code == 200, response.text
    return response.json()


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "ok"
    assert "timestamp" in body


@pytest.mark.asyncio
async def test_login_admin(client):
    body = await _login(client)
    assert "access_token" in body
    assert "refresh_token" in body


@pytest.mark.asyncio
async def test_refresh_and_me(client):
    tokens = await _login(client)
    refresh = await client.post(
        "/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
        headers={"User-Agent": "e2e-test-agent"},
    )
    assert refresh.status_code == 200, refresh.text
    new_tokens = refresh.json()
    assert new_tokens["access_token"]

    me = await client.get(
        "/user/me",
        headers={"Authorization": f"Bearer {new_tokens['access_token']}"},
    )
    assert me.status_code == 200, me.text
    assert me.json()["username"] == "admin"


@pytest.mark.asyncio
async def test_admin_create_and_list_users(client):
    tokens = await _login(client)
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}

    created = await client.post(
        "/user/createUser",
        headers=headers,
        json={
            "name": "E2E User",
            "username": "e2e_user",
            "password": "password123",
            "role": "Member",
        },
    )
    assert created.status_code == 201, created.text
    assert created.json()["username"] == "e2e_user"

    listed = await client.get("/user", headers=headers)
    assert listed.status_code == 200, listed.text
    body = listed.json()
    assert body["total"] >= 1
    usernames = {row["username"] for row in body["items"]}
    assert "e2e_user" in usernames


@pytest.mark.asyncio
async def test_bilingual_auth_error(client):
    response = await client.post(
        "/auth/logIn",
        json={"username": "missing", "password": "wrong"},
        headers={"Accept-Language": "fa"},
    )
    assert response.status_code == 401
    body = response.json()
    assert body["persianTranslation"]
    assert body["message"] == body["persianTranslation"]


@pytest.mark.asyncio
async def test_graphql_login(client):
    query = """
    mutation Login($input: LoginInput!) {
      login(input: $input) {
        accessToken
        refreshToken
      }
    }
    """
    response = await client.post(
        "/graphql",
        json={
            "query": query,
            "variables": {
                "input": {"username": "admin", "password": "admin"},
            },
        },
        headers={"User-Agent": "e2e-test-agent"},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert not body.get("errors"), body
    assert body["data"]["login"]["accessToken"]


@pytest.mark.asyncio
async def test_graphql_me(client):
    login_query = """
    mutation Login($input: LoginInput!) {
      login(input: $input) { accessToken }
    }
    """
    login = await client.post(
        "/graphql",
        json={
            "query": login_query,
            "variables": {"input": {"username": "admin", "password": "admin"}},
        },
        headers={"User-Agent": "e2e-test-agent"},
    )
    token = login.json()["data"]["login"]["accessToken"]

    me_query = "{ me { username role } }"
    response = await client.post(
        "/graphql",
        json={"query": me_query},
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "e2e-test-agent",
        },
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert not body.get("errors"), body
    assert body["data"]["me"]["username"] == "admin"
