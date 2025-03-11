from datetime import datetime, timedelta
from unittest.mock import MagicMock

import jwt
import pytest
import sys
import os


def set_env_vars():
    os.environ["SECRET_KEY"] = "test_secret_key"
    os.environ["TESTING"] = "1"
    os.environ["ALGORITHM"] = "HS256"
    os.environ["REDIS_HOST"] = "localhost"
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
    os.environ["PROJECT_NAME"] = "Test Project"
    os.environ["POSTGRES_SERVER"] = "localhost"
    os.environ["POSTGRES_USER"] = "test_user"
    os.environ["POSTGRES_PASSWORD"] = "test_password"


set_env_vars()

sys.path.append("")
from blog_api.model import Blog
from db.session import get_session
from main import app

mock_session = MagicMock()


def override_session():
    try:
        yield mock_session
    finally:
        pass


app.dependency_overrides[get_session] = override_session


@pytest.fixture
def mock_session():
    return mock_session

mock_query = MagicMock()
mock_data = [
    Blog(id=1, name="Test Blog", description="Test blog description"),
    Blog(id=2, name="Test Blog2", description="Test blog2 description"),
]
mock_query.all.return_value = mock_data

mock_session.add = MagicMock()
mock_session.commit = MagicMock()
mock_session.refresh = MagicMock()
mock_session.exec = MagicMock()
mock_session.get = MagicMock()
mock_session.delete = MagicMock()


def get_side_effect(model, blog_id):
    if model == Blog and blog_id == 1:
        return mock_data[0]
    if model == Blog and blog_id == 2:
        return mock_data[1]
    return None


mock_session.get.side_effect = get_side_effect

mock_session.exec.return_value = mock_query


def create_mock_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=5)
    payload = {
        "sub": username,
        "exp": expire
    }
    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return token