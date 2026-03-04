"""
Password reset token model
"""

import uuid

from sqlalchemy import Column, String, DateTime, UUID, Boolean, ForeignKey

from app.database import Base


class PasswordResetToken(Base):
    """
    Password reset token model for temporary reset links
    """

    __tablename__ = "password_reset_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userid = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        return f"<PasswordResetToken(id={self.id}, userid={self.userid}, used={self.used})>"