# Social Media Backend

This is the backend for a toy social media application designed to manage user interactions such as account creation, post management, and voting. The backend is built using FastAPI and uses PostgreSQL for data storage, SQLAlchemy for ORM, and Alembic for database migrations.

## Features

- **Users Router**: Handles user account creation and retrieval.
- **Posts Router**: Allows users to view, create, update, and delete posts.
- **Votes Router**: Enables users to upvote posts.
- **Authorization Router**: Enables users to log in to perform the above actions.

## Requirements

- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Poetry (for dependency management)
- Uvicorn (for running the application)

## Installation

To set up the project environment, install Poetry on your machine and follow these steps:

```bash
# Clone the repository
git clone https://github.com/Asrorbek-Orzikulov/social-media-app
cd social-media-app

# Install dependencies
poetry install

# Create and update the database
alembic upgrade head
```

## Configuration

Ensure you have the following environment variables set or update the `.env` file in the project root with your database credentials and other configurations:

```bash
# db settings
DB_HOSTNAME=
DB_PORT=
DB_USERNAME=
DB_PASSWORD=
DB_NAME=

# oauth settings
OAUTH_SECRET_KEY=
OAUTH_ALGORITHM=
OAUTH_EXPIRY_MINUTES=
```

## Running the Application

To run the server, use the following command:

```bash
uvicorn src.main:app --port 8000 --reload
```

This command will start the FastAPI application with live reloading enabled.

## Usage

- To interact with the application, navigate to `http://127.0.0.1:8000/docs` in your web browser to access the Swagger UI, where you can test the API routes.