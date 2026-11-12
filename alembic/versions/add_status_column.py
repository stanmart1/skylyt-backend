"""Add status column to payments

Revision ID: add_status_column
Revises: fix_payment_enums
Create Date: 2025-09-03 20:52:00.000000

"""
from alembic import op
from app.migration_helpers import (
    table_exists, column_exists, add_column_if_missing,
    create_table_if_missing, create_index_if_missing,
    drop_column_if_exists, rename_column_if_exists,
)

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_status_column'
down_revision = 'fix_payment_enums'
branch_labels = None
depends_on = None

def upgrade():
    # Add status column if it doesn't exist
    add_column_if_missing(op, 'payments', sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'))

def downgrade():
    drop_column_if_exists(op, 'payments', 'status')