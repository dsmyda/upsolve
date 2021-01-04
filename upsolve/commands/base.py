
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
from argparse import ArgumentTypeError
from tinydb import Query
import sys

VERSION_BANNER = """
Upsolve manages and reminds you about contest problems that you weren't able to solve
%s
""" % (get_version_banner())


class Base(Controller):

    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'Upsolve manages and reminds you about contest problems that you weren\'t able to solve'

        # text displayed at the bottom of --help output
        epilog = 'Usage: upsolve push -lc -c 223 -q 3'

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
