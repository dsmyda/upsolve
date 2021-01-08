
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
from argparse import ArgumentTypeError
from tinydb import Query
import sys

VERSION_BANNER = """ \n
 /$$   /$$                               /$$
| $$  | $$                              | $$
| $$  | $$  /$$$$$$   /$$$$$$$  /$$$$$$ | $$ /$$    /$$ /$$$$$$
| $$  | $$ /$$__  $$ /$$_____/ /$$__  $$| $$|  $$  /$$//$$__  $$
| $$  | $$| $$  \ $$|  $$$$$$ | $$  \ $$| $$ \  $$/$$/| $$$$$$$$
| $$  | $$| $$  | $$ \____  $$| $$  | $$| $$  \  $$$/ | $$_____/
|  $$$$$$/| $$$$$$$/ /$$$$$$$/|  $$$$$$/| $$   \  $/  |  $$$$$$$
\______/ | $$____/ |_______/  \______/ |__/    \_/    \_______/
         | $$
         | $$                                        CLI v%s
         |__/                                 created by dsmyda

%s
      """ % (get_version(), get_version_banner())


class Base(Controller):

    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'Upsolve manages and reminds you about contest problems ' \
        'that you weren\'t able to solve. \nIt also tracks basic stats to help you ' \
        'identify concepts that need more practice.'

        # text displayed at the bottom of --help output
        epilog = 'Usage: upsolve contest -lcw 223 3'

        # controller level arguments. ex: 'upsolv --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    def _default(self):
        """Default action if no sub-command is passed."""
        self.app.args.print_help()
