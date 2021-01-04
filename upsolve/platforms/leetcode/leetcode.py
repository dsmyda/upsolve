from ..platform_api_handler import PlatformAPIHandler
from ...database.problem_metadata import ProblemMetadata
import requests, json, sys

CONTEST_URL_TEMPLATE = "https://leetcode.com/contest/api/info/weekly-contest-%d"
PROBLEM_URL_TEMPLATE = "https://leetcode.com/problems/%s/"
DIFFICULTY = {
    0: "Easy",
    1: "Medium",
    2: "Medium",
    3: "Hard"
}
NAME = "leetcode"

class LeetCode(PlatformAPIHandler):

    class Meta:
        label = NAME

    def _fetch_metadata(self, contest_number, question_number):
        self.app.log.info("Querying leetcode for metadata...")
        response = requests.get(CONTEST_URL_TEMPLATE % contest_number)
        contest_metadata = json.loads(response.text)
        questions_list = contest_metadata['questions']

        if len(questions_list) <= question_number:
            self.app.log.fatal("Question %d was not found. Contest %d only has %d questions" % (question_number + 1, contest_number, len(questions_metadata)))
            sys.exit(1)
        question = questions_list[question_number]

        metadata = ProblemMetadata()
        metadata.platform = NAME
        metadata.contest_number = contest_number
        metadata.question_number = question_number
        metadata.contest = contest_metadata['contest']['title']
        metadata.title = question['title']
        metadata.url = PROBLEM_URL_TEMPLATE % question['title_slug']
        metadata.difficulty = DIFFICULTY[question_number]

        return metadata
