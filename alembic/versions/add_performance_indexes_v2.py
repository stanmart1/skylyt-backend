"""add performance indexes v2

Revision ID: add_performance_indexes_v2
Revises: add_children_count
Create Date: 2024-01-01 00:00:01.000000

"""
from alembic import op

from app.migration_helpers import (
    table_exists, column_exists, add_column_if_missing,
    create_table_if_missing, create_index_if_missing,
    drop_column_if_exists, rename_column_if_exists,
)

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_performance_indexes_v2'
down_revision = 'add_children_count'
branch_labels = None
depends_on = None


def upgrade():
    # Add indexes for frequently queried fields (with IF NOT EXISTS logic)
    try:
        create_index_if_missing(op, 'idx_bookings_payment_status', 'bookings', ['payment_status'])
    except:
        pass
    try:
        create_index_if_missing(op, 'idx_bookings_booking_type', 'bookings', ['booking_type'])
    except:
        pass
    try:
        create_index_if_missing(op, 'idx_bookings_customer_email', 'bookings', ['customer_email'])
    except:
        pass
    try:
        create_index_if_missing(op, 'idx_bookings_created_at', 'bookings', ['created_at'])
    except:
        pass
    
    # Add indexes for payments
    try:
        create_index_if_missing(op, 'idx_payments_status', 'payments', ['status'])
    except:
        pass
    try:
        create_index_if_missing(op, 'idx_payments_booking_id', 'payments', ['booking_id'])
    except:
        pass
    try:
        create_index_if_missing(op, 'idx_payments_created_at', 'payments', ['created_at'])
    except:
        pass
    
    # Add indexes for users
    try:
        create_index_if_missing(op, 'idx_users_is_active', 'users', ['is_active'])
    except:
        pass


def downgrade():
    # Remove indexes
    op.drop_index('idx_bookings_status', 'bookings')
    op.drop_index('idx_bookings_payment_status', 'bookings')
    op.drop_index('idx_bookings_booking_type', 'bookings')
    op.drop_index('idx_bookings_customer_email', 'bookings')
    op.drop_index('idx_bookings_created_at', 'bookings')
    
    op.drop_index('idx_payments_status', 'payments')
    op.drop_index('idx_payments_booking_id', 'payments')
    op.drop_index('idx_payments_created_at', 'payments')
    
    op.drop_index('idx_users_is_active', 'users')