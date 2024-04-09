"""V1.7 : Added Table for all Category

Revision ID: 59fef5335480
Revises: d95b7ef356b7
Create Date: 2024-04-09 11:38:55.817648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59fef5335480'
down_revision: Union[str, None] = 'd95b7ef356b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bikes',
    sa.Column('bike_id', sa.String(), nullable=False),
    sa.Column('bike_name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('bike_id'),
    sa.UniqueConstraint('bike_name')
    )
    op.create_table('cities',
    sa.Column('city_id', sa.String(), nullable=False),
    sa.Column('city_name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('city_id'),
    sa.UniqueConstraint('city_name')
    )
    op.create_table('colors',
    sa.Column('color_id', sa.String(), nullable=False),
    sa.Column('color_name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('color_id'),
    sa.UniqueConstraint('color_name')
    )
    op.create_table('new_category',
    sa.Column('category_id', sa.String(), nullable=False),
    sa.Column('category_name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('category_id'),
    sa.UniqueConstraint('category_name')
    )
    op.create_table('size',
    sa.Column('size_id', sa.String(), nullable=False),
    sa.Column('size_name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('size_id'),
    sa.UniqueConstraint('size_name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('size')
    op.drop_table('new_category')
    op.drop_table('colors')
    op.drop_table('cities')
    op.drop_table('bikes')
    # ### end Alembic commands ###