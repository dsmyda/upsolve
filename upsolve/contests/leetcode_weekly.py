from .contest_interface import ContestInterface
from cement import Handler
from ..constants import GREEN, LEETCODE_WEEKLY_CODE, platform_display, LEETCODE
from .utils.leetcode_helper import query_problem_instances, verify_question_number

class LeetcodeWeekly(ContestInterface, Handler):

    class Meta:
        label = LEETCODE_WEEKLY_CODE

    def get_contest_problems(self, contest_number):
        self.app.log.info("Querying %s for contest metadata..." % (platform_display(LEETCODE) + GREEN))

        metadata = {
            'contest_number' : contest_number,
            'code' : LEETCODE_WEEKLY_CODE
        }
        contest_slug = "weekly-contest-%d" % contest_number
        return query_problem_instances(contest_slug, metadata)

    def get_contest_problem(self, contest_number, question_number):
        instances = self.get_contest_problems(contest_number)
        verify_question_number(instances, question_number, self.app.log)
        return instances[question_number - 1]
