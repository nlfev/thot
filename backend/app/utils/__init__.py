"""
Utilities package
"""

from .auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    get_current_user,
    generate_email_token,
    generate_otp_secret,
    verify_otp,
    get_otp_qr_code,
    generate_short_code,
    validate_password_requirements,
    is_password_reset_needed,
)
from .email_service import email_service, EmailService

__all__ = [
    "hash_password",
    "verify_password",
    "create_access_token",
    "decode_access_token",
    "get_current_user",
    "generate_email_token",
    "generate_otp_secret",
    "verify_otp",
    "get_otp_qr_code",
    "generate_short_code",
    "validate_password_requirements",
    "is_password_reset_needed",
    "email_service",
    "EmailService",
]
