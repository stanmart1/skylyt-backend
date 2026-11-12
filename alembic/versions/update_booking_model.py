"""Update booking model with customer details

Revision ID: update_booking_model
Revises: update_hotel_model
Create Date: 2024-01-01 00:00:02.000000

"""
from alembic import op
from app.migration_helpers import (
    table_exists, column_exists, add_column_if_missing,
    create_table_if_missing, create_index_if_missing,
    drop_column_if_exists, rename_column_if_exists,
)

import sqlalchemy as sa

# revision identifiers
revision = 'update_booking_model'
down_revision = 'update_hotel_model'
branch_labels = None
depends_on = None

def upgrade():
    # Add customer details
    add_column_if_missing(op, 'bookings', sa.Column('customer_name', sa.String(255), nullable=False, server_default='Unknown'))
    add_column_if_missing(op, 'bookings', sa.Column('customer_email', sa.String(255), nullable=False, server_default='unknown@example.com'))
    
    # Add booking details
    add_column_if_missing(op, 'bookings', sa.Column('number_of_guests', sa.Integer(), nullable=True))
    add_column_if_missing(op, 'bookings', sa.Column('special_requests', sa.String(1000), nullable=True))
    add_column_if_missing(op, 'bookings', sa.Column('payment_status', sa.String(20), nullable=False, server_default='pending'))

def downgrade():
    # Remove added columns
    drop_column_if_exists(op, 'bookings', 'payment_status')
    drop_column_if_exists(op, 'bookings', 'special_requests')
    drop_column_if_exists(op, 'bookings', 'number_of_guests')
    drop_column_if_exists(op, 'bookings', 'customer_email')
    drop_column_if_exists(op, 'bookings', 'customer_name')