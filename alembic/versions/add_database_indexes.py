"""Add database indexes for performance optimization

Revision ID: add_indexes_001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op

from app.migration_helpers import (
    table_exists, column_exists, add_column_if_missing,
    create_table_if_missing, create_index_if_missing,
    drop_column_if_exists, rename_column_if_exists,
)

import sqlalchemy as sa

# revision identifiers
revision = 'add_indexes_001'
down_revision = '00_baseline_schema'
depends_on = None

def upgrade():
    # User table indexes
    create_index_if_missing(op, 'idx_users_email', 'users', ['email'])
    create_index_if_missing(op, 'idx_users_phone', 'users', ['phone_number'])
    create_index_if_missing(op, 'idx_users_created_at', 'users', ['created_at'])
    
    # Booking table indexes
    create_index_if_missing(op, 'idx_bookings_user_id', 'bookings', ['user_id'])
    create_index_if_missing(op, 'idx_bookings_status', 'bookings', ['status'])
    create_index_if_missing(op, 'idx_bookings_reference', 'bookings', ['booking_reference'])
    create_index_if_missing(op, 'idx_bookings_created_at', 'bookings', ['created_at'])
    create_index_if_missing(op, 'idx_bookings_check_in', 'bookings', ['check_in_date'])
    create_index_if_missing(op, 'idx_bookings_type_status', 'bookings', ['booking_type', 'status'])
    
    # Payment table indexes
    create_index_if_missing(op, 'idx_payments_booking_id', 'payments', ['booking_id'])
    create_index_if_missing(op, 'idx_payments_status', 'payments', ['status'])
    create_index_if_missing(op, 'idx_payments_gateway', 'payments', ['gateway'])
    create_index_if_missing(op, 'idx_payments_transaction_id', 'payments', ['transaction_id'])
    create_index_if_missing(op, 'idx_payments_created_at', 'payments', ['created_at'])
    
    # Role and Permission indexes
    create_index_if_missing(op, 'idx_roles_name', 'roles', ['name'])
    create_index_if_missing(op, 'idx_permissions_name', 'permissions', ['name'])
    
    # User roles association indexes
    create_index_if_missing(op, 'idx_user_roles_user_id', 'user_roles', ['user_id'])
    create_index_if_missing(op, 'idx_user_roles_role_id', 'user_roles', ['role_id'])

def downgrade():
    # Drop indexes in reverse order
    op.drop_index('idx_user_roles_role_id')
    op.drop_index('idx_user_roles_user_id')
    op.drop_index('idx_permissions_name')
    op.drop_index('idx_roles_name')
    op.drop_index('idx_payments_created_at')
    op.drop_index('idx_payments_transaction_id')
    op.drop_index('idx_payments_gateway')
    op.drop_index('idx_payments_status')
    op.drop_index('idx_payments_booking_id')
    op.drop_index('idx_bookings_type_status')
    op.drop_index('idx_bookings_check_in')
    op.drop_index('idx_bookings_created_at')
    op.drop_index('idx_bookings_reference')
    op.drop_index('idx_bookings_status')
    op.drop_index('idx_bookings_user_id')
    op.drop_index('idx_users_created_at')
    op.drop_index('idx_users_phone')
    op.drop_index('idx_users_email')