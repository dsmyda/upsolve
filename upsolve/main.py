from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .commands.base import Base
from .commands.clear import Clear
from .commands.list import List
from .commands.shuffle import Shuffle
from .commands.next import Next
from .commands.contest import Contest
from .commands.stats import Stats
from .contests.contest_interface import ContestInterface
from .contests.leetcode import LeetcodeWeekly, LeetcodeBiweekly
from .contests.binarysearch import BinarysearchWeekly, BinarysearchEdu
from .database.database_initialization import database_initialization_hook

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
            ContestInterface
        ]

        handlers = [
            # Command handlers
            Base, Clear, List, Shuffle, Next, Contest, Stats,
            # Contest handlers
            LeetcodeWeekly, LeetcodeBiweekly,
            BinarysearchWeekly, BinarysearchEdu
        ]

        hooks = [
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
