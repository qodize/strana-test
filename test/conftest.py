from contextlib import ExitStack

import httpx
import pytest
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor

from app.data.db.database import Database
from app.data.db.models import Base
from app.main import get_app

pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return 'asyncio'


test_db = factories.postgresql_proc(port=None, dbname="test_db")


@pytest.fixture(autouse=True)
async def test_database(test_db):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
            pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password
    ):
        connection_str = f"postgresql+asyncpg://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        database = Database(
            connection_str,
            echo=True
        )
        async with database._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        yield database


@pytest.fixture(autouse=True)
def _app(test_database):
    with ExitStack():
        __app = get_app()
        with __app.metrics_container.db.override(test_database):
            yield __app


@pytest.fixture
async def client(_app):
    async with httpx.AsyncClient(app=_app, base_url='http://test') as ac:
        yield ac
