import datetime

from celery import shared_task
from flask import current_app

from server import db
from server.controllers import events
from server.models.events import LocationEvent
from server.models.robots import Robot


@shared_task
def push_event(msg, socket):
    try:
        start = datetime.datetime.utcnow()
        csv_data = msg.split(",")

        if len(csv_data) != 4:
            current_app.logger.error("%s Data does not have 4 parts" % msg)
            socket.send("ERR")
            return False

        robot_data = {
            "robot": csv_data[3],
            "x": float(csv_data[0]),
            "y": float(csv_data[1]),
            "timestamp": int(csv_data[2])
        }

        location_event = LocationEvent(**robot_data)

        robot = Robot.query.get(robot_data["robot"])

        if robot is not None:
            current_app.logger.debug("%s Updated" % robot_data["robot"])
            last_event_id = robot.last_event_id
            current_app.logger.debug(last_event_id)
            last_event = LocationEvent.query.get(last_event_id)

            odometer = events.calculate_distance(
                last_event.x,
                last_event.y,
                robot_data["x"],
                robot_data["y"]
            )

            db.session.add(location_event)
            db.session.flush()
            robot.odometer = odometer + robot.odometer
            robot.last_event_id = location_event.id
            robot.last_x = robot_data["x"]
            robot.last_y = robot_data["y"]

            db.session.commit()

        else:
            current_app.logger.debug("%s Added" % robot_data["robot"])
            db.session.add(location_event)
            db.session.flush()
            new_robot = Robot(
                name=robot_data["robot"],
                last_x=robot_data["x"],
                last_y=robot_data["y"],
                last_event_id=location_event.id
            )
            db.session.add(new_robot)
            db.session.commit()

        socket.send("OK")

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(e)

    finally:
        end = datetime.datetime.utcnow()
        current_app.logger.info("Took %s ms" % (end - start))
