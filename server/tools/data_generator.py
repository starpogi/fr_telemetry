"""Generate data for input.

Usage:
    python data_generator.py 1000  > input_1k.csv
    python data_generator.py 10000  > input_10k.csv
    python data_generator.py 100000  > input_100k.csv
    python data_generator.py 1000000  > input_1m.csv
"""

import argparse
import csv
import random
import sys

import click
from flask import current_app

try:
    from flask.cli import AppGroup
except ImportError:
    from flask_cli import AppGroup


@click.command(cls=AppGroup)
def cli():
    """Perform data generators."""

    pass

ROBOT_NAMES ="""Sark
Proto
Test
Uqvroid
Ocstron
Tink
Ehi
Sterling
Clank
Ajnoid
Ibxroid
Terra
Norbit
Beta
Dustie
Adig
Spanner
Talus
Silver
Ubxroid
Imzroid
Socket
Ewoid
Knave
Ox
Spark
Rob Oto
Brobot
Nozzle
Oxef
Rusty
Ejec""".split("\n")


def gen_robot_name(i):
    return ROBOT_NAMES[i%len(ROBOT_NAMES)] + " " + ROBOT_NAMES[i%len(ROBOT_NAMES)]


def gen_robot(name=None):
    return {
        "x": random.random() * 100,
        "y": random.random() * 100,
        "timestamp": i,
        "robot": name or gen_robot_name(i)
    }

def gen_robots(num):
    for i in range(num):
        yield gen_robot()


@cli.command()
@click.argument('nums', default=1)
def generate(nums):
    from server.models import events
    db = current_app.extensions['sqlalchemy'].db

    try:
        for robot in gen_robot(nums):
            event = events.LocationEvent(**robot)
            print(event)
            db.session.add(event)

        db.session.commit()
    finally:
        db.session.rollback()
