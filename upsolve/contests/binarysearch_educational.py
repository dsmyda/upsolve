from .contest_interface import ContestInterface
from cement import Handler
from ..constants import BINARYSEARCH_EDUCATIONAL_CODE, BINARYSEARCH, platform_display, GREEN
from .utils.binarysearch_helper import query_problem_instances, verify_question_number

class BinarysearchEdu(ContestInterface, Handler):

    class Meta:
        label = BINARYSEARCH_EDUCATIONAL_CODE

    def get_contest_problem(self, contest_number, question_number):
        problems = self.get_contest_problems(contest_number)
        verify_question_number(problems, question_number, self.app.log)
        return problems[question_number - 1]

    def get_contest_problems(self, contest_number):
        self.app.log.info("Querying %s for all educational question metadata..." % (platform_display(BINARYSEARCH) + GREEN))
        metadata = {
            'contest_number' : contest_number,
            'code' : BINARYSEARCH_EDUCATIONAL_CODE,
            'type' : 'eduContests'
        }
        return query_problem_instances(contest_number, metadata, self.app.log)
