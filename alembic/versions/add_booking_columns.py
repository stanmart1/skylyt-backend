"""add booking columns

Revision ID: add_booking_cols
Revises: add_updated_at
Create Date: 2024-01-01 15:00:00.000000

"""
from alembic import op
from app.migration_helpers import (
    table_exists, column_exists, add_column_if_missing,
    create_table_if_missing, create_index_if_missing,
    drop_column_if_exists, rename_column_if_exists,
)

import sqlalchemy as sa

# revision identifiers
revision = 'add_booking_cols'
down_revision = 'add_updated_at'
branch_labels = None
depends_on = None

def upgrade():
    # Add missing columns to bookings table
    try:
        add_column_if_missing(op, 'bookings', sa.Column('hotel_name', sa.String(255), nullable=True))
    except:
        pass
    try:
        add_column_if_missing(op, 'bookings', sa.Column('car_name', sa.String(255), nullable=True))
    except:
        pass
    try:
        add_column_if_missing(op, 'bookings', sa.Column('check_in_date', sa.DateTime(), nullable=True))
    except:
        pass
    try:
        add_column_if_missing(op, 'bookings', sa.Column('check_out_date', sa.DateTime(), nullable=True))
    except:
        pass
    try:
        add_column_if_missing(op, 'bookings', sa.Column('total_amount', sa.Float(), nullable=True))
    except:
        pass
    try:
        add_column_if_missing(op, 'bookings', sa.Column('currency', sa.String(3), nullable=True))
    except:
        pass
    try:
        add_column_if_missing(op, 'bookings', sa.Column('booking_data', sa.JSON(), nullable=True))
    except:
        pass
    try:
        add_column_if_missing(op, 'bookings', sa.Column('updated_at', sa.DateTime(), nullable=True))
    except:
        pass
    
    # Update existing records
    op.execute("UPDATE bookings SET updated_at = created_at WHERE updated_at IS NULL")
    op.execute("UPDATE bookings SET currency = 'USD' WHERE currency IS NULL")
    op.execute("UPDATE bookings SET total_amount = 0 WHERE total_amount IS NULL")

def downgrade():
    drop_column_if_exists(op, 'bookings', 'booking_data')
    drop_column_if_exists(op, 'bookings', 'currency')
    drop_column_if_exists(op, 'bookings', 'total_amount')
    drop_column_if_exists(op, 'bookings', 'check_out_date')
    drop_column_if_exists(op, 'bookings', 'check_in_date')
    drop_column_if_exists(op, 'bookings', 'car_name')
    drop_column_if_exists(op, 'bookings', 'hotel_name')
    drop_column_if_exists(op, 'bookings', 'updated_at')