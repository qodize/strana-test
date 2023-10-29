from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


class Database:
    def __init__(
            self,
            db_uri: str,
            echo: bool,
    ):
        self._engine = create_async_engine(
            db_uri,
            echo=echo,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        sessionmaker = async_sessionmaker(self._engine, expire_on_commit=False)
        async with sessionmaker.begin() as session:
            yield session
