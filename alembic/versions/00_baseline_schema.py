"""baseline schema

Creates the complete application schema from the SQLAlchemy models.
This is the root of the migration chain: the historical migrations below it
were written against a database whose base tables (users, cars, hotels,
bookings, ...) already existed, so a fresh database could never be migrated
successfully. With this baseline, `alembic upgrade head` produces a complete
schema on any database; the later migrations then only apply guarded,
incremental fixes.

Revision ID: 00_baseline_schema
Revises:
Create Date: 2026-11-12

"""
from alembic import op

# revision identifiers
revision = '00_baseline_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Import every model module so each table is registered on Base.metadata.
    # (app.models.__init__ does not import all of them, e.g. Settings,
    # AboutSettings and CurrencyRate live in their own modules.)
    import importlib
    import pkgutil
    import app.models as models_pkg

    for module in pkgutil.iter_modules(models_pkg.__path__):
        importlib.import_module(f"{models_pkg.__name__}.{module.name}")

    from app.core.database import Base

    Base.metadata.create_all(bind=op.get_bind(), checkfirst=True)


def downgrade():
    # Intentionally a no-op: dropping the baseline schema would destroy
    # all application data. Do not run `alembic downgrade base` in production.
    pass
