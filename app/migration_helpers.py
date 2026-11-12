"""Guarded (idempotent) DDL helpers for Alembic migrations.

The migration history in this project is partially branched and assumes
several core tables already exist. These helpers make migration DDL safe to
run against any database state (empty, partially migrated, or fully
migrated) by checking table/column/index existence before executing.
"""
from sqlalchemy import inspect as sa_inspect


def _inspector(bind):
    return sa_inspect(bind)


def table_exists(bind, table_name):
    try:
        return _inspector(bind).has_table(table_name)
    except Exception:
        return False


def column_exists(bind, table_name, column_name):
    try:
        insp = _inspector(bind)
        if not insp.has_table(table_name):
            return False
        return any(c["name"] == column_name for c in insp.get_columns(table_name))
    except Exception:
        return False


def index_exists(bind, index_name, table_name):
    try:
        insp = _inspector(bind)
        if not insp.has_table(table_name):
            return False
        names = {ix["name"] for ix in insp.get_indexes(table_name)}
        unique = {
            uq.get("name") for uq in insp.get_unique_constraints(table_name)
        }
        return index_name in names or index_name in unique
    except Exception:
        return False


def add_column_if_missing(op, table_name, column, **kw):
    """op.add_column() that no-ops when the table or column already exists."""
    bind = op.get_bind()
    if not table_exists(bind, table_name):
        print(f"  [skip] add_column {table_name}.{getattr(column, 'name', column)}: table missing")
        return
    if column_exists(bind, table_name, getattr(column, "name", "")):
        return
    op.add_column(table_name, column, **kw)


def create_table_if_missing(op, table_name, *columns, **kw):
    """op.create_table() that no-ops when the table already exists."""
    if table_exists(op.get_bind(), table_name):
        return
    op.create_table(table_name, *columns, **kw)


def create_index_if_missing(op, index_name, table_name, columns, **kw):
    """op.create_index() that no-ops when the table, columns or index are missing/already present."""
    bind = op.get_bind()
    if not table_exists(bind, table_name):
        print(f"  [skip] create_index {index_name}: table {table_name} missing")
        return
    for col in columns:
        if not column_exists(bind, table_name, col):
            print(f"  [skip] create_index {index_name}: column {table_name}.{col} missing")
            return
    if index_exists(bind, index_name, table_name):
        return
    kw.pop("if_not_exists", None)
    op.create_index(index_name, table_name, columns, **kw)


def drop_column_if_exists(op, table_name, column_name, **kw):
    """op.drop_column() that no-ops when the table or column does not exist."""
    bind = op.get_bind()
    if not table_exists(bind, table_name) or not column_exists(bind, table_name, column_name):
        return
    op.drop_column(table_name, column_name, **kw)


def rename_column_if_exists(op, table_name, old_name, new_name, **kw):
    """Rename a column only when the old column exists and the new one does not."""
    bind = op.get_bind()
    if not table_exists(bind, table_name):
        return
    if not column_exists(bind, table_name, old_name):
        return
    if column_exists(bind, table_name, new_name):
        return
    op.alter_column(table_name, old_name, new_column_name=new_name, **kw)


def create_unique_constraint_if_missing(op, constraint_name, table_name, columns, **kw):
    """op.create_unique_constraint() that no-ops when it already exists.

    Note: never wrap raw DDL in try/except inside a migration — a failed
    statement aborts the whole transaction. Pre-check instead.
    """
    bind = op.get_bind()
    if not table_exists(bind, table_name):
        return
    for col in columns:
        if not column_exists(bind, table_name, col):
            return
    if index_exists(bind, constraint_name, table_name):
        return
    # Also skip when an equivalent unique constraint already covers the columns
    try:
        insp = _inspector(bind)
        for uq in insp.get_unique_constraints(table_name):
            if set(uq.get("column_names", [])) == set(columns):
                return
    except Exception:
        pass
    op.create_unique_constraint(constraint_name, table_name, columns, **kw)
