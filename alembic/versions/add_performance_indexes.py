"""Add performance indexes

Revision ID: add_performance_indexes
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
revision = 'add_performance_indexes'
down_revision = '00_baseline_schema'
branch_labels = None
depends_on = None

def upgrade():
    # Cars table indexes
    create_index_if_missing(op, 'idx_cars_category', 'cars', ['category'])
    create_index_if_missing(op, 'idx_cars_price_per_day', 'cars', ['price_per_day'])
    create_index_if_missing(op, 'idx_cars_is_featured', 'cars', ['is_featured'])
    create_index_if_missing(op, 'idx_cars_is_available', 'cars', ['is_available'])
    create_index_if_missing(op, 'idx_cars_location', 'cars', ['location'])
    create_index_if_missing(op, 'idx_cars_make_model', 'cars', ['make', 'model'])
    
    # Hotels table indexes
    create_index_if_missing(op, 'idx_hotels_location', 'hotels', ['location'])
    create_index_if_missing(op, 'idx_hotels_rating', 'hotels', ['rating'])
    create_index_if_missing(op, 'idx_hotels_price', 'hotels', ['price'])
    
    # Bookings table indexes
    create_index_if_missing(op, 'idx_bookings_user_id', 'bookings', ['user_id'])
    create_index_if_missing(op, 'idx_bookings_status', 'bookings', ['status'])
    create_index_if_missing(op, 'idx_bookings_type', 'bookings', ['booking_type'])
    create_index_if_missing(op, 'idx_bookings_reference', 'bookings', ['booking_reference'])
    create_index_if_missing(op, 'idx_bookings_dates', 'bookings', ['check_in_date', 'check_out_date'])
    
    # Users table indexes (additional)
    create_index_if_missing(op, 'idx_users_active', 'users', ['is_active'])
    create_index_if_missing(op, 'idx_users_verified', 'users', ['is_verified'])
    create_index_if_missing(op, 'idx_users_name', 'users', ['first_name', 'last_name'])
    
    # Base model indexes for common queries
    create_index_if_missing(op, 'idx_cars_created_at', 'cars', ['created_at'])
    create_index_if_missing(op, 'idx_hotels_created_at', 'hotels', ['created_at'])
    create_index_if_missing(op, 'idx_bookings_created_at', 'bookings', ['created_at'])
    create_index_if_missing(op, 'idx_users_created_at', 'users', ['created_at'])

def downgrade():
    # Drop indexes in reverse order
    op.drop_index('idx_users_created_at', 'users')
    op.drop_index('idx_bookings_created_at', 'bookings')
    op.drop_index('idx_hotels_created_at', 'hotels')
    op.drop_index('idx_cars_created_at', 'cars')
    
    op.drop_index('idx_users_name', 'users')
    op.drop_index('idx_users_verified', 'users')
    op.drop_index('idx_users_active', 'users')
    
    op.drop_index('idx_bookings_dates', 'bookings')
    op.drop_index('idx_bookings_reference', 'bookings')
    op.drop_index('idx_bookings_type', 'bookings')
    op.drop_index('idx_bookings_status', 'bookings')
    op.drop_index('idx_bookings_user_id', 'bookings')
    
    op.drop_index('idx_hotels_price', 'hotels')
    op.drop_index('idx_hotels_rating', 'hotels')
    op.drop_index('idx_hotels_location', 'hotels')
    
    op.drop_index('idx_cars_make_model', 'cars')
    op.drop_index('idx_cars_location', 'cars')
    op.drop_index('idx_cars_is_available', 'cars')
    op.drop_index('idx_cars_is_featured', 'cars')
    op.drop_index('idx_cars_price_per_day', 'cars')
    op.drop_index('idx_cars_category', 'cars')