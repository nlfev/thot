"""
Authentication routes for user registration, login, and password management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.models import User
from app.schemas import (
    UserRegisterRequest,
    UserCompleteRegistration,
    UserLoginRequest,
    UserLoginResponse,
    UserResponse,
    PasswordResetRequest,
    PasswordResetConfirmRequest,
    EmailChangeRequest,
    EmailChangeConfirmRequest,
    OTPEnableRequest,
)
from app.services import UserService
from app.utils import (
    create_access_token,
    validate_password_requirements,
    generate_email_token,
    verify_password,
    verify_otp,
    generate_short_code,
)
from app.utils.email_service import email_service
from config import config


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


@router.post("/register", response_model=dict)
async def register_user(
    request: UserRegisterRequest,
    db: Session = Depends(get_db),
):
    """
    Register a new user
    User must agree to Terms of Service
    """
    # Check if username already exists
    existing_user = UserService.get_user_by_username(db, request.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email already exists
    existing_email = UserService.get_user_by_email(db, request.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if TOS agreed
    if not request.tos_agreed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must agree to the Terms of Service"
        )

    # TODO: Generate email token and send verification email
    # token, _ = generate_email_token()
    # verification_link = f"{config.FRONTEND_URL}/register/confirm/{token}"
    # email_service.send_registration_confirmation_email(
    #     request.email,
    #     request.username,
    #     verification_link,
    #     config.EMAIL_TOKEN_EXPIRE_HOURS
    # )

    return {
        "message": "Registration successful. Check your email for confirmation.",
        "username": request.username,
        "email": request.email,
    }


@router.post("/register/confirm/{token}")
async def confirm_registration(
    token: str,
    request: UserCompleteRegistration,
    db: Session = Depends(get_db),
):
    """
    Complete user registration with confirmed email
    """
    # TODO: Verify token validity
    # TODO: Check token expiration

    # Validate password requirements
    is_valid, error_msg = validate_password_requirements(request.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    # Check if passwords match
    if request.password != request.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    # TODO: Create user from token data
    # is_first_user = db.query(User).count() == 0
    # user = UserService.create_user(
    #     db=db,
    #     username=...,  # from token
    #     email=...,     # from token
    #     password=request.password,
    #     first_name=request.first_name,
    #     last_name=request.last_name,
    #     corporate_number=request.corporate_number,
    #     is_first_user=is_first_user,
    # )

    # if request.enable_otp:
    #     otp_secret = UserService.enable_otp(db, str(user.id))
    #     # TODO: Return QR code or secret for setup

    return {
        "message": "Registration completed successfully",
    }


@router.post("/login", response_model=UserLoginResponse)
async def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db),
):
    """
    Login user with username/email and password
    Optional OTP for two-factor authentication
    """
    # Authenticate user
    user, error = UserService.authenticate_user(
        db=db,
        username=request.username,
        password=request.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error or "Invalid username or password"
        )

    # Check if OTP is enabled and provided
    if user.otp_enabled:
        if not request.otp_code:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Two-factor authentication required"
            )

        # Verify OTP
        if not verify_otp(user.otp_secret, request.otp_code):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid OTP code"
            )

    # Create access token
    access_token = create_access_token(str(user.id))

    # Prepare user response
    user_response = UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        current_language=user.current_language,
        corporate_number=user.corporate_number,
        corporate_approved=user.corporate_approved,
        active=user.active,
        created_on=user.created_on,
        roles=user.get_roles(),
    )

    return UserLoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response,
    )


@router.post("/password-reset")
async def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(get_db),
):
    """
    Request password reset via email
    """
    user = UserService.get_user_by_email(db, request.email)

    # Always return success for security
    if user:
        # TODO: Generate password reset token
        # token, _ = generate_email_token()
        # reset_link = f"{config.FRONTEND_URL}/password-reset/confirm/{token}"
        # email_service.send_password_reset_email(
        #     user.email,
        #     user.username,
        #     reset_link,
        #     config.PASSWORD_RESET_TOKEN_EXPIRE_HOURS
        # )

        pass

    return {
        "message": "If the email exists, you will receive password reset instructions"
    }


@router.post("/password-reset/confirm/{token}")
async def confirm_password_reset(
    token: str,
    request: PasswordResetConfirmRequest,
    db: Session = Depends(get_db),
):
    """
    Confirm password reset with new password
    """
    # TODO: Verify token and get user from token
    # user_id = verify_password_reset_token(token)

    # TODO: Validate and update password
    # success, message = UserService.reset_password(
    #     db=db,
    #     user_id=user_id,
    #     new_password=request.new_password
    # )

    return {
        "message": "Password reset successfully"
    }


# TODO: Implement remaining endpoints:
# - /logout - Logout user
# - /refresh - Refresh access token
# - /users/email-change - Change email
# - /users/email-change/confirm/{token} - Confirm email change
# - /users/otp/enable - Enable OTP
# - /users/otp/disable - Disable OTP
