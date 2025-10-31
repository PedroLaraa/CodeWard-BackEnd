from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from backend.core.config import settings
from backend.core.db import Base
from backend.models import user, token  # importa os modelos para o Alembic ver

# Configuração do Alembic
config = context.config
fileConfig(config.config_file_name)

# Usa a DATABASE_URL do seu config.py
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
