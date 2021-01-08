from .contest_interface import ContestInterface
from cement import Handler
from ..database.problem import Problem
import requests, json, sys
from ..constants import PLATFORM_DISPLAY, LEETCODE, LEETCODE_WEEKLY_CODE, LEETCODE_BIWEEKLY_CODE, EASY, MEDIUM, HARD

# Indexed by question in the contest, the keys
# are not integer values taken from question metadata
DIFFICULTY = {
    1: EASY,
    2: MEDIUM,
    3: MEDIUM,
    4: HARD
}

PROBLEM_URL_TEMPLATE = "https://leetcode.com/problems/%s/"

def query(log, code, contest_number, question_number, template):
    contest_metadata = get_contest_metadata(log, template % contest_number)
    question_metadata = get_question_metadata(log, contest_metadata, question_number)

    problem = Problem()
    problem.platform = LEETCODE
    problem.contest_code = code
    problem.contest_number = contest_number
    problem.question_number = question_number
    problem.contest = contest_metadata['contest']['title']
    problem.title = question_metadata['title']
    problem.url = PROBLEM_URL_TEMPLATE % question_metadata['title_slug']
    problem.difficulty = DIFFICULTY[question_number]

    return problem

def get_contest_metadata(log, url):
    response = requests.get(url)
    contest_metadata = json.loads(response.text)

    ERROR_KEY = "error"

    if ERROR_KEY in contest_metadata:
        log.error("Leetcode responded with the following error message.")
        log.error(contest_metadata[ERROR_KEY])
        sys.exit(1)

    return contest_metadata

def get_question_metadata(log, contest_metadata, question_number):
    questions_list = contest_metadata['questions']
    if len(questions_list) < question_number:
        log.error("Question %d was not found. Contest %d only has" \
        " %d questions" % (question_number, contest_number, len(questions_list)))
        sys.exit(1)

    # question numbers are zero indexed
    return questions_list[question_number - 1]

class LeetcodeWeekly(ContestInterface, Handler):

    URL_TEMPLATE = "https://leetcode.com/contest/api/info/weekly-contest-%d"

    class Meta:
        label = LEETCODE_WEEKLY_CODE

    def get_metadata(self, contest_number, question_number):
        log = self.app.log
        log.info("Querying %s for weekly contest metadata..." % PLATFORM_DISPLAY[LEETCODE])
        return query(log, LEETCODE_WEEKLY_CODE, contest_number,
            question_number, LeetcodeWeekly.URL_TEMPLATE)

class LeetcodeBiweekly(ContestInterface, Handler):

    BIWEEKLY_URL_TEMPLATE = "https://leetcode.com/contest/api/info/biweekly-contest-%d"

    class Meta:
        label = LEETCODE_BIWEEKLY_CODE

    def get_metadata(self, contest_number, question_number):
        log = self.app.log
        log.info("Querying %s for biweekly contest metadata..." % PLATFORM_DISPLAY[LEETCODE])
        return query(log, LEETCODE_BIWEEKLY_CODE, contest_number,
            question_number, LeetcodeBiweekly.BIWEEKLY_URL_TEMPLATE)
