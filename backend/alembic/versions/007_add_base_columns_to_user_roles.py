"""Add base columns to user_roles table

Revision ID: 007
Revises: 006
Create Date: 2026-03-08 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add base columns to user_roles table
    op.add_column('user_roles', sa.Column('created_by', sa.UUID(as_uuid=True), nullable=True))
    op.add_column('user_roles', sa.Column('created_on', sa.DateTime(timezone=True), nullable=True))
    op.add_column('user_roles', sa.Column('last_modified_by', sa.UUID(as_uuid=True), nullable=True))
    op.add_column('user_roles', sa.Column('last_modified_on', sa.DateTime(timezone=True), nullable=True))
    op.add_column('user_roles', sa.Column('active', sa.Boolean(), nullable=False, server_default='true'))
    
    # Set created_on for existing records to current timestamp
    op.execute("UPDATE user_roles SET created_on = NOW() WHERE created_on IS NULL")
    
    # Make created_on NOT NULL
    op.alter_column('user_roles', 'created_on', nullable=False)
    
    # Ensure all existing records have active = true
    op.execute("UPDATE user_roles SET active = true WHERE active IS NULL OR active = false")


def downgrade() -> None:
    op.drop_column('user_roles', 'active')
    op.drop_column('user_roles', 'last_modified_on')
    op.drop_column('user_roles', 'last_modified_by')
    op.drop_column('user_roles', 'created_on')
    op.drop_column('user_roles', 'created_by')
