"""
Registration service for user registration logic
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple, Dict
from sqlalchemy.orm import Session
import uuid
import secrets
import logging
import pyotp
import qrcode
import io
import base64

from app.models import User, UserRegistration, Role, UserRole
from app.utils import hash_password
from config import config

logger = logging.getLogger(__name__)


class RegistrationService:
    """Service for user registration operations"""

    @staticmethod
    def cleanup_expired_registrations(db: Session) -> int:
        """
        Delete expired registration entries
        Returns: number of deleted entries
        """
        try:
            now = datetime.now(timezone.utc)
            expired = (
                db.query(UserRegistration)
                .filter(UserRegistration.expires_at < now)
                .all()
            )
            count = len(expired)
            
            for reg in expired:
                db.delete(reg)
            
            db.commit()
            logger.info(f"Cleaned up {count} expired registration(s)")
            return count
        except Exception as e:
            db.rollback()
            logger.error(f"Error cleaning up expired registrations: {str(e)}")
            return 0

    @staticmethod
    def check_username_available(db: Session, username: str) -> bool:
        """
        Check if username is available (not in users table or user_registrations table)
        """
        # Check in users table
        user_exists = db.query(User).filter(User.username == username).first()
        if user_exists:
            return False

        # Check in user_registrations table
        registration_exists = (
            db.query(UserRegistration)
            .filter(UserRegistration.username == username)
            .first()
        )
        if registration_exists:
            return False

        return True

    @staticmethod
    def initiate_registration(
        db: Session, username: str, email: str
    ) -> Tuple[Optional[UserRegistration], Optional[str]]:
        """
        Initiate registration process
        Returns: (UserRegistration, error_message)
        """
        try:
            # Cleanup expired registrations first
            RegistrationService.cleanup_expired_registrations(db)

            # Check if username is available
            if not RegistrationService.check_username_available(db, username):
                return None, "Username already exists"

            # Check if email is already registered
            email_exists = db.query(User).filter(User.email == email).first()
            if email_exists:
                return None, "Email already registered"

            # Generate secure token
            token = secrets.token_urlsafe(32)

            # Calculate expiry time (UTC with timezone info)
            expires_at = datetime.now(timezone.utc) + timedelta(
                hours=config.REGISTRATION_TOKEN_EXPIRE_HOURS
            )

            # Create registration entry
            registration = UserRegistration(
                id=uuid.uuid4(),
                username=username,
                email=email,
                token=token,
                expires_at=expires_at,
            )

            db.add(registration)
            db.commit()
            db.refresh(registration)

            logger.info(f"Registration initiated for username: {username}")
            return registration, None

        except Exception as e:
            db.rollback()
            logger.error(f"Error initiating registration: {str(e)}")
            return None, "An error occurred during registration"

    @staticmethod
    def get_registration_by_token(
        db: Session, token: str
    ) -> Tuple[Optional[UserRegistration], Optional[str]]:
        """
        Get registration by token and validate it's not expired
        Returns: (UserRegistration, error_message)
        """
        try:
            # Cleanup expired registrations first
            RegistrationService.cleanup_expired_registrations(db)

            registration = (
                db.query(UserRegistration)
                .filter(UserRegistration.token == token)
                .first()
            )

            if not registration:
                return None, "Invalid or expired registration link"

            # Double-check expiry (should be already deleted by cleanup)
            if registration.is_expired():
                db.delete(registration)
                db.commit()
                return None, "Registration link has expired"

            return registration, None

        except Exception as e:
            db.rollback()
            logger.error(f"Error getting registration by token: {str(e)}")
            return None, "An error occurred"

    @staticmethod
    def is_first_user(db: Session) -> bool:
        """Check if this is the first user in the database"""
        user_count = db.query(User).count()
        return user_count == 0

    @staticmethod
    def generate_otp_qr_code(username: str, otp_secret: str) -> str:
        """
        Generate QR code for OTP setup
        Returns: base64 encoded QR code image
        """
        try:
            # Create OTP URI
            otp_uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(
                name=username, issuer_name=config.APP_NAME
            )

            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(otp_uri)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode()

            return img_str

        except Exception as e:
            logger.error(f"Error generating OTP QR code: {str(e)}")
            return ""

    @staticmethod
    def complete_registration(
        db: Session,
        token: str,
        first_name: str,
        last_name: str,
        password: str,
        corporate_number: Optional[str] = None,
        enable_otp: bool = False,
        current_language: str = "en",
    ) -> Tuple[Optional[User], Optional[Dict], Optional[str]]:
        """
        Complete registration process
        Returns: (User, otp_setup_data, error_message)
        """
        try:
            # Get and validate registration
            registration, error = RegistrationService.get_registration_by_token(
                db, token
            )
            if error:
                return None, None, error

            # Check if username already exists in users table (not in registrations, since this one is expected)
            user_exists = db.query(User).filter(User.username == registration.username).first()
            if user_exists:
                db.delete(registration)
                db.commit()
                return None, None, "Username no longer available"

            # Hash password
            hashed_password = hash_password(password)

            # Determine if this is the first user
            is_first_user = RegistrationService.is_first_user(db)

            # Generate OTP secret if requested
            otp_secret = None
            otp_setup_data = None
            if enable_otp:
                otp_secret = pyotp.random_base32()
                otp_qr_code = RegistrationService.generate_otp_qr_code(
                    registration.username, otp_secret
                )
                otp_setup_data = {
                    "secret": otp_secret,
                    "qr_code": otp_qr_code,
                    "manual_entry": otp_secret,
                }

            # Create user
            user = User(
                id=uuid.uuid4(),
                username=registration.username,
                email=registration.email,
                hashed_password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                current_language=current_language,
                corporate_number=corporate_number,
                otp_secret=otp_secret,
                otp_enabled=enable_otp,
                created_on=datetime.now(timezone.utc),
            )

            db.add(user)
            db.flush()

            # Assign role
            if is_first_user:
                admin_role = db.query(Role).filter(Role.name == "admin").first()
                if admin_role:
                    user_role = UserRole(
                        id=uuid.uuid4(), user_id=user.id, role_id=admin_role.id
                    )
                    db.add(user_role)
                logger.info(f"First user created with admin role: {user.username}")
            else:
                user_role = db.query(Role).filter(Role.name == "user").first()
                if user_role:
                    user_role_entry = UserRole(
                        id=uuid.uuid4(), user_id=user.id, role_id=user_role.id
                    )
                    db.add(user_role_entry)

            # Delete registration entry
            db.delete(registration)

            # Commit all changes
            db.commit()
            db.refresh(user)

            logger.info(f"Registration completed for user: {user.username}")
            return user, otp_setup_data, None

        except Exception as e:
            db.rollback()
            logger.error(f"Error completing registration: {str(e)}")
            return None, None, "An error occurred while completing registration"

    @staticmethod
    def verify_otp_code(otp_secret: str, otp_code: str) -> bool:
        """
        Verify OTP code against secret
        """
        try:
            totp = pyotp.TOTP(otp_secret)
            return totp.verify(otp_code, valid_window=1)
        except Exception as e:
            logger.error(f"Error verifying OTP code: {str(e)}")
            return False
