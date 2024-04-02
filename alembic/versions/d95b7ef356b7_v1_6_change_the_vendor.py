"""V1.6 Change the vendor

Revision ID: d95b7ef356b7
Revises: c93ca5bb488a
Create Date: 2024-04-02 17:15:57.671874

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd95b7ef356b7'
down_revision: Union[str, None] = 'c93ca5bb488a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory', sa.Column('vendor', sa.String(), nullable=True))
    op.drop_column('inventory', 'vender')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory', sa.Column('vender', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('inventory', 'vendor')
    # ### end Alembic commands ###
