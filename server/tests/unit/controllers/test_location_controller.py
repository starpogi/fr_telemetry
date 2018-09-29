from server import db
from server.controllers import location


def test_calculate_euc_distance(test_client):
    assert location.calculate_distance(0, 1, 0, 0) == 1
