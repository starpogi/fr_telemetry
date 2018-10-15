import pytest
import os

from server import create_app
from server import db
from server.models.events import LocationEvent
from server.models.robots import Robot


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


@pytest.fixture(scope="function")
def test_api_db():
    db.create_all()

    db.session.add(LocationEvent(robot="Bender", x=0, y=0, timestamp=0))
    db.session.add(LocationEvent(robot="Bender", x=1, y=0, timestamp=1))
    new_event = LocationEvent(robot="Bender", x=0, y=0, timestamp=2)
    db.session.add(new_event)
    db.session.flush()

    new_robot = Robot(name="Bender", last_x=0.0, last_y=0.0,
                      last_event_id=new_event.id, odometer=2.0)

    db.session.add(new_robot)
    db.session.commit()

    yield db

    db.session.rollback()
    db.drop_all()
