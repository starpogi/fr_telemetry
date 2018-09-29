import math

from server.models.events import LocationEvent
from server import db


def get_events(robots=None, start_time=None, end_time=None):
    filter = []

    if isinstance(robots, (list, tuple)):
        filter.append(LocationEvent.robot.in_(robots))
    elif isinstance(robots, str):
        filter.append(LocationEvent.robot == robots)

    if start_time is not None and end_time is not None \
       and start_time > end_time:
        start_time, end_time = end_time, start_time

    if start_time is not None and end_time is not None:
        filter.append(start_time <= LocationEvent.timestamp)
        filter.append(LocationEvent.timestamp <= end_time)
    elif start_time is None and end_time is not None:
        filter.append(LocationEvent.timestamp <= end_time)
    elif start_time is not None and end_time is None:
        filter.append(start_time <= LocationEvent.timestamp)

    events = LocationEvent.query.filter(*filter)
    return events


def get_odometer(robots=None, start_time=None, end_time=None):
    events = get_events(robots, start_time, end_time)
    odometer = 0.0

    if events.count() == 0:
        return 0.0

    for i in range(events.count() - 2):
        coord_1 = events[i]
        coord_2 = events[i + 1]
        odometer += calculate_distance(coord_1.x, coord_1.y,
                                       coord_2.x, coord_2.y)

    return odometer


def add_event(robot, x, y, timestamp):
    pass


def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
