import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from url_shortener.extensions import db
from url_shortener import appF

migrate = Migrate(appF, db)
manager = Manager(appF)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
