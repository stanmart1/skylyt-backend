"""add notification settings

Revision ID: add_notification_settings
Revises: 
Create Date: 2024-12-19 12:00:00.000000

"""
from alembic import op
from app.migration_helpers import (
    table_exists, column_exists, add_column_if_missing,
    create_table_if_missing, create_index_if_missing,
    drop_column_if_exists, rename_column_if_exists,
)

import sqlalchemy as sa

# revision identifiers
revision = 'add_notification_settings'
down_revision = '00_baseline_schema'
depends_on = None

def upgrade():
    # Add notification settings columns to settings table
    add_column_if_missing(op, 'settings', sa.Column('smtp_server', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('smtp_port', sa.Integer(), nullable=True, default=587))
    add_column_if_missing(op, 'settings', sa.Column('smtp_username', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('smtp_password', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('from_email', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('resend_api_key', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('onesignal_app_id', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('onesignal_api_key', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('email_notifications_enabled', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('push_notifications_enabled', sa.Boolean(), nullable=True, default=True))

def downgrade():
    # Remove notification settings columns
    drop_column_if_exists(op, 'settings', 'push_notifications_enabled')
    drop_column_if_exists(op, 'settings', 'email_notifications_enabled')
    drop_column_if_exists(op, 'settings', 'onesignal_api_key')
    drop_column_if_exists(op, 'settings', 'onesignal_app_id')
    drop_column_if_exists(op, 'settings', 'resend_api_key')
    drop_column_if_exists(op, 'settings', 'from_email')
    drop_column_if_exists(op, 'settings', 'smtp_password')
    drop_column_if_exists(op, 'settings', 'smtp_username')
    drop_column_if_exists(op, 'settings', 'smtp_port')
    drop_column_if_exists(op, 'settings', 'smtp_server')