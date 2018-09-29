from server import db
from sqlalchemy import text
from datetime import datetime


class LocationEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    robot = db.Column(db.String(50), nullable=False)
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, default=datetime.utcnow,
                          nullable=False, server_default=text('0'))

    def __repr__(self):
        return '<Location Event %r (%r, %r)>' % (self.robot, self.x, self.y)
