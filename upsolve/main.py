from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .commands.base import Base
from .commands.clear import Clear
from .commands.view import View
from .commands.shuffle import Shuffle
from .commands.pop import Pop
from .commands.push import Push
from .platforms.platform_api import PlatformAPI
from .platforms.leetcode import LeetCode
from .platforms.binarysearch import BinarySearch
from .database.database_init_hook import init_app_database
from .hooks.ascii_art_hook import print_ascii_art

# configuration defaults
CONFIG = init_defaults('upsolve')
CONFIG['upsolve']['db'] = '~/.upsolve/tinydb/upsolve.json'

class Upsolve(App):
    """Upsolve primary application."""

    class Meta:
        label = 'upsolve'
        config_defaults = CONFIG
        exit_on_close = True

        extensions = [
            'yaml', 'colorlog', 'tabulate',
        ]

        config_handler = 'yaml'
        config_file_suffix = '.yml'
        log_handler = 'colorlog'
        output_handler = 'tabulate'

        interfaces = [
            PlatformAPI
        ]

        handlers = [
            # Command handlers
            Base, Clear, View, Shuffle, Pop,Push,
            # Platform API handlers
            LeetCode, BinarySearch
        ]

        hooks = [
            ('pre_setup', print_ascii_art),
            ('post_setup', init_app_database)
        ]

def main():
    with Upsolve() as app:
        try:
            app.run()
        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
