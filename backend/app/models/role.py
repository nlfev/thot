"""
Role model for RBAC
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class Role(BaseModel):
    """
    Role model for Role-Based Access Control (RBAC)
    """

    __tablename__ = "roles"

    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(String(500), nullable=True)

    # Relationships
    user_roles = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")
    role_permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name={self.name})>"
