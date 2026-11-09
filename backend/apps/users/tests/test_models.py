"""Tests for the custom User model."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


@pytest.mark.django_db
def test_user_can_be_created() -> None:
    user = User.objects.create_user(
        username="alice",
        email="alice@example.com",
        password="secure-password-123",
    )

    assert user.pk is not None
    assert user.username == "alice"
    assert user.email == "alice@example.com"
    assert user.is_active is True
    assert user.is_staff is False


@pytest.mark.django_db
def test_password_is_stored_as_hash() -> None:
    password = "secure-password-123"
    user = User.objects.create_user(
        username="bob",
        email="bob@example.com",
        password=password,
    )

    assert user.password != password
    assert user.password.startswith("pbkdf2_")
    assert user.check_password(password)


@pytest.mark.django_db
def test_user_can_be_retrieved() -> None:
    created = User.objects.create_user(
        username="carol",
        email="carol@example.com",
        password="secure-password-123",
    )

    retrieved = User.objects.get(username="carol")

    assert retrieved.pk == created.pk
    assert retrieved.email == "carol@example.com"


@pytest.mark.django_db
def test_email_uniqueness_is_enforced() -> None:
    User.objects.create_user(
        username="dave",
        email="shared@example.com",
        password="secure-password-123",
    )

    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username="erin",
            email="shared@example.com",
            password="secure-password-123",
        )


@pytest.mark.django_db
def test_username_uniqueness_is_enforced() -> None:
    User.objects.create_user(
        username="frank",
        email="frank@example.com",
        password="secure-password-123",
    )

    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username="frank",
            email="frank2@example.com",
            password="secure-password-123",
        )
