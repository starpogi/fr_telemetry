import pytest
from server import create_app


@pytest.fixture(scope="module")
def test_client():
    app = create_app(config='configs.test.Test')
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope="module")
def init_database():
    db.create_all()

    yield db

    db.drop_all()
