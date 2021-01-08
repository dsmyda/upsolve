from .contest_interface import ContestInterface
from ..constants import GREEN, PLATFORM_DISPLAY, BINARYSEARCH, BINARYSEARCH_WEEKLY_CODE, BINARYSEARCH_EDUCATIONAL_CODE, EASY, MEDIUM, HARD, HARDER
import requests, json, sys
from cement import Handler
from ..database.model.problem import Problem

ALL_CONTESTS_URL = "https://api.binarysearch.io/contests"

# Channel slug then room slug
CONTEST_LOBBY_URL_TEMPLATE = "https://api.binarysearch.io/rooms/%s?slug=%s"
PROBLEM_URL_TEMPLATE = "https://binarysearch.com/problems/%s"

# Keys are integer values taken from the question metadata
# returned from the API.
DIFFICULTY = {
    0: EASY,
    1: MEDIUM,
    2: HARD,
    3: HARDER
}

def query(log, code, type, contest_number, question_number):
    contest_metadata = get_contest_metadata(log, type, contest_number)
    question_metadata = get_question_metadata(log, contest_metadata, contest_number, question_number)

    problem = Problem()
    problem.platform = BINARYSEARCH
    problem.contest_code = code
    problem.contest_number = contest_number
    problem.question_number = question_number
    problem.contest_title = contest_metadata['name']
    problem.problem_title = question_metadata['title']
    problem.url = PROBLEM_URL_TEMPLATE % question_metadata['slug']
    problem.difficulty = DIFFICULTY[question_metadata['difficulty']]

    return problem

def get_contest_metadata(log, type, contest_number):
    all_contests = requests.get(ALL_CONTESTS_URL)
    all_contests = json.loads(all_contests.text)
    contests_of_type = all_contests[type]

    if len(contests_of_type) < contest_number:
        log.error("Contest %d was not found. There have only been" \
        " %d contests" % (contest_number, len(contests_of_type)))
        sys.exit(1)

    # Contests in the JSON are zero-indexed
    return contests_of_type[contest_number - 1]

def get_question_metadata(log, contest, contest_number, question_number):
    channel_slug = contest["channelSlug"]
    room_slug = contest["slug"]

    contest_lobby = requests.get(CONTEST_LOBBY_URL_TEMPLATE % (channel_slug, room_slug))
    contest_lobby = json.loads(contest_lobby.text)
    questions = contest_lobby['sessions'][0]['questionsets']

    if len(questions) < question_number:
        log.error("Question %d was not found. Contest %d only has" \
        " %d questions" % (question_number, contest_number, len(questions)))
        sys.exit(1)

    # Questions in the JSON are zero-indexed
    return questions[question_number - 1]['question']

class BinarysearchWeekly(ContestInterface, Handler):

    JSON_KEY = "contests"

    class Meta:
        label = BINARYSEARCH_WEEKLY_CODE

    def get_metadata(self, contest_number, question_number):
        log = self.app.log
        log.info("Querying %s for weekly question metadata..." % (PLATFORM_DISPLAY[BINARYSEARCH] + GREEN))
        return query(log, BINARYSEARCH_WEEKLY_CODE,
            BinarysearchWeekly.JSON_KEY, contest_number, question_number)

    def get_all_questions_metadata(self, contest_number):
        log = self.app.log
        log.info("Querying %s for all weekly question metadata..." % (PLATFORM_DISPLAY[BINARYSEARCH] + GREEN))

class BinarysearchEdu(ContestInterface, Handler):

    JSON_KEY = "eduContests"

    class Meta:
        label = BINARYSEARCH_EDUCATIONAL_CODE

    def get_metadata(self, contest_number, question_number):
        log = self.app.log
        log.info("Querying %s for educational question metadata..." % (PLATFORM_DISPLAY[BINARYSEARCH] + GREEN))
        return query(log, BINARYSEARCH_EDUCATIONAL_CODE,
            BinarysearchEdu.JSON_KEY, contest_number, question_number)

    def get_all_questions_metadata(self, contest_number):
        log = self.app.log
        log.info("Querying %s for all educational question metadata..." % (PLATFORM_DISPLAY[BINARYSEARCH] + GREEN))
