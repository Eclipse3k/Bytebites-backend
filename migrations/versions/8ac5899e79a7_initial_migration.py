"""initial migration

Revision ID: 8ac5899e79a7
Revises: 
Create Date: 2025-02-24 23:50:25.303586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ac5899e79a7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('foods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('calories_per_100g', sa.Float(), nullable=False),
    sa.Column('protein_per_100g', sa.Float(), nullable=True),
    sa.Column('carbs_per_100g', sa.Float(), nullable=True),
    sa.Column('fat_per_100g', sa.Float(), nullable=True),
    sa.Column('usda_id', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('usda_id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=1024), nullable=False),
    sa.Column('bio', sa.String(length=500), nullable=True),
    sa.Column('daily_calorie_goal', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('height', sa.Float(), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('joined_at', sa.DateTime(), nullable=True),
    sa.Column('profile_picture_url', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    op.create_table('food_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('food_id', sa.Integer(), nullable=False),
    sa.Column('grams', sa.Float(), nullable=False),
    sa.Column('log_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['food_id'], ['foods.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('food_logs', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_food_logs_log_date'), ['log_date'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('food_logs', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_food_logs_log_date'))

    op.drop_table('food_logs')
    op.drop_table('followers')
    op.drop_table('users')
    op.drop_table('foods')
    # ### end Alembic commands ###
