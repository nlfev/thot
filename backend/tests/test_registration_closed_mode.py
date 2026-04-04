"""Tests for closed registration behavior."""

from datetime import datetime, timedelta, timezone
import uuid
from pathlib import Path

from config import config
from app.models import Role, User, UserConfirmation, UserConfirmations, UserRegistration
from app.services.registration_service import RegistrationService
from app.utils.email_service import email_service


def _host_headers():
    return {"Host": "localhost"}


def _create_role(db, name: str):
    role = Role(id=uuid.uuid4(), name=name, description=f"{name} role")
    db.add(role)
    db.commit()
    return role


def _create_user(db, username: str, email: str):
    user = User(
        id=uuid.uuid4(),
        username=username,
        email=email,
        hashed_password="hashed",
        first_name="Test",
        last_name="User",
        current_language="en",
    )
    db.add(user)
    db.commit()
    return user


def test_public_config_keeps_bootstrap_registration_open(client, monkeypatch):
    monkeypatch.setattr(config, "CLOSED_REGISTRATION", True)

    response = client.get("/api/v1/config", headers=_host_headers())

    assert response.status_code == 200
    payload = response.json()
    assert payload["features"]["closedRegistrationConfigured"] is True
    assert payload["features"]["closedRegistration"] is False
    assert payload["legalContent"]["termsOfServiceUrl"] == "/api/v1/config/legal/terms-of-service"


def test_legal_content_endpoint_reads_language_specific_html(client, monkeypatch, tmp_path: Path):
    monkeypatch.setattr(type(config), "LEGAL_CONTENT_DIRECTORY", tmp_path.resolve())

    imprint_file = tmp_path / "imprint.de.html"
    imprint_file.write_text("<h1>Impressum Test</h1>", encoding="utf-8")

    response = client.get("/api/v1/config/legal/imprint?lang=de", headers=_host_headers())

    assert response.status_code == 200
    assert "Impressum Test" in response.text


def test_legal_content_endpoint_returns_404_when_file_missing(client, monkeypatch, tmp_path: Path):
    monkeypatch.setattr(type(config), "LEGAL_CONTENT_DIRECTORY", tmp_path.resolve())

    response = client.get("/api/v1/config/legal/terms-of-service?lang=en", headers=_host_headers())

    assert response.status_code == 404
    assert "Legal content file not found" in response.json()["detail"]



def test_legal_content_endpoint_returns_404_when_not_allowed(client, monkeypatch, tmp_path: Path):
    monkeypatch.setattr(type(config), "LEGAL_CONTENT_DIRECTORY", tmp_path.resolve())

    response = client.get("/api/v1/config/legal/imprints?lang=de", headers=_host_headers())

    assert response.status_code == 404
    assert "Legal document not found" in response.json()["detail"]


def test_legal_content_endpoint_reads_500_wrong_encoding(client, monkeypatch, tmp_path: Path):
    monkeypatch.setattr(type(config), "LEGAL_CONTENT_DIRECTORY", tmp_path.resolve())

    imprint_file = tmp_path / "imprint.de.html"
    imprint_file.write_text("<h1>Impressum Testö</h1>", encoding="latin-1")

    response = client.get("/api/v1/config/legal/imprint?lang=de", headers=_host_headers())

    assert response.status_code == 500
    assert "Failed to read legal content file" in response.json()["detail"]


def test_bootstrap_registration_still_requires_tos(client, monkeypatch):
    monkeypatch.setattr(config, "CLOSED_REGISTRATION", True)

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "bootstrap-admin",
            "email": "bootstrap@example.com",
            "tos_agreed": False,
            "language": "en",
        },
        headers=_host_headers(),
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "You must agree to the Terms of Service"


def test_closed_registration_blocks_anonymous_users_after_first_user(client, db, monkeypatch):
    monkeypatch.setattr(config, "CLOSED_REGISTRATION", True)
    _create_user(db, "existing-admin", "existing@example.com")

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "blocked-user",
            "email": "blocked@example.com",
            "tos_agreed": False,
            "language": "en",
        },
        headers=_host_headers(),
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Registration is currently limited to support and admin users"


def test_registration_trims_username_before_persisting(client, db, monkeypatch):
    monkeypatch.setattr(config, "CLOSED_REGISTRATION", False)
    monkeypatch.setattr(email_service, "send_registration_confirmation_email", lambda **kwargs: True)

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "  trimmed-user  ",
            "email": "trimmed@example.com",
            "tos_agreed": True,
            "language": "en",
        },
        headers=_host_headers(),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["username"] == "trimmed-user"

    registration = db.query(UserRegistration).filter(UserRegistration.email == "trimmed@example.com").one()
    assert registration.username == "trimmed-user"


def test_registration_rejects_existing_username_after_trim(client, db, monkeypatch):
    monkeypatch.setattr(config, "CLOSED_REGISTRATION", False)
    monkeypatch.setattr(email_service, "send_registration_confirmation_email", lambda **kwargs: True)
    _create_user(db, "existing-user", "existing-user@example.com")

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "  existing-user  ",
            "email": "another@example.com",
            "tos_agreed": True,
            "language": "en",
        },
        headers=_host_headers(),
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"


def test_registration_rejects_username_shorter_than_five_after_trim(client, monkeypatch):
    monkeypatch.setattr(config, "CLOSED_REGISTRATION", False)

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "  abcd  ",
            "email": "short@example.com",
            "tos_agreed": True,
            "language": "en",
        },
        headers=_host_headers(),
    )

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("Username must be at least 5 characters" in error["msg"] for error in errors)


def test_open_registration_tos_confirmation_uses_current_timestamp(db):
    _create_role(db, "user")
    confirmation = UserConfirmation(
        id=uuid.uuid4(),
        confirmation="Terms of Service",
        confirmation_short="ToS",
    )
    db.add(confirmation)

    registration = UserRegistration(
        id=uuid.uuid4(),
        username="open-user",
        email="open@example.com",
        token="open-token",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        admin=False,
    )
    db.add(registration)
    db.commit()

    started_at = datetime.now(timezone.utc).replace(tzinfo=None)
    user, _, error = RegistrationService.complete_registration(
        db=db,
        token="open-token",
        first_name="Open",
        last_name="User",
        password="ValidPass123!",
        tos_agreed=False,
        current_language="en",
    )
    finished_at = datetime.now(timezone.utc).replace(tzinfo=None)

    assert error is None
    assert user is not None

    stored_confirmation = db.query(UserConfirmations).filter(UserConfirmations.userid == user.id).one()
    assert started_at <= stored_confirmation.created_on <= finished_at


def test_admin_registration_tos_confirmation_uses_current_timestamp(db):
    _create_role(db, "user")
    _create_user(db, "seed-user", "seed@example.com")
    confirmation = UserConfirmation(
        id=uuid.uuid4(),
        confirmation="Terms of Service",
        confirmation_short="ToS",
    )
    db.add(confirmation)

    historical_created_on = datetime(2026, 3, 10, 8, 30, tzinfo=timezone.utc)
    registration = UserRegistration(
        id=uuid.uuid4(),
        username="admin-created-user",
        email="admin-created@example.com",
        token="admin-token",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        admin=True,
    )
    db.add(registration)
    db.commit()

    started_at = datetime.now(timezone.utc).replace(tzinfo=None)
    user, _, error = RegistrationService.complete_registration(
        db=db,
        token="admin-token",
        first_name="Admin",
        last_name="Created",
        password="ValidPass123!",
        tos_agreed=True,
        current_language="en",
    )
    finished_at = datetime.now(timezone.utc).replace(tzinfo=None)

    assert error is None
    assert user is not None

    stored_confirmation = db.query(UserConfirmations).filter(UserConfirmations.userid == user.id).one()
    assert started_at <= stored_confirmation.created_on <= finished_at
