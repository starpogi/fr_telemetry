import collections
import math
from sqlalchemy import desc, asc

from server.models.events import LocationEvent
from server.models.robots import Robot
from server import db


def get_events(robots=None, start_time=None, end_time=None):
    filter = []

    if isinstance(robots, (list, tuple)):
        filter.append(LocationEvent.robot.in_(robots))
    elif isinstance(robots, str):
        filter.append(LocationEvent.robot == robots)
    else:
        if robots is not None:
            raise TypeError("Robots should be a string, list, or tuple.")

    if start_time is not None:
        start_time = int(start_time)

    if end_time is not None:
        end_time = int(end_time)

    if start_time is not None and start_time < 0:
        raise ValueError("Start Time should be positive.")

    if end_time is not None and end_time < 0:
        raise ValueError("End Time should be positive.")

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
    events = events.order_by(desc(LocationEvent.robot))
    events = events.order_by(asc(LocationEvent.timestamp))

    return events


def get_odometer(robot_name, start_time=None, end_time=None):
    events = get_events(robot_name, start_time, end_time)
    odometer = 0.0

    if events.count() == 0:
        return odometer

    if start_time is None and end_time is None:
        robot = Robot.query.get(robot_name)

        if robot is not None:
            return float(robot.odometer)

    for i in range(events.count() - 1):
        coord_1 = events[i]
        coord_2 = events[i + 1]
        odometer += calculate_distance(coord_1.x, coord_1.y,
                                       coord_2.x, coord_2.y)

    return odometer


def add_event(robot_name, x, y, timestamp):
    if timestamp < 0:
        raise ValueError("Timestamp should be positive.")

    if not isinstance(timestamp, int):
        raise TypeError("Timestamp should be an integer.")

    if not isinstance(x, (int, float)):
        raise TypeError("x-coordinate should be an integer or float.")

    if not isinstance(y, (int, float)):
        raise TypeError("y-coordinate should be an integer or float.")

    if not isinstance(robot_name, str):
        raise TypeError("Robot name should be a string.")

    location_event = LocationEvent(robot=robot_name, x=x, y=y,
                                   timestamp=timestamp)
    db.session.add(location_event)
    db.session.commit()


def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
