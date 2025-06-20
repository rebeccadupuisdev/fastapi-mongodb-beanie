import pytest_asyncio
from beanie import init_beanie

from infrastructure.mongo_setup import init_connection
from models.category import Category
from models.word import Word


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db_session():
    """
    Create test database and initialize collections
    """
    client = await init_connection("words_app_test")

    # Initialize Beanie with the required document models
    await init_beanie(database=client.get_database(), document_models=[Category, Word])

    yield client

    # Clean up collections after tests
    await client.get_database().drop_collection(Word.get_collection_name())
    await client.get_database().drop_collection(Category.get_collection_name())
    client.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db(db_session):
    """
    Clear test database collections before each test
    """
    await db_session.get_database().drop_collection(Word.get_collection_name())
    await db_session.get_database().drop_collection(Category.get_collection_name())
