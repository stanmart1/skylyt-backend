"""Add currency support

Revision ID: add_currency_support
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
revision = 'add_currency_support'
down_revision = '00_baseline_schema'
branch_labels = None
depends_on = None

def upgrade():
    # Create currency_rates table
    create_table_if_missing(op, 'currency_rates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('from_currency', sa.String(length=3), nullable=False),
        sa.Column('to_currency', sa.String(length=3), nullable=False),
        sa.Column('rate', sa.Numeric(precision=10, scale=4), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('from_currency', 'to_currency')
    )
    
    # Create countries table
    create_table_if_missing(op, 'countries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=2), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('currency_code', sa.String(length=3), nullable=False),
        sa.Column('is_supported', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    
    # Add currency fields to existing tables
    add_column_if_missing(op, 'bookings', sa.Column('currency_code', sa.String(length=3), nullable=True, default='NGN'))
    add_column_if_missing(op, 'bookings', sa.Column('exchange_rate', sa.Numeric(precision=10, scale=4), nullable=True, default=1.0))
    add_column_if_missing(op, 'hotels', sa.Column('base_currency', sa.String(length=3), nullable=True, default='NGN'))
    add_column_if_missing(op, 'cars', sa.Column('base_currency', sa.String(length=3), nullable=True, default='NGN'))
    
    # Insert supported countries
    op.execute("""
        INSERT INTO countries (code, name, currency_code, is_supported) VALUES
        ('NG', 'Nigeria', 'NGN', true),
        ('US', 'United States', 'USD', true),
        ('GB', 'United Kingdom', 'GBP', true),
        ('CA', 'Canada', 'USD', true),
        ('DE', 'Germany', 'EUR', true),
        ('FR', 'France', 'EUR', true)
    """)
    
    # Insert initial exchange rates (placeholder values)
    op.execute("""
        INSERT INTO currency_rates (from_currency, to_currency, rate, created_at, updated_at) VALUES
        ('NGN', 'USD', 0.0012, NOW(), NOW()),
        ('NGN', 'GBP', 0.001, NOW(), NOW()),
        ('NGN', 'EUR', 0.0011, NOW(), NOW()),
        ('USD', 'NGN', 830.0, NOW(), NOW()),
        ('GBP', 'NGN', 1000.0, NOW(), NOW()),
        ('EUR', 'NGN', 910.0, NOW(), NOW())
        ON CONFLICT DO NOTHING
    """)

def downgrade():
    drop_column_if_exists(op, 'cars', 'base_currency')
    drop_column_if_exists(op, 'hotels', 'base_currency')
    drop_column_if_exists(op, 'bookings', 'exchange_rate')
    drop_column_if_exists(op, 'bookings', 'currency_code')
    op.drop_table('countries')
    op.drop_table('currency_rates')