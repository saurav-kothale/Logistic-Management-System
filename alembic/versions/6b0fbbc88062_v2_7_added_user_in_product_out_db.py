"""V2.7 Added user in Product out db

Revision ID: 6b0fbbc88062
Revises: 493c024296f3
Create Date: 2024-06-03 18:51:17.084925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b0fbbc88062'
down_revision: Union[str, None] = '493c024296f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory out', sa.Column('user', sa.JSON(), nullable=True))
    op.add_column('rawfile_record', sa.Column('PAYMENT_SENT_ONLINE', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rawfile_record', 'PAYMENT_SENT_ONLINE')
    op.drop_column('inventory out', 'user')
    # ### end Alembic commands ###