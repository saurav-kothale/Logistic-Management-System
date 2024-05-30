"""V2.4 Added file record table

Revision ID: 7bffe2e465bf
Revises: 363b813e0a52
Create Date: 2024-05-30 11:28:20.524963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7bffe2e465bf'
down_revision: Union[str, None] = '363b813e0a52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rawfile_record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=True),
    sa.Column('CITY_NAME', sa.String(), nullable=True),
    sa.Column('CLIENT_NAME', sa.String(), nullable=True),
    sa.Column('DATE', sa.String(), nullable=True),
    sa.Column('AADHAR_NUMBER', sa.String(length=12), nullable=True),
    sa.Column('DRIVER_ID', sa.String(), nullable=True),
    sa.Column('DRIVER_NAME', sa.String(), nullable=True),
    sa.Column('WORK_TYPE', sa.String(), nullable=True),
    sa.Column('LOG_IN_HR', sa.String(), nullable=True),
    sa.Column('PICKUP_DOCUMENT_ORDERS', sa.String(), nullable=True),
    sa.Column('DONE_DOCUMENT_ORDERS', sa.Integer(), nullable=True),
    sa.Column('PICKUP_PARCEL_ORDERS', sa.Integer(), nullable=True),
    sa.Column('DONE_PARCEL_ORDERS', sa.Integer(), nullable=True),
    sa.Column('PICKUP_BIKER_ORDERS', sa.Integer(), nullable=True),
    sa.Column('DONE_BIKER_ORDERS', sa.Integer(), nullable=True),
    sa.Column('PICKUP_MICRO_ORDERS', sa.Integer(), nullable=True),
    sa.Column('DONE_MICRO_ORDERS', sa.Integer(), nullable=True),
    sa.Column('CUSTOMER_TIP', sa.Integer(), nullable=True),
    sa.Column('RAIN_ORDER', sa.Integer(), nullable=True),
    sa.Column('IGCC_AMOUNT', sa.Integer(), nullable=True),
    sa.Column('BAD_ORDER', sa.Integer(), nullable=True),
    sa.Column('REJECTION', sa.Integer(), nullable=True),
    sa.Column('ATTENDANCE', sa.Integer(), nullable=True),
    sa.Column('CASH_COLLECTION', sa.Integer(), nullable=True),
    sa.Column('CASH_DEPOSIT', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rawfile_record_id'), 'rawfile_record', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_rawfile_record_id'), table_name='rawfile_record')
    op.drop_table('rawfile_record')
    # ### end Alembic commands ###
