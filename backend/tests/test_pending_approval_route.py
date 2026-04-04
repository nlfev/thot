"""
Unittests for /users/pending-approval route
"""
import pytest
from app.models import Role, User, UserRole
from app.utils import create_access_token, hash_password
from sqlalchemy.orm import Session


def _create_user_with_role(db: Session, username: str, email: str, role_name: str, active=True, corporate_approved=False, corporate_number=None):
    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        role = Role(name=role_name, description=f"{role_name} role", active=True)
        db.add(role)
        db.flush()
    user = User(
        username=username,
        email=email,
        hashed_password=hash_password("TestPassword123!"),
        active=active,
        corporate_approved=corporate_approved,
        corporate_number=corporate_number,
    )
    db.add(user)
    db.flush()
    db.add(UserRole(user_id=user.id, role_id=role.id, active=True))
    db.commit()
    db.refresh(user)
    return user

def _auth_headers_for_user(user: User) -> dict:
    token = create_access_token(str(user.id))
    return {"Authorization": f"Bearer {token}", "Host": "localhost"}


def test_pending_approval_count_only_active_with_corporate_number(client, db):
    """
    Only users with active=True, corporate_approved=False, and non-empty corporate_number are counted.
    """
    # Setup roles
    admin = _create_user_with_role(db, "admin", "admin@example.com", "admin")
    support = _create_user_with_role(db, "support", "support@example.com", "support")
    # Users to be counted
    u1 = _create_user_with_role(db, "user1", "u1@example.com", "user", active=True, corporate_approved=False, corporate_number="12345")
    # Not counted: inactive
    u2 = _create_user_with_role(db, "user2", "u2@example.com", "user", active=False, corporate_approved=False, corporate_number="12345")
    # Not counted: already approved
    u3 = _create_user_with_role(db, "user3", "u3@example.com", "user", active=True, corporate_approved=True, corporate_number="12345")
    # Not counted: no corporate_number
    u4 = _create_user_with_role(db, "user4", "u4@example.com", "user", active=True, corporate_approved=False, corporate_number=None)
    u5 = _create_user_with_role(db, "user5", "u5@example.com", "user", active=True, corporate_approved=False, corporate_number="   ")

    # Admin request
    headers = _auth_headers_for_user(admin)
    resp = client.get("/api/v1/users/pending-approval", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["pending_approval_count"] == 1

    # Support request
    headers = _auth_headers_for_user(support)
    resp = client.get("/api/v1/users/pending-approval", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["pending_approval_count"] == 1

    # User request (forbidden)
    user_headers = _auth_headers_for_user(u1)
    resp = client.get("/api/v1/users/pending-approval", headers=user_headers)
    assert resp.status_code == 403
    assert "Insufficient permissions" in resp.json()["detail"]
