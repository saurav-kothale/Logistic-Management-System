"""V1.18 : Added Product category table

Revision ID: 232b392fed64
Revises: aaa85c0be2cf
Create Date: 2024-05-11 12:34:19.884218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '232b392fed64'
down_revision: Union[str, None] = 'aaa85c0be2cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
