"""
UserRole association model for RBAC
"""

from sqlalchemy import Column, UUID, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class UserRole(BaseModel):
    """
    Association table between User and Role
    """

    __tablename__ = "user_roles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")

    def __repr__(self) -> str:
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id})>"
