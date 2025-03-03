from beanie import init_beanie
from motor import motor_asyncio

from models.word import Word


async def init_connection(db_name: str):
    conn_str = f"mongodb://localhost:27017/{db_name}"
    client = motor_asyncio.AsyncIOMotorClient(conn_str)

    await init_beanie(database=client[db_name], document_models=[Word])

    print(f"Connected to {db_name}.")
