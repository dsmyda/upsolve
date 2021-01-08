import os
from tinydb import TinyDB, Query
from cement.utils import fs
from .tables.problems_table import ProblemsTable

def database_initialization_hook(app):
    ''' Database init hook run before command processing '''

    app.log.debug("Initializing the upsolve database file")

    db_absolute_path = fs.abspath(app.config.get('upsolve', 'db'))
    app.log.debug('Database file is: %s' % db_absolute_path)

    db_dir = os.path.dirname(db_absolute_path)
    if not os.path.exists(db_dir):
        app.log.debug("Creating parent directory %s" % db_dir)
        os.makedirs(db_dir)

    app.extend('problems_table', ProblemsTable(TinyDB(db_absolute_path)))
    app.log.debug("TinyDB initialization successful, connected to %s" % db_absolute_path)
