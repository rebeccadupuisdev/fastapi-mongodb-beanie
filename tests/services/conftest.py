import pytest_asyncio

from infrastructure.mongo_setup import init_connection
from models.word import Word


@pytest_asyncio.fixture(scope="session", autouse=True)
async def words_db_session():
    """
    Create test database
    """
    client = await init_connection("words_app_test")

    yield client

    await client.get_database().drop_collection(Word.get_collection_name())
    client.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def words_db(words_db_session):
    """
    Clear test database
    """
    await words_db_session.get_database().drop_collection(Word.get_collection_name())
