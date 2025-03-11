from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from main import app
from tests.conftest import create_mock_token

import sys
sys.path.append("")

client = TestClient(app)

token = create_mock_token(username="test")
headers = {"Authorization": f"Bearer {token}"}


def test_create_blog(mock_session):
    # check authorization
    response = client.post("/blogs/create/", json={"name": "Test Blog", "description": "Test Description"})
    assert response.status_code == 401

    # check create blog api
    response = client.post("/blogs/create/", json={"name": "Test Blog", "description": "Test Description"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Blog"
    assert data["description"] == "Test Description"


def test_blogs(mock_session):
    # check authorization
    response = client.get("/blogs/")
    assert response.status_code == 401

    response = client.get("/blogs/", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    assert len(data) == 2
    assert data[0]["name"] == "Test Blog"
    assert data[0]["description"] == "Test blog description"

    assert data[1]["name"] == "Test Blog2"
    assert data[1]["description"] == "Test blog2 description"


def test_blog_get(mock_session):
    # check authorization
    response = client.get("/blogs/1/")
    assert response.status_code == 401

    # check blog not found
    response = client.get("/blogs/6/", headers=headers)
    assert response.status_code == 404

    response = client.get("/blogs/1", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)

    assert len(data) > 0

    assert data["name"] == "Test Blog"
    assert data["description"] == "Test blog description"


def test_update_blog(mock_session):
    update_data = {
        "name": "Updated Blog",
        "description": "Updated Description"
    }
    # check authorization
    response = client.put("/blogs/update/999", json=update_data)
    assert response.status_code == 401

    # check blog not found
    response = client.put("/blogs/update/999", json=update_data, headers=headers)
    assert response.status_code == 404

    assert response.json()["detail"] == "Blog 999 not found"
    response = client.put("/blogs/update/1", json=update_data, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Updated Blog"
    assert data["description"] == "Updated Description"


def test_delete_blog(mock_session):
    # check authorization
    response = client.delete("/blogs/delete/999")
    assert response.status_code == 401

    # check blog not found
    response = client.delete("/blogs/delete/999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Blog 999 not found"

    response = client.delete("/blogs/delete/1", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
