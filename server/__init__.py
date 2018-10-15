import os

from celery import Celery
from flask import Flask
from flask_alembic import Alembic
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_sockets import Sockets

from server.tools import data_generator

alembic = Alembic()
db = SQLAlchemy()
ma = Marshmallow()
ws = Sockets()

def create_app(config=None):
    config = config or os.environ['CONFIG']
    app = Flask(__name__)

    app.config.from_object(config)
    alembic.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    ws.init_app(app)

    from server import views
    from server import models

    app.register_blueprint(views.api.blueprint)
    app.register_blueprint(views.stream.blueprint)

    app.cli.add_command(data_generator.cli, "tools")

    return app


def init_celery(app=None, config=None):
    config = config or os.environ['CONFIG']
    app = app or create_app(config)
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery

celery = init_celery()
