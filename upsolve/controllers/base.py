
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
from argparse import ArgumentTypeError
from tinydb import Query
import sys
from tabulate import tabulate

VERSION_BANNER = """
Upsolve manages and reminds you about contest problems that you weren't able to solve %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):

    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'Upsolve manages and reminds you about contest problems that you weren\'t able to solve'

        # text displayed at the bottom of --help output
        epilog = 'Usage: upsolve push --lc -c 223 -q 3'

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

    def ensure_one_platform(self):
        lc = self.app.pargs.lc
        bs = self.app.pargs.bs

        if (lc and bs) or (not lc and not bs):
            return False
        return True

    def validate_question_number(value):
        try:
            return int(value)
        except ValueError:
            raise ArgumentTypeError("%s is an invalid question number." \
            " Please use only integer values (such as [1, 4])" % value)

    def validate_contest_number(value):
        try:
            return int(value)
        except ValueError:
            raise ArgumentTypeError("%s is an invalid contest number." \
            " Please use only integer values (such as 225)" % value)

    @ex(
        help='push a new contest question',
        arguments=[
            ( ['-lc'],
              {'help': 'specify the leetcode platform',
              'action': 'store_const',
               'const': 'leetcode'} ),
            ( ['-bs'],
              {'help': 'specify the binarysearch platform',
               'action': 'store_const',
               'const': 'binarysearch'} ),
            ( ['-c'],
              {'help': 'contest number',
               'action': 'store',
               'required': 'True',
               'type': validate_contest_number,
               'dest': 'contest_number' } ),
        ],
    )
    def push(self):
        # Precondition - ensure only one (and exactly one) platform is specified.
        if not self.ensure_one_platform():
            self.app.args.error("Please specify exactly one platform type" \
            " [Hint: try -lc or -bs, use -h for more info]")

        #question_number = self.app.pargs.question_number
        contest_number = self.app.pargs.contest_number
        platform = self.app.pargs.lc or self.app.pargs.bs

        #self.app.log.debug("Enqueueing question %d of" \
        #" contest %d for platform %s" % (question_number, contest_number, platform))

        task = {
            'platform': platform,
            'contest_number': contest_number,
            #'question_number': question_number
        }

        # TODO - Query for the task to avoid duplicates

        todo_table = self.app.db.table('todo')
        id = todo_table.insert(task)

        self.app.log.debug("Successfully inserted into the todo table: %s" % str(task))
        self.app.log.info("%s problem successfully queued." % platform.capitalize())
        self.app.log.info("Problem is currently position %d in the queue." % id)
        self.app.log.info("Consider shuffling for a random order (run 'upsolv shuffle').\n")

    @ex(
        help='pop a contest question'
    )
    def pop(self):
        pass

    @ex(
        help='shuffle the question queue'
    )
    def shuffle(self):
        pass

    @ex(
        help='view questions'
    )
    def view(self):
        todo_table = self.app.db.table('todo')
        task_table = list(todo_table)
        if task_table:
            headers = task_table[0].keys()
            task_table = [task.values() for task in task_table]
            print(tabulate(task_table, headers), "\n")
        else:
            print("Nothing todo!")

    @ex(
        help='clear the question queue'
    )
    def clear(self):
        pending_problems = len(self.app.db.table('todo'))
        self.app.log.warning("Dropping %d pending problem(s)." % pending_problems)

        query = '?'
        while query != 'y' and query != 'n':
            query = input("Are you sure want to continue? [y/n] ")

        if query == 'y':
            self.app.db.drop_table('todo')
            self.app.log.info("Successfully dropped %d problem(s)." \
            " Your queue is now empty.\n" % pending_problems)
        else:
            self.app.log.info("Operation aborted.\n")
