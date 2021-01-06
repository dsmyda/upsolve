from .platform_api import PlatformAPI
from ..constants import BINARYSEARCH, EASY, MEDIUM, HARD, HARDER
import requests, json, sys
from cement import Handler
from ..database.problem_metadata import ProblemMetadata

ALL_CONTESTS_URL = "https://api.binarysearch.io/contests"

# Channel slug then room slug
CONTEST_URL_TEMPLATE = "https://api.binarysearch.io/rooms/%s?slug=%s"
PROBLEM_URL_TEMPLATE = "https://binarysearch.com/problems/%s"

# Keys are integer values taken from the question metadata
# returned from the API.
DIFFICULTY = {
    0: EASY,
    1: MEDIUM,
    2: HARD,
    3: HARDER
}

NAME = BINARYSEARCH

class BinarySearch(PlatformAPI, Handler):

    class Meta:
        label = NAME

    def get_metadata(self, contest_number, question_number):
        self.app.log.info("Querying binarysearch for metadata...")
        all_contests = requests.get(ALL_CONTESTS_URL)
        contests = json.loads(all_contests.text)
        contests = contests["contests"]

        # JSON document is zero indexed
        contest_number -= 1
        question_number -= 1

        if len(contests) <= contest_number:
            self.app.log.error("Contest %d was not found. There has only been" \
            " %d contests" % (contest_number + 1, len(contests)))
            sys.exit(1)

        selected_contest = contests[contest_number]
        channel_slug = selected_contest["channelSlug"]
        room_slug = selected_contest["slug"]

        contest_metadata = requests.get(CONTEST_URL_TEMPLATE % (channel_slug, room_slug))
        contest_metadata = json.loads(contest_metadata.text)
        question_set = contest_metadata['sessions'][0]['questionsets']

        if len(question_set) <= question_number:
            self.app.log.error("Question %d was not found. Contest %d only has" \
            " %d questions" % (question_number + 1, contest_number + 1, len(question_set)))
            sys.exit(1)

        question_metadata = question_set[question_number]['question']

        metadata = ProblemMetadata()
        metadata.platform = NAME
        metadata.contest_number = contest_number + 1
        metadata.question_number = question_number + 1
        metadata.contest = contest_metadata['name']
        metadata.title = question_metadata['title']
        metadata.url = PROBLEM_URL_TEMPLATE % question_metadata['slug']
        metadata.difficulty = DIFFICULTY[question_metadata['difficulty']]

        return metadata
