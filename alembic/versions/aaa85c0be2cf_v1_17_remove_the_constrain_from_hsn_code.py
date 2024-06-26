"""V1.17 Remove the Constrain from HSN code

Revision ID: aaa85c0be2cf
Revises: be0ca5d53d93
Create Date: 2024-05-10 12:10:16.537954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aaa85c0be2cf'
down_revision: Union[str, None] = 'be0ca5d53d93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('product_HSN_code_key', 'product', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('product_HSN_code_key', 'product', ['HSN_code'])
    # ### end Alembic commands ###
