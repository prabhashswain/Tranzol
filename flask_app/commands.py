from flask.cli import with_appcontext
import click
from .extensions import db
from .models import *

@click.command(name='create_table')
@with_appcontext
def create_table():
    db.create_all()