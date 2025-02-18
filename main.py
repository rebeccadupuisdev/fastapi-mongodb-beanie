from contextlib import asynccontextmanager

import uvicorn
from beanie import init_beanie
from fastapi import FastAPI
from motor import motor_asyncio

from api import word_api
from models.word import Word


@asynccontextmanager
async def lifespan(api: FastAPI):
    print("Start app...")
    await init_connection("words_app")
    yield
    print("Stop app...")


api = FastAPI(lifespan=lifespan)


def main():
    configure_routing()

    uvicorn.run(api)


async def init_connection(db_name: str):
    conn_str = f"mongodb://localhost:27017/{db_name}"
    client = motor_asyncio.AsyncIOMotorClient(conn_str)

    await init_beanie(database=client[db_name], document_models=[Word])

    print(f"Connected to {db_name}.")


def configure_routing():
    api.include_router(word_api.router)


@api.get("/")
def index():
    return {"Hello world!"}


if __name__ == "__main__":
    main()
