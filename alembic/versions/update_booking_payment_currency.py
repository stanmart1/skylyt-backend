"""update booking and payment currency fields

Revision ID: update_booking_payment_currency
Revises: add_currencies_table
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
revision = 'update_booking_payment_currency'
down_revision = 'add_currencies_table'
branch_labels = None
depends_on = None


def upgrade():
    # Update bookings table
    add_column_if_missing(op, 'bookings', sa.Column('total_amount_ngn', sa.Numeric(precision=15, scale=2), nullable=True))
    add_column_if_missing(op, 'bookings', sa.Column('display_currency', sa.String(length=3), nullable=True))
    add_column_if_missing(op, 'bookings', sa.Column('display_amount', sa.Numeric(precision=15, scale=2), nullable=True))
    
    # Migrate existing data
    op.execute("UPDATE bookings SET total_amount_ngn = total_amount, display_currency = currency, display_amount = total_amount WHERE total_amount_ngn IS NULL")
    
    # Make total_amount_ngn not nullable (server defaults keep ORM inserts,
    # which do not know about these columns, working)
    op.alter_column('bookings', 'total_amount_ngn', nullable=False, server_default='0')
    op.alter_column('bookings', 'display_currency', nullable=False, server_default='NGN')
    
    # Update payments table
    add_column_if_missing(op, 'payments', sa.Column('amount_ngn', sa.Numeric(precision=15, scale=2), nullable=True))
    add_column_if_missing(op, 'payments', sa.Column('display_currency', sa.String(length=3), nullable=True))
    add_column_if_missing(op, 'payments', sa.Column('display_amount', sa.Numeric(precision=15, scale=2), nullable=True))
    
    # Migrate existing data
    op.execute("UPDATE payments SET amount_ngn = amount, display_currency = currency, display_amount = amount WHERE amount_ngn IS NULL")
    
    # Make amount_ngn not nullable (server defaults keep ORM inserts working)
    op.alter_column('payments', 'amount_ngn', nullable=False, server_default='0')
    op.alter_column('payments', 'display_currency', nullable=False, server_default='NGN')


def downgrade():
    # Remove new columns
    drop_column_if_exists(op, 'bookings', 'display_amount')
    drop_column_if_exists(op, 'bookings', 'display_currency')
    drop_column_if_exists(op, 'bookings', 'total_amount_ngn')
    
    drop_column_if_exists(op, 'payments', 'display_amount')
    drop_column_if_exists(op, 'payments', 'display_currency')
    drop_column_if_exists(op, 'payments', 'amount_ngn')