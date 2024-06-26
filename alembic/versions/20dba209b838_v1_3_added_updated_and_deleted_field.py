"""V1.3 Added updated and deleted field

Revision ID: 20dba209b838
Revises: fe0934d7c64d
Create Date: 2024-04-02 11:34:32.724833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20dba209b838'
down_revision: Union[str, None] = 'fe0934d7c64d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('product', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('product', sa.Column('is_deleted', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'is_deleted')
    op.drop_column('product', 'updated_at')
    op.drop_column('product', 'created_at')
    # ### end Alembic commands ###
