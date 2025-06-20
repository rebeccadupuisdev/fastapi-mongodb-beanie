# Dictionary with ASL and Pictograms

A web application that manages a dictionary of words with their associated American Sign Language (ASL) and pictogram representations, using MongoDB as the database backend with Beanie ODM. The application features both a REST API and a user-friendly web interface.

## Technologies Used

- FastAPI: Modern, fast web framework for building APIs with Python
- MongoDB: NoSQL database
- Beanie: MongoDB ODM (Object Document Mapper) for Python
- Jinja2: Template engine for the web interface
- TailwindCSS: Utility-first CSS framework for the frontend
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
cd dictionary
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

2. Access the application:
- Web Interface: http://localhost:8000
- API Documentation (Swagger UI): http://localhost:8000/docs
- API Documentation (ReDoc): http://localhost:8000/redoc

## Features

### Web Interface
- Browse words by categories
- View detailed word information including:
  - English word
  - Category
  - Pictogram representation
  - ASL video demonstration (when available)
- Responsive design that works on desktop and mobile devices

### API Endpoints

#### Categories
- `GET /api/categories`: Get all categories
- `POST /api/categories`: Create a new category
- `GET /api/categories/{id}`: Get a specific category
- `PUT /api/categories/{id}`: Update a category
- `DELETE /api/categories/{id}`: Delete a category

#### Words
- `GET /api/words`: Get all words
- `POST /api/words`: Create a new word
- `GET /api/words/{id}`: Get a specific word
- `PUT /api/words/{id}`: Update a word
- `DELETE /api/words/{id}`: Delete a word

## Project Structure

```
dictionary/
├── api/                    # API routes
│   ├── category_api.py
│   └── word_api.py
├── frontend/              # Frontend assets and templates
│   ├── static/
│   │   ├── content/      # Static content (videos, images)
│   │   ├── css/         
│   │   └── js/
│   └── templates/        # Jinja2 templates
│       ├── base.html
│       ├── category.html
│       ├── index.html
│       └── word.html
├── infrastructure/        # Configuration and setup
│   ├── mongo_setup.py
│   └── template_config.py
├── models/               # Data models
│   ├── category.py
│   └── word.py
├── services/             # Business logic
│   ├── category_service.py
│   └── word_service.py
├── views/                # Web route handlers
│   ├── category_views.py
│   ├── home_views.py
│   └── word_views.py
└── tests/               # Test files
    ├── api/
    ├── models/
    └── services/
```

## Testing

Run the tests using pytest:
```bash
pytest
```
