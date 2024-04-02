"""V1.4 remove unique from invoice number

Revision ID: c93ca5bb488a
Revises: 20dba209b838
Create Date: 2024-04-02 11:44:24.265747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c93ca5bb488a'
down_revision: Union[str, None] = '20dba209b838'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('inventory_invoice_number_key', 'inventory', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('inventory_invoice_number_key', 'inventory', ['invoice_number'])
    # ### end Alembic commands ###
