from icecream import ic
import pytest

from src.schemas import PostRecord
from src.utils import get_record
from src import models
from tests.constants import POST_1_DATA, POST_2_DATA, UPDATED_POST_DATA


def test_create_post(authorized_client_1, user_1):
    response = authorized_client_1.post("/posts", json=POST_1_DATA)
    post_record = PostRecord(**response.json())
    assert post_record.user.id == user_1.id
    assert response.status_code == 201


def test_create_post_unauthorized(client, user_1):
    response = client.post("/posts", json=POST_1_DATA)
    assert response.status_code == 401


@pytest.mark.parametrize(
    "title, content", [("title1", 3), (None, "content2"), ("title1", None), (5, 3)]
)
def test_create_post_invalid(authorized_client_1, title, content):
    json_content = {"title": title, "content": content}
    response = authorized_client_1.post("/posts", json=json_content)
    assert response.status_code == 422


def test_update_post(session, authorized_client_1, post_1):
    new_json = UPDATED_POST_DATA.copy()
    response = authorized_client_1.put(f"/posts/{post_1.id}", json=new_json)
    assert response.status_code == 204

    post_record = get_record(session, models.Post, "Post ID", post_1.id, False)
    assert post_record.title == new_json["title"]
    assert post_record.content == new_json["content"]


def test_update_post_missing(authorized_client_1):
    new_json = UPDATED_POST_DATA.copy()
    response = authorized_client_1.put(f"/posts/{1}", json=new_json)
    assert response.status_code == 404


def test_update_post_unauthorized(session, authorized_client_1, post_2):
    response = authorized_client_1.put(f"/posts/{post_2.id}", json=UPDATED_POST_DATA)
    assert response.status_code == 401

    post_record = get_record(session, models.Post, "Post ID", post_2.id, False)
    assert post_record.title == POST_2_DATA["title"]
    assert post_record.content == POST_2_DATA["content"]


@pytest.mark.parametrize(
    "title, content", [("title1", 3), (None, "content2"), ("title1", None), (5, 3)]
)
def test_update_post_invalid(authorized_client_1, post_1, title, content):
    json_content = {"title": title, "content": content}
    response = authorized_client_1.put(f"/posts/{post_1.id}", json=json_content)
    assert response.status_code == 422
