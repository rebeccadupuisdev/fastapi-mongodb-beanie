import fastapi
import uvicorn

from api import word_api

api = fastapi.FastAPI()


def main():
    configure_routing()

    uvicorn.run(api)


def configure_routing():
    api.include_router(word_api.router)


@api.get("/")
def index():
    return {"Hello world!"}


if __name__ == "__main__":
    main()
else:
    configure_routing()
