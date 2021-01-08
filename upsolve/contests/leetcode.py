from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from .contest_interface import ContestInterface
from cement import Handler
from ..database.model.problem import Problem
import requests, json, sys
from ..constants import GREEN, PLATFORM_DISPLAY, LEETCODE, LEETCODE_WEEKLY_CODE, LEETCODE_BIWEEKLY_CODE, EASY, MEDIUM, HARD

# Indexed by question in the contest, the keys
# are not integer values taken from question metadata
DIFFICULTY = {
    1: EASY,
    2: MEDIUM,
    3: MEDIUM,
    4: HARD
}

PROBLEM_URL_TEMPLATE = "https://leetcode.com/problems/%s/"

def add_tags(problem, title_slug):
    transport = RequestsHTTPTransport(
        url="https://leetcode.com/graphql", verify=True, retries=3,
    )

    client = Client(transport=transport)
    query = gql(
        '''
        query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                topicTags {
                    name
                }
            }
        }
        '''
    )
    params = {'titleSlug': title_slug}
    result = client.execute(query, variable_values=params)
    for tag in result['question']['topicTags']:
        problem.add_tag(tag['name'])

def create_problem_instance(code, contest_number, question_number, contest_metadata, question_metadata):
    problem = Problem()
    problem.platform = LEETCODE
    problem.contest_code = code
    problem.contest_number = contest_number
    problem.question_number = question_number
    problem.contest_title = contest_metadata['contest']['title']
    problem.problem_title = question_metadata['title']
    problem.url = PROBLEM_URL_TEMPLATE % question_metadata['title_slug']
    problem.difficulty = DIFFICULTY[question_number]

    add_tags(problem, question_metadata['title_slug'])
    return problem

def query_all_questions(log, code, contest_number, template):
    contest_metadata = get_contest_metadata(log, template % contest_number)
    questions_list = contest_metadata['questions']

    ans = []
    for i, question_metadata in enumerate(questions_list):
        ans.append(create_problem_instance(code, contest_number, i + 1,
            contest_metadata, question_metadata))
        print([p.problem_title for p in ans])
    return ans

def query_question(log, code, contest_number, question_number, template):
    contest_metadata = get_contest_metadata(log, template % contest_number)
    question_metadata = get_question_metadata(log, contest_metadata, question_number)
    return create_problem_instance(code, contest_number, question_number,
        contest_metadata, question_metadata)

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
        log.info("Querying %s for weekly question metadata..." % (PLATFORM_DISPLAY[LEETCODE] + GREEN))
        return query_question(log, LEETCODE_WEEKLY_CODE, contest_number,
            question_number, LeetcodeWeekly.URL_TEMPLATE)

    def get_all_questions_metadata(self, contest_number):
        log = self.app.log
        log.info("Querying %s for all weekly question metadata..." % (PLATFORM_DISPLAY[LEETCODE] + GREEN))
        return query_all_questions(log, LEETCODE_WEEKLY_CODE, contest_number,
            LeetcodeWeekly.URL_TEMPLATE)

class LeetcodeBiweekly(ContestInterface, Handler):

    BIWEEKLY_URL_TEMPLATE = "https://leetcode.com/contest/api/info/biweekly-contest-%d"

    class Meta:
        label = LEETCODE_BIWEEKLY_CODE

    def get_metadata(self, contest_number, question_number):
        log = self.app.log
        log.info("Querying %s for biweekly question metadata..." % (PLATFORM_DISPLAY[LEETCODE] + GREEN))
        return query_question(log, LEETCODE_BIWEEKLY_CODE, contest_number,
            question_number, LeetcodeBiweekly.BIWEEKLY_URL_TEMPLATE)

    def get_all_questions_metadata(self, contest_number):
        log = self.app.log
        log.info("Querying %s for all biweekly question metadata..." % (PLATFORM_DISPLAY[LEETCODE] + GREEN))
        return query_all_questions(log, LEETCODE_BIWEEKLY_CODE, contest_number,
            LeetcodeBiweekly.BIWEEKLY_URL_TEMPLATE)
