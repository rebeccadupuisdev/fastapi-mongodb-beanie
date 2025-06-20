from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api import category_api, word_api
from infrastructure.mongo_setup import init_connection
from views import category_views, home_views, word_views


@asynccontextmanager
async def lifespan(api: FastAPI):
    print("Start app...")
    client = await init_connection("words_app")
    yield
    client.close()
    print("Stop app...")


api = FastAPI(lifespan=lifespan)

# Configure CORS
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def configure_routing():
    # API routes
    api.include_router(word_api.router)
    api.include_router(category_api.router)

    # View routes
    api.include_router(home_views.router)
    api.include_router(word_views.router)
    api.include_router(category_views.router)

    # Mount the frontend directory last to ensure API routes take precedence
    api.mount("/static", StaticFiles(directory="frontend/static"), name="static")


def main():
    configure_routing()
    uvicorn.run(api)


if __name__ == "__main__":
    main()
else:
    configure_routing()
