# Dictionary with ASL and Pictograms

A FastAPI application that manages a dictionary of words with their associated American Sign Language (ASL) and pictogram representations, using MongoDB as the database backend with Beanie ODM.

## Technologies Used

- FastAPI: Modern, fast web framework for building APIs with Python
- MongoDB: NoSQL database
- Beanie: MongoDB ODM (Object Document Mapper) for Python
- Docker: For containerization
- pytest: For testing

## Prerequisites

- Python 3.8 or higher
- Docker
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi-mongodb-beanie
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment Setup

1. Start MongoDB server using Docker:
```bash
docker run -d --rm -p 127.0.0.1:27017:27017 -v mongowords:/data/db --name mongowords-srv mongo
```

## Running the Application

1. Start the FastAPI application:
```bash
uvicorn main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Categories
- `GET /categories`: Get all categories
- `POST /categories`: Create a new category
- `GET /categories/{id}`: Get a specific category
- `PUT /categories/{id}`: Update a category
- `DELETE /categories/{id}`: Delete a category

### Words
- `GET /words`: Get all words
- `POST /words`: Create a new word
- `GET /words/{id}`: Get a specific word
- `PUT /words/{id}`: Update a word
- `DELETE /words/{id}`: Delete a word

## Project Structure

```
fastapi-mongodb-beanie/
├── api/                    # API routes
│   ├── category_api.py
│   └── word_api.py
├── infrastructure/         # Database configuration
│   └── mongo_setup.py
├── models/                # Data models
│   ├── category.py
│   └── word.py
├── services/              # Business logic
│   ├── category_service.py
│   └── word_service.py
└── tests/                 # Test files
    ├── api/
    ├── models/
    └── services/
```

## Testing

Run the tests using pytest:
```bash
pytest
```
