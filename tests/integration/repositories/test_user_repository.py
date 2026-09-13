from uuid import uuid4

from app.domain.entities.user import User
from app.domain.value_objects.role import Role


async def test_user_repository_create_and_get(uow):
    async with uow:
        created = await uow.users.create(
            User(
                username=f"user_{uuid4().hex[:8]}",
                password_hash="hash",
                name="Test",
                active=True,
                role=Role.MEMBER,
            )
        )
        await uow.commit()

    async with uow:
        found = await uow.users.get(created.safe_id)
        assert found is not None
        assert found.username == created.username
