import pytest

from server.controllers import events
from server.models.events import LocationEvent


def test_odometer_no_event(test_client, test_db):
    assert events.get_events().count() == 0


def test_odometer_single_event(test_client, test_db):
    new_events = [
        LocationEvent(robot="Bender", x=0, y=0, timestamp=0)
    ]

    [test_db.session.add(event) for event in new_events]
    test_db.session.commit()

    assert events.get_events().count() == 1
    assert events.get_odometer("Bender") == 0


def test_odometer_two_events(test_client, test_db):
    new_events = [
        LocationEvent(robot="Bender", x=0, y=0, timestamp=0),
        LocationEvent(robot="Bender", x=1, y=0, timestamp=1)
    ]

    [test_db.session.add(event) for event in new_events]
    test_db.session.commit()

    assert events.get_events().count() == 2
    assert events.get_odometer("Bender") == 1


def test_odometer_three_events(test_client, test_db):
    new_events = [
        LocationEvent(robot="Bender", x=0, y=0, timestamp=0),
        LocationEvent(robot="Bender", x=1, y=0, timestamp=1),
        LocationEvent(robot="Bender", x=0, y=0, timestamp=2)
    ]

    [test_db.session.add(event) for event in new_events]
    test_db.session.commit()

    assert events.get_events().count() == 3
    assert events.get_odometer("Bender") == 2


def test_event_filter(test_client, test_db):
    new_events = [
        LocationEvent(robot="Bender", x=0, y=0, timestamp=0),
        LocationEvent(robot="Bender", x=2, y=0, timestamp=2),
        LocationEvent(robot="Bender", x=0, y=4, timestamp=3),
        LocationEvent(robot="Bender", x=1, y=0, timestamp=5),
        LocationEvent(robot="Bender", x=0, y=0, timestamp=7)
    ]

    [test_db.session.add(event) for event in new_events]
    test_db.session.commit()

    assert events.get_events(start_time=3).count() == 3
    assert events.get_events(start_time=5).count() == 2
    assert events.get_events(start_time=7).count() == 1
    assert events.get_events(start_time=10).count() == 0
    assert events.get_events(start_time=0, end_time=5).count() == 4
    assert events.get_events(end_time=5).count() == 4
    assert events.get_events(end_time=2).count() == 2

    with pytest.raises(ValueError):
        events.get_events(end_time="2a").count()

    with pytest.raises(ValueError):
        events.get_events(start_time="2b").count()

    with pytest.raises(ValueError):
        events.get_events(end_time=-2).count()

    with pytest.raises(ValueError):
        events.get_events(start_time=-20).count()

    with pytest.raises(ValueError):
        events.get_events(end_time="2c").count()


def test_event_filter_multiple_robots(test_client, test_db):
    new_events = [
        LocationEvent(robot="Bender", x=0, y=0, timestamp=0),
        LocationEvent(robot="Bender", x=2, y=0, timestamp=2),
        LocationEvent(robot="Bender", x=0, y=4, timestamp=3),
        LocationEvent(robot="Bender", x=1, y=0, timestamp=5),
        LocationEvent(robot="Bender", x=0, y=0, timestamp=7),
        LocationEvent(robot="Calculon", x=3, y=2, timestamp=0),
        LocationEvent(robot="Calculon", x=4, y=3, timestamp=1),
        LocationEvent(robot="Calculon", x=5, y=6, timestamp=4),
        LocationEvent(robot="Calculon", x=1, y=0, timestamp=8),
        LocationEvent(robot="Calculon", x=0, y=0, timestamp=9),
        LocationEvent(robot="Angleyne", x=0, y=0, timestamp=19),
        LocationEvent(robot="Angleyne", x=0, y=0, timestamp=20),
        LocationEvent(robot="Angleyne", x=0, y=0, timestamp=21),
    ]

    [test_db.session.add(event) for event in new_events]
    test_db.session.commit()

    assert events.get_events(start_time=3).count() == 9
    assert events.get_events(start_time=30).count() == 0
    assert events.get_events(start_time=0, end_time=5).count() == 7
    assert events.get_events(end_time=3).count() == 5

    assert events.get_events(robots='Bender', start_time=7).count() == 1
    assert events.get_events(robots=['Bender'], start_time=7).count() == 1
    assert events.get_events(robots=['Bender'], start_time=10).count() == 0
    assert events.get_events(robots=['Bender'], start_time=0, end_time=5).count() == 4

    assert events.get_events(robots=['Bender', 'Angleyne'], start_time=7).count() == 4
    assert events.get_events(robots=['Bender', 'Angleyne'], start_time=0, end_time=5).count() == 4
    assert events.get_events(robots=['Bender', 'Calculon'], start_time=0, end_time=5).count() == 7


def test_add_event(test_client, test_db):
    events.add_event(robot_name="Bender", x=1, y=2, timestamp=0)
    assert events.get_events().count() == 1

    with pytest.raises(TypeError):
        events.add_event(robot_name=1, x=1, y=2, timestamp=0)

    with pytest.raises(TypeError):
        events.add_event(robot_name="Bender", x=1, y=2, timestamp=1.5)

    with pytest.raises(TypeError):
        events.add_event(robot_name="Bender", x="1", y=2, timestamp=0)

    with pytest.raises(TypeError):
        events.add_event(robot_name="Bender", x=1, y="2", timestamp=0)

    with pytest.raises(TypeError):
        events.add_event(robot_name="Bender", x=1, y=2, timestamp="0")

    with pytest.raises(ValueError):
        events.add_event(robot_name="Bender", x=1, y=2, timestamp=-10)
