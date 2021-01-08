from cement import Controller, ex
from ..constants import GREEN, WHITE, DIFFICULTY_DISPLAY, LEETCODE_WEEKLY_CODE, LEETCODE_BIWEEKLY_CODE, BINARYSEARCH_WEEKLY_CODE, BINARYSEARCH_EDUCATIONAL_CODE
from argparse import ArgumentTypeError

class Contest(Controller):

    class Meta:
        label = "contest"
        stacked_type = 'embedded'
        stacked_on = 'base'

    def ensure_one_contest(self):
        print(self.app.pargs)

    def validate_integer(value):
        try:
            ival = int(value)
            if ival < 0:
                raise ValueError()
            return ival
        except ValueError:
            raise ArgumentTypeError("%s is an invalid question or contest number." \
            " Please use only positive integer values." % value)

    @ex(
        help='Add a new contest problem to the queue',
        arguments=[
            ( ['-' + LEETCODE_WEEKLY_CODE],
              {'help': 'Leetcode Weekly',
              'action': 'store_const',
               'const': LEETCODE_WEEKLY_CODE} ),
            ( ['-' + LEETCODE_BIWEEKLY_CODE],
              {'help': 'Leetcode Biweekly',
               'action': 'store_const',
               'const': LEETCODE_BIWEEKLY_CODE} ),
            ( ['-' + BINARYSEARCH_WEEKLY_CODE],
              {'help': 'Binarysearch Weekly',
               'action': 'store_const',
               'const': BINARYSEARCH_WEEKLY_CODE} ),
            ( ['-' + BINARYSEARCH_EDUCATIONAL_CODE],
              {'help': 'Binarysearch Educational',
               'action': 'store_const',
               'const': BINARYSEARCH_EDUCATIONAL_CODE} ),
            ( ['number'],
              {'help': 'Specify the contest number. Ex: 220 ',
               'action': 'store',
               'type' : validate_integer} ),
            ( ['question'],
              {'help': 'Specify the question number. Ex: 4 ',
               'action': 'store',
               'type' : validate_integer} )
        ],
    )
    def contest(self):
        print()
        # Precondition - ensure only one (and exactly one) platform is specified.
        log = self.app.log
        question_number = self.app.pargs.question
        contest_number = self.app.pargs.number
        # FIX THIS
        contest_code = (self.app.pargs.lcw or
                        self.app.pargs.bsw or
                        self.app.pargs.bse or
                        self.app.pargs.lcb)

        if self.app.problems_table.exists(contest_code, contest_number, question_number):
            log.info("Problem already exists, exiting...")
            return

        contest_handler = self.app.handler.get('contest_api', contest_code, setup=True)
        problem_metadata = contest_handler.get_metadata(contest_number, question_number)

        id = self.app.problems_table.add(problem_metadata)[0]

        log.debug("Successfully inserted into the problems table: %s" % str(problem_metadata))
        log.info("%s Problem %s successfully added." %
            (DIFFICULTY_DISPLAY[problem_metadata.difficulty] + GREEN, WHITE + problem_metadata.problem_title + GREEN))
        log.info("Problem is currently position %d in the queue." % id)
        log.info("Consider shuffling for a random order (run 'upsolve shuffle').\n")
