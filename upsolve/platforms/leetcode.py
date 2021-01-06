from .platform_api import PlatformAPI
from cement import Handler
from ..database.problem_metadata import ProblemMetadata
import requests, json, sys
from ..constants import LEETCODE, EASY, MEDIUM, HARD

CONTEST_URL_TEMPLATE = "https://leetcode.com/contest/api/info/weekly-contest-%d"
PROBLEM_URL_TEMPLATE = "https://leetcode.com/problems/%s/"

# Indexed by question in the contest, the keys
# are not integer values taken from question metadata
DIFFICULTY = {
    0: EASY,
    1: MEDIUM,
    2: MEDIUM,
    3: HARD
}

NAME = LEETCODE
ERROR_KEY = "error"

class LeetCode(PlatformAPI, Handler):

    class Meta:
        label = NAME

    def validate_response(self, contest_metadata):
        if ERROR_KEY in contest_metadata:
            self.app.log.error("Leetcode responded with the following error message.")
            self.app.log.error(contest_metadata[ERROR_KEY])
            sys.exit(1)

    def get_metadata(self, contest_number, question_number):
        self.app.log.info("Querying leetcode for metadata...")

        response = requests.get(CONTEST_URL_TEMPLATE % contest_number)
        contest_metadata = json.loads(response.text)
        self.validate_response(contest_metadata)

        # question numbers are zero indexed
        question_number -= 1

        questions_list = contest_metadata['questions']
        if len(questions_list) <= question_number:
            self.app.log.error("Question %d was not found. Contest %d only has" \
            " %d questions" % (question_number + 1, contest_number, len(questions_list)))
            sys.exit(1)

        question = questions_list[question_number]

        metadata = ProblemMetadata()
        metadata.platform = NAME
        metadata.contest_number = contest_number
        metadata.question_number = question_number + 1
        metadata.contest = contest_metadata['contest']['title']
        metadata.title = question['title']
        metadata.url = PROBLEM_URL_TEMPLATE % question['title_slug']
        metadata.difficulty = DIFFICULTY[question_number]

        return metadata
