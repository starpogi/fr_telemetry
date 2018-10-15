from server.controllers import events


def test_calculate_euc_distance():
    assert events.calculate_distance(0, 1, 0, 0) == 1
    assert events.calculate_distance(0, 0, 0, 1) == 1
    assert events.calculate_distance(0, 0, 0, 0) == 0
    assert events.calculate_distance(0, 1, 0, 1) == 0
    assert events.calculate_distance(0, 0, 1, 1) == 1.4142135623730951
