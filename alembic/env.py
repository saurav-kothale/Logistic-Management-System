from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.User.user.model.user import User
from app.client.model import Client
from app.vendor.model import Vendor
from app.file_system.model import FileInfo, FileRecord
from app.salary_surat.model.model import SalaryFile
from app.Inventory_in.model import InventoryDB
from app.product.model.model import ProductDB
from app.Inventory_in.category_new.model import NewCategoryDb
from app.Inventory_in.bike_category.model import BikeDb
from app.Inventory_in.city_category.model import CityDb
from app.Inventory_in.color_category.model import ColorDb
from app.Inventory_in.size_category.model import SizeDb
from app.inventory_out.model import ProductOutDb
from app.Inventory_in.product_category.model import ProductCategoryDB

from database.database import Base
import os
from decouple import config

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
USER_NAME = config("DB_USER_NAME")
DB_PASSWORD  = config("DB_PASSWORD")
DB_PORT = config("DB_PORT")
DB_NAME = config("DB_NAME")
DB_HOST = config("DB_HOST")

connection_string = f'postgresql://{USER_NAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

config = context.config
config.set_main_option('sqlalchemy.url', connection_string)
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
