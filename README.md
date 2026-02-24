# Dictionary with ASL and Pictograms

A web application that manages a dictionary of words with their associated American Sign Language (ASL) and pictogram representations, using MongoDB as the database backend with Beanie ODM. The application features both a REST API and a user-friendly web interface.

## Technologies Used

- FastAPI: Modern, fast web framework for building APIs with Python
- MongoDB: NoSQL database
- Beanie: MongoDB ODM (Object Document Mapper) for Python
- Jinja2: Template engine for the web interface
- TailwindCSS: Utility-first CSS framework for the frontend (loaded via CDN)
- HTMX: For dynamic web interactions (loaded via CDN)
- Docker: For running MongoDB database container
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

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
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
uvicorn main:api --reload
```

2. Access the application:
- Web Interface: http://localhost:8000
- API Documentation (Swagger UI): http://localhost:8000/docs
- API Documentation (ReDoc): http://localhost:8000/redoc

## Features

### Web Interface
- Browse a hierarchical category structure with nested subcategories and words
- View detailed word information including:
  - Word text
  - Category (with full ancestor hierarchy)
  - Pictogram representation
  - ASL video demonstration (when available)
- Pictogram-based breadcrumb navigation showing the full ancestor chain
- Responsive design that works on desktop and mobile devices

### API Endpoints

#### Categories
- `GET /api/categories/{category}`: Get a category by name
- `POST /api/categories`: Create a new category

#### Words
- `GET /api/words`: Get all words
- `GET /api/words/{word}`: Get a word by name
- `POST /api/words`: Create a new word
- `DELETE /api/words/{word}`: Delete a word by name
- `GET /api/pictograms`: Get all pictograms

## Project Structure

```
dictionary/
├── api/                    # API routes
│   ├── category_api.py
│   └── word_api.py
├── frontend/              # Frontend assets and templates
│   ├── static/
│   │   ├── content/      # Static content (videos, images) - gitignored
│   │   │   └── videos/
│   │   ├── css/
│   │   └── js/
│   └── templates/        # Jinja2 templates
│       ├── base.html
│       ├── category.html
│       ├── index.html
│       ├── word.html
│       └── partials/
│           └── breadcrumb.html
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
├── tests/               # Test files
│   ├── api/
│   │   ├── conftest.py
│   │   ├── test_category_api.py
│   │   └── test_word_api.py
│   ├── models/
│   │   ├── test_category.py
│   │   └── test_word.py
│   ├── services/
│   │   ├── test_category_service.py
│   │   └── test_word_service.py
│   └── conftest.py
├── main.py              # Application entry point
├── pytest.ini           # pytest configuration
├── pyproject.toml       # Project configuration (Ruff)
└── requirements.txt     # Python dependencies
```

## Testing

Run the tests using pytest:
```bash
pytest
```
