from server import db
from datetime import datetime


class Robot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    external_id = db.Column(db.String(50), nullable=False, unique=True,
                            index=True)
    name = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return '<Robot %r>' % self.name
