"""add phone column back

Revision ID: add_phone_back
Revises: remove_phone
Create Date: 2025-01-01 20:52:00.000000

"""
from alembic import op
from app.migration_helpers import (
    table_exists, column_exists, add_column_if_missing,
    create_table_if_missing, create_index_if_missing,
    drop_column_if_exists, rename_column_if_exists,
)

import sqlalchemy as sa

# revision identifiers
revision = 'add_phone_back'
down_revision = 'remove_phone'
branch_labels = None
depends_on = None

def upgrade():
    # Add phone column back to users table
    try:
        add_column_if_missing(op, 'users', sa.Column('phone', sa.String(20), nullable=True))
    except Exception as e:
        print(f"Column might already exist: {e}")

def downgrade():
    # Remove phone column
    try:
        drop_column_if_exists(op, 'users', 'phone')
    except Exception as e:
        print(f"Column might not exist: {e}")