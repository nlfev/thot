"""
Email utilities for sending emails
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from datetime import datetime
import logging

from config import config

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails"""

    def __init__(self):
        self.smtp_server = config.SMTP_SERVER
        self.smtp_port = config.SMTP_PORT
        self.smtp_user = config.SMTP_USER
        self.smtp_password = config.SMTP_PASSWORD
        self.from_email = config.SMTP_FROM_EMAIL
        self.from_name = config.SMTP_FROM_NAME

    def _create_smtp_connection(self):
        """Create SMTP connection"""
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.smtp_user, self.smtp_password)
        return server

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_text: Optional[str] = None,
    ) -> bool:
        """
        Send an email
        """
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.from_name} <{self.from_email}>"
            message["To"] = to_email

            if plain_text:
                part1 = MIMEText(plain_text, "plain")
                message.attach(part1)

            part2 = MIMEText(html_content, "html")
            message.attach(part2)

            server = self._create_smtp_connection()
            server.sendmail(self.from_email, to_email, message.as_string())
            server.quit()

            logger.info(f"Email sent to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    def send_registration_confirmation_email(
        self,
        to_email: str,
        username: str,
        confirmation_link: str,
        expiration_hours: int = 24,
    ) -> bool:
        """Send registration confirmation email"""
        subject = "Confirm Your Email Address"
        html_content = f"""
        <html>
            <body>
                <h2>Welcome, {username}!</h2>
                <p>Thank you for registering. Please confirm your email address by clicking the link below:</p>
                <p>
                    <a href="{confirmation_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                        Confirm Email
                    </a>
                </p>
                <p>This link will expire in {expiration_hours} hours.</p>
                <p>If you did not register for this account, please ignore this email.</p>
            </body>
        </html>
        """
        plain_text = (
            f"Welcome, {username}!\n\n"
            f"Please confirm your email address by visiting: {confirmation_link}\n\n"
            f"This link will expire in {expiration_hours} hours."
        )
        return self.send_email(to_email, subject, html_content, plain_text)

    def send_password_reset_email(
        self,
        to_email: str,
        username: str,
        reset_link: str,
        expiration_hours: int = 24,
    ) -> bool:
        """Send password reset email"""
        subject = "Reset Your Password"
        html_content = f"""
        <html>
            <body>
                <h2>Password Reset Request</h2>
                <p>Hi {username},</p>
                <p>We received a request to reset your password. Click the link below to set a new password:</p>
                <p>
                    <a href="{reset_link}" style="background-color: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                        Reset Password
                    </a>
                </p>
                <p>This link will expire in {expiration_hours} hours.</p>
                <p>If you did not request a password reset, please ignore this email.</p>
            </body>
        </html>
        """
        plain_text = (
            f"Hi {username},\n\n"
            f"Please reset your password by visiting: {reset_link}\n\n"
            f"This link will expire in {expiration_hours} hours."
        )
        return self.send_email(to_email, subject, html_content, plain_text)

    def send_email_change_confirmation(
        self,
        to_email: str,
        username: str,
        confirmation_link: str,
        verification_code: str,
        expiration_hours: int = 1,
    ) -> bool:
        """Send email change confirmation"""
        subject = "Confirm Your New Email Address"
        html_content = f"""
        <html>
            <body>
                <h2>Email Change Confirmation</h2>
                <p>Hi {username},</p>
                <p>A request was made to change your email address. Click the link below to confirm:</p>
                <p>
                    <a href="{confirmation_link}" style="background-color: #FF9800; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                        Confirm Email Change
                    </a>
                </p>
                <p>Your verification code is: <strong>{verification_code}</strong></p>
                <p>This link will expire in {expiration_hours} hour(s).</p>
                <p>If you did not request this change, please ignore this email.</p>
            </body>
        </html>
        """
        plain_text = (
            f"Hi {username},\n\n"
            f"A request was made to change your email address.\n"
            f"Please confirm by visiting: {confirmation_link}\n\n"
            f"Your verification code is: {verification_code}\n\n"
            f"This link will expire in {expiration_hours} hour(s)."
        )
        return self.send_email(to_email, subject, html_content, plain_text)


# Global email service instance
email_service = EmailService()
