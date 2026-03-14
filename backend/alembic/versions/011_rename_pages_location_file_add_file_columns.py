"""Rename pages.location_file to orgin_file and add file metadata columns

Revision ID: 011
Revises: 010
Create Date: 2026-03-14 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '011'
down_revision = '010'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('pages', 'location_file', new_column_name='orgin_file')
    op.add_column('pages', sa.Column('current_file', sa.Text(), nullable=True))
    op.add_column('pages', sa.Column('restriction_file', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('pages', 'restriction_file')
    op.drop_column('pages', 'current_file')
    op.alter_column('pages', 'orgin_file', new_column_name='location_file')
