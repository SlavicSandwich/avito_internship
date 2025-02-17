from logging.config import fileConfig
import os
from sqlalchemy import create_engine, pool
from alembic import context

from app.models import Base

target_metadata = Base.metadata

config = context.config
fileConfig(config.config_file_name)

def get_database_url():
    return f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

def run_migrations_offline():
    """Запуск миграций в offline-режиме (генерация SQL)."""
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Запуск миграций в online-режиме (непосредственное выполнение)."""
    connectable = create_engine(
        get_database_url(),
        poolclass=pool.NullPool
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()