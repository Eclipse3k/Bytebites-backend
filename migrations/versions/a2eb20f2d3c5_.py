"""empty message

Revision ID: a2eb20f2d3c5
Revises: 80eb87e1fdec, enable_unaccent
Create Date: 2025-02-14 16:09:05.171151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2eb20f2d3c5'
down_revision = ('80eb87e1fdec', 'enable_unaccent')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
