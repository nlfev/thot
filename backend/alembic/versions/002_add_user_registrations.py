"""Add user_registrations table

Revision ID: 002
Revises: 001
Create Date: 2026-03-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user_registrations table
    op.create_table(
        'user_registrations',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('username', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('token', sa.String(255), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_registrations_username', 'user_registrations', ['username'])
    op.create_index('ix_user_registrations_email', 'user_registrations', ['email'])
    op.create_index('ix_user_registrations_token', 'user_registrations', ['token'], unique=True)


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_user_registrations_token', table_name='user_registrations')
    op.drop_index('ix_user_registrations_email', table_name='user_registrations')
    op.drop_index('ix_user_registrations_username', table_name='user_registrations')
    
    # Drop table
    op.drop_table('user_registrations')
