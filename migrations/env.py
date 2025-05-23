from logging.config import fileConfig
from sqlalchemy.engine import URL, create_engine
from alembic import context
import sqlalchemy as sa

from app.core.logger import logger
from app.models.base import Base
import os

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
fileConfig(config.config_file_name, disable_existing_loggers=False)

url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="P@ssw0rd",  
    host="10.165.1.63",     
    port=5432,
    database="auth_test_db"
)

# URL для основной базы (для управления базами)
admin_url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="P@ssw0rd",
    host="10.165.1.63",  
    port=5432,
    database="postgres"  # Основная база
)

# URL для целевых баз
databases = {
    "auth_db": URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password="P@ssw0rd",
        host="10.165.1.63",  
        port=5432,
        database="auth_db"
    ),
    "auth_test_db": URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password="P@ssw0rd",
        host="10.165.1.63",  
        port=5432,
        database="auth_test_db"
    )
}

# По умолчанию используем auth_db
target_url = databases.get(os.getenv("TARGET_DB", "auth_db"))

# Создаём движок для админ-доступа
admin_engine = create_engine(admin_url)

logger.debug(f"Admin URL: {admin_url}")
for db_name, url in databases.items():
    logger.debug(f"URL for {db_name}: {url}")

# Устанавливаем URL в конфигурацию
config.set_main_option("sqlalchemy.url", str(target_url))

# engine = create_engine(url)
engine = create_engine(target_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Устанавливаем URL в конфигурацию, чтобы переопределить пустое значение из alembic.ini
#config.set_main_option("sqlalchemy.url", str(url))
#config.set_main_option("sqlalchemy.url", str(target_url))

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# def run_migrations_offline() -> None:
#     """Run migrations in 'offline' mode."""
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#     )

#     with context.begin_transaction():
#         context.run_migrations()

# def run_migrations_online() -> None:
#     """Run migrations in 'online' mode."""
#     # Используем тот же движок, что в отладке
#     with engine.connect() as connection:
#         context.configure(
#             connection=connection,
#             target_metadata=target_metadata
#         )

#         with context.begin_transaction():
#             context.run_migrations()

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=target_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    logger.debug("Проверка и создание баз перед миграциями...")
    # Отдельное подключение без транзакции для создания баз
    with admin_engine.connect() as admin_conn:
        admin_conn.execution_options(isolation_level="AUTOCOMMIT")
        # Проверяем и создаём базы
        for db_name in databases.keys():
            logger.debug(f"Проверка существования базы {db_name}...")
            result = admin_conn.execute(
                sa.text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                {"db_name": db_name}
            ).fetchone()
            if not result:
                logger.debug(f"База {db_name} не существует, создание...")
                admin_conn.execute(sa.text(f"CREATE DATABASE {db_name}"))
                logger.debug(f"База {db_name} создана.")
            else:
                logger.debug(f"База {db_name} уже существует.")

# Применяем миграции к целевой базе
    with engine.connect() as connection:
        logger.debug(f"Применение миграций к {target_url.database}...")
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()
        logger.debug(f"Миграции успешно применены к {target_url.database}.")

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()