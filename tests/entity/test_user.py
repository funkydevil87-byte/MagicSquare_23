from __future__ import annotations

import uuid

import pytest

from magicsquare.entity.user import User


def test_user_create_valid() -> None:
    # Arrange
    user_id = uuid.uuid4()

    # Act
    user = User(user_id=user_id, name="Alice")

    # Assert
    assert user.user_id == user_id
    assert user.name == "Alice"


@pytest.mark.parametrize("bad_name", ["", "   ", "\n\t"])
def test_user_create_rejects_blank_name(bad_name: str) -> None:
    # Arrange
    user_id = uuid.uuid4()

    # Act / Assert
    with pytest.raises(ValueError, match="name must be non-empty"):
        User(user_id=user_id, name=bad_name)


def test_user_rename_returns_new_instance() -> None:
    # Arrange
    user_id = uuid.uuid4()
    user = User(user_id=user_id, name="Alice")

    # Act
    renamed = user.rename("Bob")

    # Assert
    assert renamed is not user
    assert renamed.user_id == user_id
    assert renamed.name == "Bob"
    assert user.name == "Alice"


def test_user_rename_rejects_blank_name() -> None:
    # Arrange
    user = User(user_id=uuid.uuid4(), name="Alice")

    # Act / Assert
    with pytest.raises(ValueError, match="name must be non-empty"):
        user.rename("   ")

