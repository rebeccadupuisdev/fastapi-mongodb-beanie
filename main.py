from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import word_api
from infrastructure.mongo_setup import init_connection


@asynccontextmanager
async def lifespan(api: FastAPI):
    print("Start app...")
    client = await init_connection("words_app")
    yield
    client.close()
    print("Stop app...")


api = FastAPI(lifespan=lifespan)


@api.get("/", include_in_schema=False)
def index():
    return {"message": "Hello world!"}


def configure_routing():
    api.include_router(word_api.router)


def main():
    configure_routing()

    uvicorn.run(api)


if __name__ == "__main__":
    main()
else:
    configure_routing()
