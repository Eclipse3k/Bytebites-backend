"""enable unaccent extension

Revision ID: enable_unaccent
Revises: ee967f6889ec
Create Date: 2024-03-19

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'enable_unaccent'
down_revision = 'ee967f6889ec'
branch_labels = None
depends_on = None

def upgrade():
    # Enable unaccent extension
    op.execute('CREATE EXTENSION IF NOT EXISTS unaccent')

def downgrade():
    # Disable unaccent extension
    op.execute('DROP EXTENSION IF EXISTS unaccent')