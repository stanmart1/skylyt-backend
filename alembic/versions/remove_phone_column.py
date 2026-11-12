"""remove phone column

Revision ID: remove_phone
Revises: fix_booking_ref
Create Date: 2024-01-01 13:00:00.000000

"""
from alembic import op
from app.migration_helpers import (
    table_exists, column_exists, add_column_if_missing,
    create_table_if_missing, create_index_if_missing,
    drop_column_if_exists, rename_column_if_exists,
)

import sqlalchemy as sa

# revision identifiers
revision = 'remove_phone'
down_revision = 'fix_booking_ref'
branch_labels = None
depends_on = None

def upgrade():
    # Remove phone column from users table
    try:
        drop_column_if_exists(op, 'users', 'phone')
    except:
        pass  # Column might not exist

def downgrade():
    # Add phone column back
    add_column_if_missing(op, 'users', sa.Column('phone', sa.String(20), nullable=True))