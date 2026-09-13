from app.domain.entities.user import User
from app.domain.exceptions.common_exceptions import UnexpectedIdException
from app.domain.value_objects.role import Role
import pytest


def test_user_safe_id_raises_when_missing():
    user = User(
        username="a",
        password_hash="h",
        name="A",
        active=True,
        role=Role.MEMBER,
    )
    with pytest.raises(UnexpectedIdException):
        _ = user.safe_id
