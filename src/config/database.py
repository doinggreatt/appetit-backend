import os
from typing import Annotated

from sqlalchemy import String, Text, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column
from fastapi import Depends

class DatabaseSettings:
    def __init__(self):

        self._read_env()

        engine = self.async_engine  # async engine by default

        self.session = async_sessionmaker(engine, expire_on_commit=False)

    def _read_env(self):
        """Reads ../.envs/.postgres file"""
        try:

            self.USERNAME = os.getenv('POSTGRES_USER')
            self.PASSWORD = os.getenv('POSTGRES_PASSWORD')
            self.HOST = os.getenv('POSTGRES_HOST')
            self.PORT = os.getenv('POSTGRES_PORT')
            self.DB = os.getenv('POSTGRES_DB')

        except Exception as e:
            raise e

    @property
    def DATABASE_URI_psycopg(self):
        psql_uri = f"postgresql+psycopg://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"

        return psql_uri

    @property
    def DATABASE_URI_asyncpg(self):
        psql_uri = f"postgresql+asyncpg://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"
        print(psql_uri)
        return psql_uri

    @property
    def sync_engine(self):
        engine = create_engine(self.DATABASE_URI_psycopg)

        return engine

    @property
    def async_engine(self):

        engine = create_async_engine(self.DATABASE_URI_asyncpg)

        return engine

    async def get_async_session(self):
        async with self.session() as session:
            yield session

    def get_sync_session(self):
        with self.session() as session:
            yield session

db_settings = DatabaseSettings()

SessionDep = Annotated[AsyncSession, Depends(db_settings.get_async_session)]

class BaseModelFieldTypes:
    intpk = Annotated[int, mapped_column(primary_key=True)]
    str_255 = Annotated[str, String(length=255)]
    text = Annotated[str, Text]

# ====== Base Model =========
class Base(DeclarativeBase):
    ...

# ==========================

from sqlalchemy import text

schemas = [
    "users",
    "menu",
    "restaurant",
]

def create_schemas():
    """Create basic schemas"""

    with db_settings.sync_engine.connect() as conn:
        for raw_schema in schemas:
            schema = raw_schema.strip()
            if not schema.isidentifier():
                raise ValueError(f"Invalid schema name: {schema}")

            stmt = f"""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_namespace WHERE nspname = '{schema}'
                ) THEN
                    EXECUTE 'CREATE SCHEMA {schema}';
                END IF;
            END
            $$;
            """
            conn.execute(text(stmt))
        conn.commit()