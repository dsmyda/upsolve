from cement import Controller, ex
from ...platforms.leetcode.leetcode import LeetCode

class Push(Controller):

    class Meta:
        label = "push"
        stacked_type = 'embedded'
        stacked_on = 'base'

    def ensure_one_platform(self):
        lc = self.app.pargs.lc
        bs = self.app.pargs.bs

        if (lc and bs) or (not lc and not bs):
            return False
        return True

    def validate_question_number(value):
        ''' Validate the question number, must be an integer. Typically, a value between 1-4.'''

        try:
            return int(value)
        except ValueError:
            raise ArgumentTypeError("%s is an invalid question number." \
            " Please use only integer values (such as [1, 4])" % value)

    def validate_contest_number(value):
        ''' Validate the contest number, must be an integer.'''

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
            ( ['-q'],
              {'help': 'question number',
               'action': 'store',
               'required': 'True',
               'type': validate_question_number,
               'dest': 'question_number' } ),
        ],
    )
    def push(self):
        # Precondition - ensure only one (and exactly one) platform is specified.
        if not self.ensure_one_platform():
            self.app.args.error("Please specify exactly one platform type" \
            " [Hint: try -lc or -bs, use -h for more info]")

        question_number = self.app.pargs.question_number - 1
        contest_number = self.app.pargs.contest_number
        platform = self.app.pargs.lc or self.app.pargs.bs

        if self.app.problems_table.exists(contest_number, question_number):
            self.app.log.info("Problem already exists, exiting...")
            return

        platform_api = self.app.handler.get('platform_api', platform, setup=True)
        metadata = platform_api.get_metadata(contest_number, question_number)

        id = self.app.problems_table.add(metadata)[0]

        self.app.log.debug("Successfully inserted into the problems table: %s" % str(metadata))
        self.app.log.info("%s problem successfully queued." % platform.capitalize())
        self.app.log.info("Problem is currently position %d in the queue." % id)
        self.app.log.info("Consider shuffling for a random order (run 'upsolve shuffle').\n")
