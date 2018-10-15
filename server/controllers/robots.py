from server.models.robots import Robot


def get_robots(name=None):
    if name is None:
        return Robot.query.all()

    return Robot.query.get(name)
