import pytest

from server.controllers import events, robots


def test_query_no_robots(test_client, test_db):
    response = test_client.get("/api/robots")
    assert response.status_code == 200
    assert len(response.json) == 0


def test_query_all_robots(test_client, test_api_db):
    response = test_client.get("/api/robots")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['name'] == "Bender"


def test_query_robot(test_client, test_api_db):
    response = test_client.get("/api/robots/Bender")
    assert response.status_code == 200
    assert response.json['name'] == "Bender"


def test_query_wrong_robot(test_client, test_api_db):
    response = test_client.get("/api/robots/Wrong")
    assert response.status_code == 404


def test_query_robot_events(test_client, test_api_db):
    response = test_client.get("/api/robots/Bender/events")
    assert response.status_code == 200
    assert len(response.json) == 3


def test_query_robot_events_trimmed(test_client, test_api_db):
    response = test_client.get("/api/robots/Bender/events?start_time=0&end_time=1")
    assert response.status_code == 200
    assert len(response.json) == 2


def test_query_robot_odometer_trimmed(test_client, test_api_db):
    response = test_client.get("/api/robots/Bender/odometer?start_time=0&end_time=1")
    assert response.status_code == 200
    assert response.json['odometer'] == 1.0


def test_query_robot_odometer_trimmed_full(test_client, test_api_db):
    response = test_client.get("/api/robots/Bender/odometer?start_time=0&end_time=2")
    assert response.status_code == 200
    assert response.json['odometer'] == 2.0


def test_query_robot_odometer(test_client, test_api_db):
    response = test_client.get("/api/robots/Bender/odometer")
    assert response.status_code == 200
    assert response.json['odometer'] == 2.0


def test_query_robot_no_odometer(test_client, test_api_db):
    response = test_client.get("/api/robots/Wrong/odometer")
    assert response.status_code == 200
    assert response.json['odometer'] == 0.0
