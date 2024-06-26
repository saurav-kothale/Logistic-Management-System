"""V2.8 Added Weekly raw data

Revision ID: 11d5506a8fcc
Revises: 6b0fbbc88062
Create Date: 2024-06-06 12:00:48.230462

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11d5506a8fcc'
down_revision: Union[str, None] = '6b0fbbc88062'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('weekly_raw_data',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('FILE_KEY', sa.String(), nullable=True),
    sa.Column('FILE_NAME', sa.String(), nullable=True),
    sa.Column('CITY_NAME', sa.String(), nullable=True),
    sa.Column('CLIENT_NAME', sa.String(), nullable=True),
    sa.Column('DATE', sa.String(), nullable=True),
    sa.Column('JOINING_DATE', sa.Date(), nullable=True),
    sa.Column('COMPANY', sa.String(), nullable=True),
    sa.Column('SALARY_DATE', sa.Date(), nullable=True),
    sa.Column('SATAUS', sa.String(), nullable=True),
    sa.Column('WEEK_NAME', sa.String(), nullable=True),
    sa.Column('PHONE_NUMBER', sa.String(), nullable=True),
    sa.Column('AADHAR_NUMBER', sa.String(length=12), nullable=True),
    sa.Column('DRIVER_ID', sa.String(), nullable=True),
    sa.Column('DRIVER_NAME', sa.String(), nullable=True),
    sa.Column('WORK_TYPE', sa.String(), nullable=True),
    sa.Column('DONE_PARCEL_ORDERS', sa.Integer(), nullable=True),
    sa.Column('DONE_DOCUMENT_ORDERS', sa.Integer(), nullable=True),
    sa.Column('DONE_BIKER_ORDERS', sa.Integer(), nullable=True),
    sa.Column('DONE_MICRO_ORDERS', sa.Integer(), nullable=True),
    sa.Column('RAIN_ORDER', sa.Integer(), nullable=True),
    sa.Column('IGCC_AMOUNT', sa.Integer(), nullable=True),
    sa.Column('BAD_ORDER', sa.Integer(), nullable=True),
    sa.Column('REJECTION', sa.Integer(), nullable=True),
    sa.Column('ATTENDANCE', sa.Integer(), nullable=True),
    sa.Column('CASH_COLLECTED', sa.Integer(), nullable=True),
    sa.Column('CASH_DEPOSITED', sa.Integer(), nullable=True),
    sa.Column('PAYMENT_SENT_ONLINE', sa.Integer(), nullable=True),
    sa.Column('POCKET_WITHDRAWAL', sa.Integer(), nullable=True),
    sa.Column('OTHER_PANALTY', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_index(op.f('ix_weekly_raw_data_ID'), 'weekly_raw_data', ['ID'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_weekly_raw_data_ID'), table_name='weekly_raw_data')
    op.drop_table('weekly_raw_data')
    # ### end Alembic commands ###
