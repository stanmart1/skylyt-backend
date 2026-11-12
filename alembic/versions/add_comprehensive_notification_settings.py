"""Add comprehensive notification settings

Revision ID: add_comprehensive_notification_settings
Revises: add_notification_settings
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
revision = 'add_comprehensive_notification_settings'
down_revision = 'add_notification_settings'
branch_labels = None
depends_on = None

def upgrade():
    # Add new notification settings columns
    add_column_if_missing(op, 'settings', sa.Column('sms_enabled', sa.Boolean(), default=False))
    add_column_if_missing(op, 'settings', sa.Column('push_notifications_enabled', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('booking_notifications', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('payment_notifications', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('system_notifications', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('driver_notifications', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('admin_notifications', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('notification_frequency', sa.String(50), default='immediate'))
    add_column_if_missing(op, 'settings', sa.Column('quiet_hours_start', sa.String(10), default='22:00'))
    add_column_if_missing(op, 'settings', sa.Column('quiet_hours_end', sa.String(10), default='08:00'))
    add_column_if_missing(op, 'settings', sa.Column('timezone', sa.String(50), default='UTC'))

def downgrade():
    # Remove the added columns
    drop_column_if_exists(op, 'settings', 'timezone')
    drop_column_if_exists(op, 'settings', 'quiet_hours_end')
    drop_column_if_exists(op, 'settings', 'quiet_hours_start')
    drop_column_if_exists(op, 'settings', 'notification_frequency')
    drop_column_if_exists(op, 'settings', 'admin_notifications')
    drop_column_if_exists(op, 'settings', 'driver_notifications')
    drop_column_if_exists(op, 'settings', 'system_notifications')
    drop_column_if_exists(op, 'settings', 'payment_notifications')
    drop_column_if_exists(op, 'settings', 'booking_notifications')
    drop_column_if_exists(op, 'settings', 'push_notifications_enabled')
    drop_column_if_exists(op, 'settings', 'sms_enabled')