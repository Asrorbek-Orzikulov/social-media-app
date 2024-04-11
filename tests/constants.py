from sqlalchemy import URL

from src.config import settings

# database
TESTING_DATABASE_URL = URL.create(
    "postgresql+psycopg",
    username=settings.db_username,
    password=settings.db_password,
    host=settings.db_hostname,
    database="test-db",
)

# users
USER_1_DATA = {"email": "User1@gmail.com", "password": "User1@password12!"}
USER_2_DATA = {"email": "User2@outlook.com", "password": "$Password!User2&^"}

# posts
POST_1_DATA = {"title": "User 1's post", "content": "Content of User 1's post"}
POST_2_DATA = {"title": "User 2's post", "content": "Content of User 2's post"}
UPDATED_POST_DATA = {"title": "Post_title_new", "content": "Post_content_new"}
