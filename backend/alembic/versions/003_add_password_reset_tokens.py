"""Add password_reset_tokens table

Revision ID: 003
Revises: 002
Create Date: 2026-03-04 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create password_reset_tokens table
    op.create_table(
        'password_reset_tokens',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('userid', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('token', sa.String(255), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('used', sa.Boolean(), nullable=False, server_default='false'),
        sa.ForeignKeyConstraint(['userid'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_password_reset_tokens_userid', 'password_reset_tokens', ['userid'])
    op.create_index('ix_password_reset_tokens_token', 'password_reset_tokens', ['token'], unique=True)


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_password_reset_tokens_token', table_name='password_reset_tokens')
    op.drop_index('ix_password_reset_tokens_userid', table_name='password_reset_tokens')

    # Drop table
    op.drop_table('password_reset_tokens')