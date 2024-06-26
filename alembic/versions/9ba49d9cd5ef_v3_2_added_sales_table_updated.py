"""V3.2 Added Sales table updated

Revision ID: 9ba49d9cd5ef
Revises: 3e1ff943f4fe
Create Date: 2024-06-21 12:58:57.888685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ba49d9cd5ef'
down_revision: Union[str, None] = '3e1ff943f4fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sales', 'sales without gst')
    op.drop_column('sales', 'sales with gst')
    op.drop_column('sales', 'location')
    op.drop_column('sales', 'full time rider')
    op.drop_column('sales', 'payout with gst')
    op.drop_column('sales', 'clent')
    op.drop_column('sales', 'part time order')
    op.drop_column('sales', 'payout without gst')
    op.drop_column('sales', 'part time rider')
    op.drop_column('sales', 'full time order')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sales', sa.Column('full time order', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('sales', sa.Column('part time rider', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('sales', sa.Column('payout without gst', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('sales', sa.Column('part time order', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('sales', sa.Column('clent', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.add_column('sales', sa.Column('payout with gst', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('sales', sa.Column('full time rider', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('sales', sa.Column('location', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.add_column('sales', sa.Column('sales with gst', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('sales', sa.Column('sales without gst', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
