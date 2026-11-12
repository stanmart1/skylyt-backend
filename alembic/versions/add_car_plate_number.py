"""add plate_number to cars

Revision ID: add_car_plate_number
Revises: update_booking_payment_currency
Create Date: 2024-01-01 00:00:02.000000

"""
from alembic import op
from app.migration_helpers import (
    table_exists, column_exists, add_column_if_missing,
    create_table_if_missing, create_index_if_missing,
    drop_column_if_exists, rename_column_if_exists,
)

import sqlalchemy as sa

revision = 'add_car_plate_number'
down_revision = 'update_booking_payment_currency'
branch_labels = None
depends_on = None

def upgrade():
    add_column_if_missing(op, 'cars', sa.Column('plate_number', sa.String(), nullable=True))

def downgrade():
    drop_column_if_exists(op, 'cars', 'plate_number')
