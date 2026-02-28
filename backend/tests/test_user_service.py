"""
Tests for User Service
"""

import pytest
from datetime import datetime
from app.services import UserService
from app.models import User, Role
from app.utils import verify_password, hash_password
import uuid


@pytest.fixture
def setup_roles(db):
    """Setup default roles"""
    admin_role = Role(
        id=uuid.uuid4(),
        name="admin",
        description="Admin role",
        active=True,
        created_on=datetime.utcnow()
    )
    user_role = Role(
        id=uuid.uuid4(),
        name="user",
        description="User role",
        active=True,
        created_on=datetime.utcnow()
    )
    db.add(admin_role)
    db.add(user_role)
    db.commit()
    return {"admin": admin_role, "user": user_role}


def test_create_user(db, setup_roles):
    """Test creating a new user"""
    user = UserService.create_user(
        db=db,
        username="testuser",
        email="test@example.com",
        password="TestPassword123!",
        first_name="Test",
        last_name="User",
        is_first_user=False
    )

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert verify_password("TestPassword123!", user.hashed_password)


def test_create_first_user_as_admin(db, setup_roles):
    """Test that first user gets admin role"""
    user = UserService.create_user(
        db=db,
        username="admin",
        email="admin@example.com",
        password="AdminPassword123!",
        is_first_user=True
    )

    assert len(user.user_roles) > 0
    assert any(ur.role.name == "admin" for ur in user.user_roles)


def test_get_user_by_username(db, setup_roles):
    """Test getting user by username"""
    UserService.create_user(
        db=db,
        username="testuser",
        email="test@example.com",
        password="TestPassword123!",
        is_first_user=False
    )

    user = UserService.get_user_by_username(db, "testuser")
    assert user is not None
    assert user.username == "testuser"


def test_get_user_by_email(db, setup_roles):
    """Test getting user by email"""
    UserService.create_user(
        db=db,
        username="testuser",
        email="test@example.com",
        password="TestPassword123!",
        is_first_user=False
    )

    user = UserService.get_user_by_email(db, "test@example.com")
    assert user is not None
    assert user.email == "test@example.com"


def test_authenticate_user_success(db, setup_roles):
    """Test successful user authentication"""
    UserService.create_user(
        db=db,
        username="testuser",
        email="test@example.com",
        password="TestPassword123!",
        is_first_user=False
    )

    user, error = UserService.authenticate_user(
        db=db,
        username="testuser",
        password="TestPassword123!"
    )

    assert user is not None
    assert user.username == "testuser"
    assert error == ""
    assert user.unsuccessful_logins == 0


def test_authenticate_user_invalid_password(db, setup_roles):
    """Test authentication with invalid password"""
    UserService.create_user(
        db=db,
        username="testuser",
        email="test@example.com",
        password="TestPassword123!",
        is_first_user=False
    )

    user, error = UserService.authenticate_user(
        db=db,
        username="testuser",
        password="WrongPassword123!"
    )

    assert user is None
    assert error != ""

    # Check that unsuccessful logins counter increased
    user_from_db = UserService.get_user_by_username(db, "testuser")
    assert user_from_db.unsuccessful_logins == 1


def test_update_user_profile(db, setup_roles):
    """Test updating user profile"""
    user = UserService.create_user(
        db=db,
        username="testuser",
        email="test@example.com",
        password="TestPassword123!",
        first_name="Test",
        last_name="User",
        is_first_user=False
    )

    updated_user = UserService.update_user_profile(
        db=db,
        user_id=str(user.id),
        first_name="Updated",
        last_name="Name",
        current_language="de"
    )

    assert updated_user.first_name == "Updated"
    assert updated_user.last_name == "Name"
    assert updated_user.current_language == "de"


def test_change_password(db, setup_roles):
    """Test changing password"""
    user = UserService.create_user(
        db=db,
        username="testuser",
        email="test@example.com",
        password="OldPassword123!",
        is_first_user=False
    )

    success, message = UserService.change_password(
        db=db,
        user_id=str(user.id),
        current_password="OldPassword123!",
        new_password="NewPassword456!"
    )

    assert success is True
    
    # Verify new password works
    user_updated, error = UserService.authenticate_user(
        db=db,
        username="testuser",
        password="NewPassword456!"
    )
    assert user_updated is not None
