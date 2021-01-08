from cement import Controller, ex
from ..constants import ORANGE, GREEN, WHITE, DIFFICULTY_DISPLAY, CODES
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
            ( ['-qn'],
              {'help': 'Question number (Ex: 4) ',
               'action': 'store',
               'type' : validate_integer,
               'dest' : 'question'} )
        ],
    )
    def contest(self):
        print()
        log = self.app.log
        contest_code = self.app.pargs.type
        question_number = self.app.pargs.question
        contest_number = self.app.pargs.number

        contest_handler = self.app.handler.get('contest_api', contest_code, setup=True)
        if question_number:
            problem_metadata = contest_handler.get_metadata(contest_number, question_number)
            self.app.problems_table.add(problem_metadata)
            print()
            log.debug("Successfully inserted into the problems table: %s" % str(problem_metadata))
            log.info("%s[%s] %s successfully added." %
                (WHITE, DIFFICULTY_DISPLAY[problem_metadata.difficulty], problem_metadata.problem_title + GREEN))
        else:
            problem_metadatas = contest_handler.get_all_questions_metadata(contest_number)
            print()
            self.app.problems_table.add(*problem_metadatas)
            log.debug("Successfully inserted into the problems table: %s" % str(problem_metadatas))
            log.info("Successfully queued the following problems")
            for problem in problem_metadatas:
                log.info("%s[%s] %s" % (
                    WHITE,
                    DIFFICULTY_DISPLAY[problem.difficulty],
                    WHITE + problem.problem_title + GREEN))
        print()
        log.info("Queue currently has %s%d%s problems" % (ORANGE, self.app.problems_table.size(), GREEN))
        log.info("You can view the queue by running %s'upsolve list'" % WHITE)
        log.info("You can reorder the queue by running %s'upsolve shuffle'" % WHITE)
        log.info("You can clear the queue by running %s'upsolve clear'\n" % WHITE)
