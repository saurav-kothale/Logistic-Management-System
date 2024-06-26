"""V1.16 added unit in prodcutDB

Revision ID: be0ca5d53d93
Revises: bcc997a8648f
Create Date: 2024-05-10 11:12:36.176727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be0ca5d53d93'
down_revision: Union[str, None] = 'bcc997a8648f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('unit', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'unit')
    # ### end Alembic commands ###
