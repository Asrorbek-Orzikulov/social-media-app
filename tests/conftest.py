from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pytest import fixture

from src.oauth2 import create_access_token
from src.database.postgres import get_db, Base
from src.schemas import UserResponse, PostRecord
from src.main import app
from tests.constants import (
    TESTING_DATABASE_URL,
    USER_1_DATA,
    USER_2_DATA,
    POST_1_DATA,
    POST_2_DATA,
)


test_engine = create_engine(TESTING_DATABASE_URL)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def get_db_test():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


@fixture
def session():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


@fixture
def client(session):
    app.dependency_overrides[get_db] = get_db_test
    client = TestClient(app)
    return client


@fixture
def user_1(client):
    response = client.post("/users", json=USER_1_DATA)
    return UserResponse(**response.json())


@fixture
def authorized_client_1(client, user_1):
    token = create_access_token({"user_id": user_1.id})
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@fixture
def authorized_client_2(client):
    client = TestClient(app)
    response = client.post("/users", json=USER_2_DATA)
    user_id = response.json()["id"]
    token = create_access_token({"user_id": user_id})
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@fixture
def post_1(authorized_client_1):
    response = authorized_client_1.post("/posts", json=POST_1_DATA)
    post_record = PostRecord(**response.json())
    return post_record


@fixture
def post_2(authorized_client_2):
    response = authorized_client_2.post("/posts", json=POST_2_DATA)
    post_record = PostRecord(**response.json())
    return post_record
