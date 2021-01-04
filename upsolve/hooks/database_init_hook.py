import os
from tinydb import TinyDB, Query
from cement.utils import fs

def init_app_database(app):
    app.log.debug("Initializing the upsolve database file")

    db_absolute_path = fs.abspath(app.config.get('upsolve', 'db'))
    app.log.debug('Database file is: %s' % db_absolute_path)

    db_dir = os.path.dirname(db_absolute_path)
    if not os.path.exists(db_dir):
        app.log.debug("Creating parent directory %s" % db_dir)
        os.makedirs(db_dir)

    app.extend('db', TinyDB(db_absolute_path))
    app.log.debug("TinyDB initialization successful, connected to %s" % db_absolute_path)

    create_templates_table(app)

def create_templates_table(app):
    app.log.debug("Creating the templates table if it doesn't already exist.")
    app.db.table("templates")
