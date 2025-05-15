from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine  # Import pour le moteur synchrone
from alembic import context
from models import Base

# Configuration Alembic
config = context.config

# Configuration des logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# MetaData pour les migrations
target_metadata = Base.metadata

# Utiliser un moteur synchrone pour les migrations
def get_url():
    return "postgresql://fastapi_user:fastapi_password@db:5432/fastapi_db"

def run_migrations_offline():
    """Exécuter les migrations en mode hors ligne."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Exécuter les migrations en mode en ligne."""
    connectable = create_engine(get_url())  # Utiliser un moteur synchrone ici

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()