import pytest

from src.schemas.users import UserResponse
from src.schemas.tokens import TokenResponse
from src.oauth2 import CREDENTIALS_EXCEPTION, verify_access_token
from tests.constants import USER_1_DATA


def test_create_user(client):
    response = client.post("/users", json=USER_1_DATA)
    assert response.status_code == 201
    new_user = UserResponse(**response.json())
    assert new_user.email == USER_1_DATA["email"]


def test_create_existing_user(client, user_1):
    response = client.post("/users", json=USER_1_DATA)
    response_message = response.json()["detail"]
    assert response.status_code == 409
    assert response_message == f"User with email {USER_1_DATA["email"]} already exists!"


def test_login(client, user_1):
    login_data = {"username": USER_1_DATA["email"], "password": USER_1_DATA["password"]}
    response = client.post("/login", data=login_data)
    assert response.status_code == 200

    token = TokenResponse(**response.json())
    verified_token = verify_access_token(token.access_token, CREDENTIALS_EXCEPTION)
    assert verified_token.user_id == user_1.id


@pytest.mark.parametrize("email, password, status_code", [
    (USER_1_DATA["email"], "wrong_password", 403),
    ("wrong_email", USER_1_DATA["password"], 403),
    ("wrong_email", "wrong_password", 403),
    (None, "wrong_password", 422),
    (USER_1_DATA["email"], None, 422)
])
def test_incorrect_login(client, user_1, email, password, status_code):
    login_data = {"username": email, "password": password}
    response = client.post("/login", data=login_data)
    assert response.status_code == status_code
