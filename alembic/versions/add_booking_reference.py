"""add booking reference column

Revision ID: add_booking_reference
Revises: add_database_indexes
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
from app.migration_helpers import (
    table_exists, column_exists, add_column_if_missing,
    create_table_if_missing, create_index_if_missing,
    drop_column_if_exists, rename_column_if_exists,
    create_unique_constraint_if_missing,
)

import sqlalchemy as sa

# revision identifiers
revision = 'add_booking_reference'
down_revision = 'add_indexes_001'
branch_labels = None
depends_on = None

def upgrade():
    # Add booking_reference column to bookings table
    add_column_if_missing(op, 'bookings', sa.Column('booking_reference', sa.String(50), nullable=True))
    
    # Update existing records with generated references
    op.execute("""
        UPDATE bookings 
        SET booking_reference = 'BK' || UPPER(SUBSTRING(MD5(RANDOM()::TEXT), 1, 8))
        WHERE booking_reference IS NULL
    """)
    
    # Make column non-nullable and unique (a sibling branch migration may
    # already have added the same constraint — pre-check, never try/except,
    # because a failed statement aborts the migration transaction)
    create_unique_constraint_if_missing(op, 'uq_bookings_booking_reference', 'bookings', ['booking_reference'])

def downgrade():
    op.drop_constraint('uq_bookings_booking_reference', 'bookings', type_='unique')
    drop_column_if_exists(op, 'bookings', 'booking_reference')