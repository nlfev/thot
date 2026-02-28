"""Initial migration - create users, roles, permissions tables

Revision ID: 001
Revises: 
Create Date: 2026-03-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create roles table
    op.create_table(
        'roles',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.String(500), nullable=True),
        sa.Column('created_by', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('created_on', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_modified_by', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('last_modified_on', sa.DateTime(timezone=True), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_roles_name', 'roles', ['name'], unique=True)

    # Create permissions table
    op.create_table(
        'permissions',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.String(500), nullable=True),
        sa.Column('created_by', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('created_on', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_modified_by', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('last_modified_on', sa.DateTime(timezone=True), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_permissions_name', 'permissions', ['name'], unique=True)

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('username', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(255), nullable=True),
        sa.Column('last_name', sa.String(255), nullable=True),
        sa.Column('current_language', sa.String(2), nullable=False, server_default='en'),
        sa.Column('corporate_number', sa.String(255), nullable=True),
        sa.Column('corporate_approved', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('unsuccessful_logins', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('timestamp_last_successful_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('otp_secret', sa.String(255), nullable=True),
        sa.Column('otp_enabled', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_by', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('created_on', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_modified_by', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('last_modified_on', sa.DateTime(timezone=True), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Create user_roles association table
    op.create_table(
        'user_roles',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('role_id', sa.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create role_permissions association table
    op.create_table(
        'role_permissions',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('role_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('permission_id', sa.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('role_permissions')
    op.drop_table('user_roles')
    op.drop_index('ix_users_email')
    op.drop_index('ix_users_username')
    op.drop_table('users')
    op.drop_index('ix_permissions_name')
    op.drop_table('permissions')
    op.drop_index('ix_roles_name')
    op.drop_table('roles')
