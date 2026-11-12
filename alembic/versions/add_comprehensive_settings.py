"""Add comprehensive settings fields

Revision ID: add_comprehensive_settings
Revises: add_comprehensive_notification_settings
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
revision = 'add_comprehensive_settings'
down_revision = 'add_comprehensive_notification_settings'
branch_labels = None
depends_on = None

def upgrade():
    # General Settings Extensions
    add_column_if_missing(op, 'settings', sa.Column('site_logo', sa.String(500), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('favicon', sa.String(500), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('default_language', sa.String(10), default='en'))
    add_column_if_missing(op, 'settings', sa.Column('default_timezone', sa.String(50), default='UTC'))
    add_column_if_missing(op, 'settings', sa.Column('site_keywords', sa.Text, nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('social_facebook', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('social_twitter', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('social_instagram', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('social_linkedin', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('terms_url', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('privacy_url', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('support_url', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('company_address', sa.Text, nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('company_registration', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('vat_number', sa.String(255), nullable=True))
    
    # Security Settings Extensions
    add_column_if_missing(op, 'settings', sa.Column('password_require_uppercase', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('password_require_lowercase', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('password_require_numbers', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('password_require_symbols', sa.Boolean(), default=False))
    add_column_if_missing(op, 'settings', sa.Column('account_lockout_duration', sa.String(10), default='30'))
    add_column_if_missing(op, 'settings', sa.Column('password_expiry_days', sa.String(10), default='90'))
    add_column_if_missing(op, 'settings', sa.Column('force_password_change', sa.Boolean(), default=False))
    add_column_if_missing(op, 'settings', sa.Column('allow_password_reset', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('captcha_enabled', sa.Boolean(), default=False))
    add_column_if_missing(op, 'settings', sa.Column('ip_whitelist_enabled', sa.Boolean(), default=False))
    add_column_if_missing(op, 'settings', sa.Column('ip_whitelist', sa.Text, nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('ssl_required', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('cookie_secure', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('session_cookie_httponly', sa.Boolean(), default=True))
    
    # Payment Settings Extensions
    add_column_if_missing(op, 'settings', sa.Column('payment_currency', sa.String(10), default='USD'))
    add_column_if_missing(op, 'settings', sa.Column('minimum_payment_amount', sa.String(20), default='1.00'))
    add_column_if_missing(op, 'settings', sa.Column('maximum_payment_amount', sa.String(20), default='10000.00'))
    add_column_if_missing(op, 'settings', sa.Column('payment_processing_fee', sa.String(10), default='2.9'))
    add_column_if_missing(op, 'settings', sa.Column('auto_capture_payments', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('refund_policy_days', sa.String(10), default='30'))
    add_column_if_missing(op, 'settings', sa.Column('partial_refunds_enabled', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('webhook_secret_stripe', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('webhook_secret_paystack', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('webhook_secret_flutterwave', sa.String(255), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('payment_retry_attempts', sa.String(10), default='3'))
    add_column_if_missing(op, 'settings', sa.Column('payment_timeout_minutes', sa.String(10), default='15'))
    
    # Bank Transfer Extensions
    add_column_if_missing(op, 'settings', sa.Column('routing_number', sa.String(50), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('swift_code', sa.String(20), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('iban', sa.String(50), nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('bank_address', sa.Text, nullable=True))
    add_column_if_missing(op, 'settings', sa.Column('account_type', sa.String(20), default='checking'))
    add_column_if_missing(op, 'settings', sa.Column('currency', sa.String(10), default='USD'))
    add_column_if_missing(op, 'settings', sa.Column('minimum_transfer_amount', sa.String(20), default='10.00'))
    add_column_if_missing(op, 'settings', sa.Column('maximum_transfer_amount', sa.String(20), default='50000.00'))
    add_column_if_missing(op, 'settings', sa.Column('transfer_fee', sa.String(20), default='0.00'))
    add_column_if_missing(op, 'settings', sa.Column('processing_time_hours', sa.String(10), default='24'))
    add_column_if_missing(op, 'settings', sa.Column('auto_verification_enabled', sa.Boolean(), default=False))
    add_column_if_missing(op, 'settings', sa.Column('require_reference_number', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('bank_transfer_instructions', sa.Text, nullable=True))
    
    # Feature Settings
    add_column_if_missing(op, 'settings', sa.Column('car_rental_enabled', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('hotel_booking_enabled', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('driver_service_enabled', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('multi_currency_enabled', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('reviews_enabled', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('loyalty_program_enabled', sa.Boolean(), default=False))
    add_column_if_missing(op, 'settings', sa.Column('referral_program_enabled', sa.Boolean(), default=False))
    add_column_if_missing(op, 'settings', sa.Column('chat_support_enabled', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('mobile_app_enabled', sa.Boolean(), default=False))
    add_column_if_missing(op, 'settings', sa.Column('api_access_enabled', sa.Boolean(), default=False))
    add_column_if_missing(op, 'settings', sa.Column('booking_modifications_enabled', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('cancellation_enabled', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('partial_payments_enabled', sa.Boolean(), default=False))
    add_column_if_missing(op, 'settings', sa.Column('group_bookings_enabled', sa.Boolean(), default=False))
    add_column_if_missing(op, 'settings', sa.Column('corporate_accounts_enabled', sa.Boolean(), default=False))
    add_column_if_missing(op, 'settings', sa.Column('maintenance_notifications', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('feature_announcements', sa.Boolean(), default=True))
    add_column_if_missing(op, 'settings', sa.Column('beta_features_enabled', sa.Boolean(), default=False))

def downgrade():
    # Remove Feature Settings
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
    
    # Remove Bank Transfer Extensions
    drop_column_if_exists(op, 'settings', 'bank_transfer_instructions')
    drop_column_if_exists(op, 'settings', 'require_reference_number')
    drop_column_if_exists(op, 'settings', 'auto_verification_enabled')
    drop_column_if_exists(op, 'settings', 'processing_time_hours')
    drop_column_if_exists(op, 'settings', 'transfer_fee')
    drop_column_if_exists(op, 'settings', 'maximum_transfer_amount')
    drop_column_if_exists(op, 'settings', 'minimum_transfer_amount')
    drop_column_if_exists(op, 'settings', 'currency')
    drop_column_if_exists(op, 'settings', 'account_type')
    drop_column_if_exists(op, 'settings', 'bank_address')
    drop_column_if_exists(op, 'settings', 'iban')
    drop_column_if_exists(op, 'settings', 'swift_code')
    drop_column_if_exists(op, 'settings', 'routing_number')
    
    # Remove Payment Settings Extensions
    drop_column_if_exists(op, 'settings', 'payment_timeout_minutes')
    drop_column_if_exists(op, 'settings', 'payment_retry_attempts')
    drop_column_if_exists(op, 'settings', 'webhook_secret_flutterwave')
    drop_column_if_exists(op, 'settings', 'webhook_secret_paystack')
    drop_column_if_exists(op, 'settings', 'webhook_secret_stripe')
    drop_column_if_exists(op, 'settings', 'partial_refunds_enabled')
    drop_column_if_exists(op, 'settings', 'refund_policy_days')
    drop_column_if_exists(op, 'settings', 'auto_capture_payments')
    drop_column_if_exists(op, 'settings', 'payment_processing_fee')
    drop_column_if_exists(op, 'settings', 'maximum_payment_amount')
    drop_column_if_exists(op, 'settings', 'minimum_payment_amount')
    drop_column_if_exists(op, 'settings', 'payment_currency')
    
    # Remove Security Settings Extensions
    drop_column_if_exists(op, 'settings', 'session_cookie_httponly')
    drop_column_if_exists(op, 'settings', 'cookie_secure')
    drop_column_if_exists(op, 'settings', 'ssl_required')
    drop_column_if_exists(op, 'settings', 'ip_whitelist')
    drop_column_if_exists(op, 'settings', 'ip_whitelist_enabled')
    drop_column_if_exists(op, 'settings', 'captcha_enabled')
    drop_column_if_exists(op, 'settings', 'allow_password_reset')
    drop_column_if_exists(op, 'settings', 'force_password_change')
    drop_column_if_exists(op, 'settings', 'password_expiry_days')
    drop_column_if_exists(op, 'settings', 'account_lockout_duration')
    drop_column_if_exists(op, 'settings', 'password_require_symbols')
    drop_column_if_exists(op, 'settings', 'password_require_numbers')
    drop_column_if_exists(op, 'settings', 'password_require_lowercase')
    drop_column_if_exists(op, 'settings', 'password_require_uppercase')
    
    # Remove General Settings Extensions
    drop_column_if_exists(op, 'settings', 'vat_number')
    drop_column_if_exists(op, 'settings', 'company_registration')
    drop_column_if_exists(op, 'settings', 'company_address')
    drop_column_if_exists(op, 'settings', 'support_url')
    drop_column_if_exists(op, 'settings', 'privacy_url')
    drop_column_if_exists(op, 'settings', 'terms_url')
    drop_column_if_exists(op, 'settings', 'social_linkedin')
    drop_column_if_exists(op, 'settings', 'social_instagram')
    drop_column_if_exists(op, 'settings', 'social_twitter')
    drop_column_if_exists(op, 'settings', 'social_facebook')
    drop_column_if_exists(op, 'settings', 'site_keywords')
    drop_column_if_exists(op, 'settings', 'default_timezone')
    drop_column_if_exists(op, 'settings', 'default_language')
    drop_column_if_exists(op, 'settings', 'favicon')
    drop_column_if_exists(op, 'settings', 'site_logo')