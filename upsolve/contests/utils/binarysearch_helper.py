from ...constants import BINARYSEARCH, EASY, MEDIUM, HARD, HARDER
import requests, json, sys
from ...database.model.problem import Problem

ALL_CONTESTS = "https://api.binarysearch.io/contests"
# Channel slug then room slug
CONTEST_LOBBY = "https://api.binarysearch.io/rooms/%s?slug=%s"

# Keys are integer values taken from the question metadata
# returned from the API.
DIFFICULTY = {
    0: EASY,
    1: MEDIUM,
    2: HARD,
    3: HARDER
}

def create_problem(contest_metadata, question_metadata, metadata):
    problem = Problem()
    problem.platform = BINARYSEARCH
    problem.contest_code = metadata['code']
    problem.contest_number = metadata['contest_number']
    problem.question_number = metadata['question_number']
    problem.contest_title = contest_metadata['name']
    problem.problem_title = question_metadata['title']
    problem.url = "https://binarysearch.com/problems/%s" % question_metadata['slug']
    problem.difficulty = DIFFICULTY[question_metadata['difficulty']]

    for topic in question_metadata['topics']:
        problem.add_tag(topic['tag'])
    return problem

def query_problem_instances(contest_number, metadata, log):
    contest_metadata = get_contest_metadata(contest_number, metadata, log)
    contest_questions = get_contest_questions(contest_metadata)

    instances = []
    for i, question in enumerate(contest_questions):
        question_metadata = question['question']
        metadata['question_number'] = i + 1
        instances.append(create_problem(contest_metadata, question_metadata, metadata))

    return instances

def get_contest_metadata(contest_number, metadata, log):
    all_contests = requests.get(ALL_CONTESTS)
    all_contests = json.loads(all_contests.text)
    contests_of_type = all_contests[metadata['type']]

    if len(contests_of_type) < contest_number:
        log.error("Contest %d was not found. There have only been" \
        " %d contests" % (contest_number, len(contests_of_type)))
        sys.exit(1)

    # Contests in the JSON are zero-indexed
    return contests_of_type[contest_number - 1]

def get_contest_questions(contest):
    channel_slug = contest["channelSlug"]
    room_slug = contest["slug"]

    contest_lobby = requests.get(CONTEST_LOBBY % (channel_slug, room_slug))
    contest_lobby = json.loads(contest_lobby.text)
    questions = contest_lobby['sessions'][0]['questionsets']
    return questions

def verify_question_number(problem_instances, question_number, log):
    if len(problem_instances) < question_number:
        log.error("Question %d was not found. Contest only has" \
            " %d questions" % (question_number, len(problem_instances)))
        sys.exit(1)
