"""add updated_at column

Revision ID: add_updated_at
Revises: remove_phone
Create Date: 2024-01-01 14:00:00.000000

"""
from alembic import op
from app.migration_helpers import (
    table_exists, column_exists, add_column_if_missing,
    create_table_if_missing, create_index_if_missing,
    drop_column_if_exists, rename_column_if_exists,
)

import sqlalchemy as sa

# revision identifiers
revision = 'add_updated_at'
down_revision = 'remove_phone'
branch_labels = None
depends_on = None

def upgrade():
    # Add updated_at column to users table
    add_column_if_missing(op, 'users', sa.Column('updated_at', sa.DateTime(), nullable=True))
    
    # Update existing records with current timestamp
    op.execute("UPDATE users SET updated_at = created_at WHERE updated_at IS NULL")
    
    # Make column non-nullable
    op.alter_column('users', 'updated_at', nullable=False)

def downgrade():
    drop_column_if_exists(op, 'users', 'updated_at')