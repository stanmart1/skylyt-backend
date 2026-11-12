"""add currencies table

Revision ID: add_currencies_table
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
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'add_currencies_table'
down_revision = '00_baseline_schema'
branch_labels = None
depends_on = None


def upgrade():
    # Create currencies table
    create_table_if_missing(op, 'currencies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('code', sa.String(length=3), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('symbol', sa.String(length=10), nullable=False),
        sa.Column('rate_to_ngn', sa.Numeric(precision=15, scale=6), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    create_index_if_missing(op, 'idx_currency_code_active', 'currencies', ['code', 'is_active'])
    create_index_if_missing(op, op.f('ix_currencies_code'), 'currencies', ['code'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_currencies_code'), table_name='currencies')
    op.drop_index('idx_currency_code_active', table_name='currencies')
    op.drop_table('currencies')