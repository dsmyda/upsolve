from cement import Controller, ex
from ..constants import GREEN, WHITE, DIFFICULTY_DISPLAY, CODES
from argparse import ArgumentTypeError

class Contest(Controller):

    class Meta:
        label = "contest"
        stacked_type = 'embedded'
        stacked_on = 'base'

    def format_contest_options():
        ans = []
        for code in CODES:
            ans.append("%s (%s)" % (code, CODES[code]))
        return ', '.join(ans)

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
            ( ['type'],
              {'help': format_contest_options(),
               'action': 'store',
               'choices': list(CODES.keys()),
               'metavar': "type"}),
            ( ['number'],
              {'help': 'Contest number (Ex: 220) ',
               'action': 'store',
               'type' : validate_integer} ),
            ( ['question'],
              {'help': 'Question number (Ex: 4) ',
               'action': 'store',
               'type' : validate_integer} )
        ],
    )
    def contest(self):
        print()
        log = self.app.log
        contest_code = self.app.pargs.type
        question_number = self.app.pargs.question
        contest_number = self.app.pargs.number

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
