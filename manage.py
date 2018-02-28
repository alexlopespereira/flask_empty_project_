#!/usr/bin/env python

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from api import create_app
from api.v1_0.models import User

app, db = create_app('config.DevelopmentConfig')

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(email="ad@min.com", password="admin", admin=True))
    db.session.commit()

if __name__ == '__main__':
    manager.run()
