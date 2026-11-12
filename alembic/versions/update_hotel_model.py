"""Update hotel model with new fields

Revision ID: update_hotel_model
Revises: add_performance_indexes
Create Date: 2024-01-01 00:00:01.000000

"""
from alembic import op
from app.migration_helpers import (
    table_exists, column_exists, add_column_if_missing,
    create_table_if_missing, create_index_if_missing,
    drop_column_if_exists, rename_column_if_exists,
)

import sqlalchemy as sa

# revision identifiers
revision = 'update_hotel_model'
down_revision = 'add_performance_indexes'
branch_labels = None
depends_on = None

def upgrade():
    # Rename existing columns
    # Rename legacy columns (no-op on schema created from the current models)
    rename_column_if_exists(op, 'hotels', 'rating', 'star_rating')
    rename_column_if_exists(op, 'hotels', 'price', 'price_per_night')
    
    # Add new columns
    add_column_if_missing(op, 'hotels', sa.Column('room_count', sa.Integer(), nullable=False, server_default='1'))
    add_column_if_missing(op, 'hotels', sa.Column('images', sa.JSON(), nullable=True))
    add_column_if_missing(op, 'hotels', sa.Column('features', sa.JSON(), nullable=True))
    add_column_if_missing(op, 'hotels', sa.Column('is_available', sa.Boolean(), nullable=False, server_default='true'))
    add_column_if_missing(op, 'hotels', sa.Column('is_featured', sa.Boolean(), nullable=False, server_default='false'))
    
    # Drop old column
    drop_column_if_exists(op, 'hotels', 'image_url')

def downgrade():
    # Add back old column
    add_column_if_missing(op, 'hotels', sa.Column('image_url', sa.String(), nullable=True))
    
    # Drop new columns
    drop_column_if_exists(op, 'hotels', 'is_featured')
    drop_column_if_exists(op, 'hotels', 'is_available')
    drop_column_if_exists(op, 'hotels', 'features')
    drop_column_if_exists(op, 'hotels', 'images')
    drop_column_if_exists(op, 'hotels', 'room_count')
    
    # Rename columns back
    op.alter_column('hotels', 'price_per_night', new_column_name='price')
    op.alter_column('hotels', 'star_rating', new_column_name='rating')