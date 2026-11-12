"""add children count to bookings

Revision ID: add_children_count
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


# revision identifiers, used by Alembic.
revision = 'add_children_count'
down_revision = '00_baseline_schema'
branch_labels = None
depends_on = None


def upgrade():
    # Add children_count column to bookings table
    add_column_if_missing(op, 'bookings', sa.Column('children_count', sa.Integer(), nullable=True, default=0))


def downgrade():
    # Remove children_count column from bookings table
    drop_column_if_exists(op, 'bookings', 'children_count')