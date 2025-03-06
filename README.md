# fastapi-mongodb-beanie-app
FastAPI app with MongoDB and Beanie

**Start MongoDB server in Docker**
```
docker run -d --rm -p 127.0.0.1:27017:27017 -v mongowords:/data/db --name mongowords-srv mongo
```