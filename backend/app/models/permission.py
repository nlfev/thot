"""
Permission model for RBAC
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class Permission(BaseModel):
    """
    Permission model for Role-Based Access Control (RBAC)
    """

    __tablename__ = "permissions"

    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(String(500), nullable=True)

    # Relationships
    role_permissions = relationship("RolePermission", back_populates="permission", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Permission(id={self.id}, name={self.name})>"
