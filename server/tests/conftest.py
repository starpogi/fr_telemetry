import pytest
import os

from server import create_app
from server import db


@pytest.fixture(scope="module")
def test_client():
    config = os.environ.get('CIRCLECI_CONFIG', 'configs.test.LocalTest')
    app = create_app(config=config)
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope="function")
def test_db():
    db.create_all()

    yield db

    db.session.rollback()
    db.drop_all()
