"""Fix monetary precision - replace Float with Numeric

Revision ID: fix_monetary_precision
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'fix_monetary_precision'
down_revision = '00_baseline_schema'
branch_labels = None
depends_on = None


def _is_float_column(table, column):
    """True when the column currently holds a float/double type (legacy schema)."""
    from sqlalchemy import inspect
    insp = inspect(op.get_bind())
    try:
        for col in insp.get_columns(table):
            if col["name"] == column:
                return "float" in str(col["type"]).lower() or "double" in str(col["type"]).lower()
    except Exception:
        return False
    return False


def upgrade():
    # Convert legacy Float monetary columns to Numeric. Tables created from
    # the baseline schema already use Numeric and must be left untouched
    # (re-running this would narrow their precision).
    if _is_float_column('payments', 'amount'):
        op.alter_column('payments', 'amount',
                        existing_type=sa.Float(),
                        type_=sa.Numeric(precision=15, scale=2),
                        existing_nullable=False)

    if _is_float_column('payments', 'refund_amount'):
        op.alter_column('payments', 'refund_amount',
                        existing_type=sa.Float(),
                        type_=sa.Numeric(precision=15, scale=2),
                        existing_nullable=True)

    if _is_float_column('bookings', 'total_amount'):
        op.alter_column('bookings', 'total_amount',
                        existing_type=sa.Float(),
                        type_=sa.Numeric(precision=15, scale=2),
                        existing_nullable=False)


def downgrade():
    # Revert bookings table
    op.alter_column('bookings', 'total_amount',
                    existing_type=sa.Numeric(precision=10, scale=2),
                    type_=sa.Float(),
                    existing_nullable=False)
    
    # Revert payments table
    op.alter_column('payments', 'refund_amount',
                    existing_type=sa.Numeric(precision=10, scale=2),
                    type_=sa.Float(),
                    existing_nullable=True)
    
    op.alter_column('payments', 'amount',
                    existing_type=sa.Numeric(precision=10, scale=2),
                    type_=sa.Float(),
                    existing_nullable=False)