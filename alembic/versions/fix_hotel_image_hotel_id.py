"""fix_hotel_image_hotel_id

Revision ID: fix_hotel_image_hotel_id
Revises: add_car_images_table
Create Date: 2024-01-01 00:00:01.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fix_hotel_image_hotel_id'
down_revision = 'add_car_images_table'
branch_labels = None
depends_on = None


def upgrade():
    # NO-OP. hotel_images.hotel_id must stay Integer: it is a foreign key to
    # hotels.id (Integer). Converting the column to String (as this revision
    # originally did) makes the FK impossible to create, which in turn aborts
    # Base.metadata.create_all() and left fresh databases without schema.
    pass


def downgrade():
    pass
