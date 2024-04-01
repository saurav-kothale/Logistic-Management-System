"""V1.1 Added New Model for product and inventory

Revision ID: c4bf767bb563
Revises: 5be12e96ec21
Create Date: 2024-03-28 17:17:06.224758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4bf767bb563'
down_revision: Union[str, None] = '5be12e96ec21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventory',
    sa.Column('invoice_id', sa.String(), nullable=False),
    sa.Column('invoice_number', sa.Integer(), nullable=True),
    sa.Column('invoice_amount', sa.Integer(), nullable=True),
    sa.Column('invoice_date', sa.Date(), nullable=True),
    sa.Column('inventory_paydate', sa.Date(), nullable=True),
    sa.Column('vender', sa.String(), nullable=True),
    sa.Column('invoice_image_id', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('invoice_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('inventory')
    # ### end Alembic commands ###
