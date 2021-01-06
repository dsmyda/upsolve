from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .commands.base import Base
from .commands.drop import Drop
from .commands.list import List
from .commands.shuffle import Shuffle
from .commands.next import Next
from .commands.new import New
from .platforms.platform_api import PlatformAPI
from .platforms.leetcode import LeetCode
from .platforms.binarysearch import BinarySearch
from .database.database_initialization import database_initialization_hook
from .hooks.ascii_banner import show_ascii_banner

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
            Base, Drop, List, Shuffle, Next, New,
            # Platform API handlers
            LeetCode, BinarySearch
        ]

        hooks = [
            ('pre_setup', show_ascii_banner),
            ('post_setup', database_initialization_hook)
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
