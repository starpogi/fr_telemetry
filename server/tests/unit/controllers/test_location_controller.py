from server.controllers import location


def test_calculate_euc_distance():
    assert location.calculate_distance(0, 1, 0, 0) == 1
    assert location.calculate_distance(0, 0, 0, 1) == 1
    assert location.calculate_distance(0, 0, 0, 0) == 0
    assert location.calculate_distance(0, 1, 0, 1) == 0
    assert location.calculate_distance(0, 0, 1, 1) == 1.4142135623730951
