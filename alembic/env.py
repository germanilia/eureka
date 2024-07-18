import asyncio
import os
import sys
from time import sleep

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from config.config import settings
from models import Base

# Create an async engine
async_engine = create_async_engine(settings.DATABASE_URL)

target_metadata = Base.metadata

async def create_database_if_not_exists():
    from sqlalchemy import text

    print("Creating database if it doesn't exist...")
    try:
        # Connect to MySQL server without specifying a database
        engine = create_async_engine(f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}")
        async with engine.connect() as connection:
            try:
                print("Creating database...")
                await connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{settings.DB_NAME}`"))
                print(f"Database '{settings.DB_NAME}' created or already exists.")
            except Exception as e:
                print(f"Error creating database: {e}")
        await engine.dispose()
    except Exception as e:
        print(f"Error connecting to MySQL server: {e}")

async def run_migrations_online() -> None:
    await create_database_if_not_exists()
    
    # Now connect to the specific database
    engine = create_async_engine(settings.DATABASE_URL)
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()


def do_run_migrations(connection: Connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_offline() -> None:
    raise NotImplementedError("Offline migrations are not supported.")


# if context.is_offline_mode():
#     run_migrations_offline()
# else:
asyncio.run(run_migrations_online())
