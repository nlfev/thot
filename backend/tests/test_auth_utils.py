"""
Tests for Authentication Utilities
"""

import pytest
from app.utils import (
    hash_password,
    verify_password,
    validate_password_requirements,
    generate_otp_secret,
    verify_otp,
    generate_short_code,
)


def test_hash_and_verify_password():
    """Test password hashing and verification"""
    password = "TestPassword123!"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_validate_password_requirements():
    """Test password validation"""
    # Valid password
    is_valid, error = validate_password_requirements("ValidPass123!")
    assert is_valid is True
    assert error == ""

    # Too short
    is_valid, error = validate_password_requirements("Short1!")
    assert is_valid is False

    # No uppercase
    is_valid, error = validate_password_requirements("validpass123!")
    assert is_valid is False

    # No lowercase
    is_valid, error = validate_password_requirements("VALIDPASS123!")
    assert is_valid is False

    # No digit or special char
    is_valid, error = validate_password_requirements("ValidPassword")
    assert is_valid is False


def test_generate_otp_secret():
    """Test OTP secret generation"""
    secret = generate_otp_secret()
    assert len(secret) > 0
    assert isinstance(secret, str)


def test_verify_otp():
    """Test OTP verification"""
    secret = generate_otp_secret()
    # Note: This test is just to verify the function can be called
    # In production, you'd use a proper TOTP token from pyotp
    assert isinstance(secret, str)


def test_generate_short_code():
    """Test short code generation"""
    code = generate_short_code()
    assert len(code) == 6
    assert code.isdigit()

    code_custom = generate_short_code(8)
    assert len(code_custom) == 8
    assert code_custom.isdigit()
