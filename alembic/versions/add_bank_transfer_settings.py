"""add bank transfer settings

Revision ID: add_bank_transfer_settings
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
revision = 'add_bank_transfer_settings'
down_revision = 'a1b5250353c9'
depends_on = None

def upgrade():
    # Add bank transfer columns to settings table
    add_column_if_missing(op, 'settings', sa.Column('bank_name', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('account_name', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('account_number', sa.String(100), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('is_primary_account', sa.Boolean(), default=True))

def downgrade():
    # Remove bank transfer columns
    drop_column_if_exists(op, 'settings', 'is_primary_account')
    drop_column_if_exists(op, 'settings', 'account_number')
    drop_column_if_exists(op, 'settings', 'account_name')
    drop_column_if_exists(op, 'settings', 'bank_name')