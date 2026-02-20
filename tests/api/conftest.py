import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from main import api


@pytest_asyncio.fixture
async def client(db_session):
    async with AsyncClient(
        transport=ASGITransport(app=api), base_url="http://test"
    ) as ac:
        yield ac
