"""add missing settings columns

Revision ID: add_missing_settings_columns
Revises: 0564db9c49e4
Create Date: 2025-01-09 14:20:00.000000

"""
from alembic import op
from app.migration_helpers import (
    table_exists, column_exists, add_column_if_missing,
    create_table_if_missing, create_index_if_missing,
    drop_column_if_exists, rename_column_if_exists,
)

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_missing_settings_columns'
down_revision = '0564db9c49e4'
branch_labels = None
depends_on = None


def upgrade():
    # Add missing notification columns
    add_column_if_missing(op, 'settings', sa.Column('sms_enabled', sa.Boolean(), nullable=True, default=False))
    add_column_if_missing(op, 'settings', sa.Column('push_notifications_enabled', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('booking_notifications', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('payment_notifications', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('system_notifications', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('driver_notifications', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('admin_notifications', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('notification_frequency', sa.String(50), nullable=True, default='immediate'))
    add_column_if_missing(op, 'settings', sa.Column('quiet_hours_start', sa.String(10), nullable=True, default='22:00'))
    add_column_if_missing(op, 'settings', sa.Column('quiet_hours_end', sa.String(10), nullable=True, default='08:00'))
    add_column_if_missing(op, 'settings', sa.Column('timezone', sa.String(50), nullable=True, default='UTC'))
    
    # Add missing Google Analytics columns
    add_column_if_missing(op, 'settings', sa.Column('google_analytics_tracking_id', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('google_analytics_measurement_id', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('google_analytics_api_key', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('google_analytics_enabled', sa.Boolean(), nullable=True, default=False))
    
    # Add missing bank transfer columns
    add_column_if_missing(op, 'settings', sa.Column('bank_address', sa.Text(), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('account_type', sa.String(20), nullable=True, default='checking'))
    add_column_if_missing(op, 'settings', sa.Column('currency', sa.String(10), nullable=True, default='USD'))
    add_column_if_missing(op, 'settings', sa.Column('transfer_fee', sa.String(20), nullable=True, default='0.00'))
    add_column_if_missing(op, 'settings', sa.Column('processing_time_hours', sa.String(10), nullable=True, default='24'))
    add_column_if_missing(op, 'settings', sa.Column('auto_verification_enabled', sa.Boolean(), nullable=True, default=False))
    add_column_if_missing(op, 'settings', sa.Column('require_reference_number', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('bank_transfer_instructions', sa.Text(), nullable=True))
    
    # Add missing webhook columns
    add_column_if_missing(op, 'settings', sa.Column('webhook_secret_stripe', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('webhook_secret_paystack', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('webhook_secret_flutterwave', sa.String(255), nullable=True))
    
    # Add missing feature columns
    add_column_if_missing(op, 'settings', sa.Column('car_rental_enabled', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('hotel_booking_enabled', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('driver_service_enabled', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('multi_currency_enabled', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('reviews_enabled', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('loyalty_program_enabled', sa.Boolean(), nullable=True, default=False))
    add_column_if_missing(op, 'settings', sa.Column('referral_program_enabled', sa.Boolean(), nullable=True, default=False))
    add_column_if_missing(op, 'settings', sa.Column('chat_support_enabled', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('mobile_app_enabled', sa.Boolean(), nullable=True, default=False))
    add_column_if_missing(op, 'settings', sa.Column('api_access_enabled', sa.Boolean(), nullable=True, default=False))
    add_column_if_missing(op, 'settings', sa.Column('booking_modifications_enabled', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('cancellation_enabled', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('partial_payments_enabled', sa.Boolean(), nullable=True, default=False))
    add_column_if_missing(op, 'settings', sa.Column('group_bookings_enabled', sa.Boolean(), nullable=True, default=False))
    add_column_if_missing(op, 'settings', sa.Column('corporate_accounts_enabled', sa.Boolean(), nullable=True, default=False))
    add_column_if_missing(op, 'settings', sa.Column('maintenance_notifications', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('feature_announcements', sa.Boolean(), nullable=True, default=True))
    add_column_if_missing(op, 'settings', sa.Column('beta_features_enabled', sa.Boolean(), nullable=True, default=False))


def downgrade():
    # Remove all added columns
    drop_column_if_exists(op, 'settings', 'beta_features_enabled')
    drop_column_if_exists(op, 'settings', 'feature_announcements')
    drop_column_if_exists(op, 'settings', 'maintenance_notifications')
    drop_column_if_exists(op, 'settings', 'corporate_accounts_enabled')
    drop_column_if_exists(op, 'settings', 'group_bookings_enabled')
    drop_column_if_exists(op, 'settings', 'partial_payments_enabled')
    drop_column_if_exists(op, 'settings', 'cancellation_enabled')
    drop_column_if_exists(op, 'settings', 'booking_modifications_enabled')
    drop_column_if_exists(op, 'settings', 'api_access_enabled')
    drop_column_if_exists(op, 'settings', 'mobile_app_enabled')
    drop_column_if_exists(op, 'settings', 'chat_support_enabled')
    drop_column_if_exists(op, 'settings', 'referral_program_enabled')
    drop_column_if_exists(op, 'settings', 'loyalty_program_enabled')
    drop_column_if_exists(op, 'settings', 'reviews_enabled')
    drop_column_if_exists(op, 'settings', 'multi_currency_enabled')
    drop_column_if_exists(op, 'settings', 'driver_service_enabled')
    drop_column_if_exists(op, 'settings', 'hotel_booking_enabled')
    drop_column_if_exists(op, 'settings', 'car_rental_enabled')
    drop_column_if_exists(op, 'settings', 'webhook_secret_flutterwave')
    drop_column_if_exists(op, 'settings', 'webhook_secret_paystack')
    drop_column_if_exists(op, 'settings', 'webhook_secret_stripe')
    drop_column_if_exists(op, 'settings', 'bank_transfer_instructions')
    drop_column_if_exists(op, 'settings', 'require_reference_number')
    drop_column_if_exists(op, 'settings', 'auto_verification_enabled')
    drop_column_if_exists(op, 'settings', 'processing_time_hours')
    drop_column_if_exists(op, 'settings', 'transfer_fee')
    drop_column_if_exists(op, 'settings', 'currency')
    drop_column_if_exists(op, 'settings', 'account_type')
    drop_column_if_exists(op, 'settings', 'bank_address')
    drop_column_if_exists(op, 'settings', 'google_analytics_enabled')
    drop_column_if_exists(op, 'settings', 'google_analytics_api_key')
    drop_column_if_exists(op, 'settings', 'google_analytics_measurement_id')
    drop_column_if_exists(op, 'settings', 'google_analytics_tracking_id')
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