from ...database.model.problem import Problem
from ...constants import LEETCODE, difficulty_display
from .graphql import GraphQL

ENDPOINT = "https://leetcode.com/graphql"
QUESTION_QUERY = '''
    query getQuestionMetadata($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            title
            titleSlug
            difficulty
            topicTags {
                name
            }
        }
    }
'''

CONTESTS_QUERY = '''
    query getContestQuestions($titleSlug: String!) {
        contest(titleSlug : $titleSlug) {
            title
            questions {
                titleSlug
            }
        }
    }
'''
def query_problem_instances(contest_slug, metadata):
    contest_data = GraphQL.execute(
        ENDPOINT, CONTESTS_QUERY,  {'titleSlug' : contest_slug}
    )
    problem_instances = []
    for i, question in enumerate(contest_data['contest']['questions']):
        slug = question['titleSlug']
        question_data = GraphQL.execute(
            ENDPOINT, QUESTION_QUERY, {'titleSlug' : slug}
        )
        metadata['question_number'] = i + 1
        problem_instances.append(create_problem(contest_data, question_data, metadata))
    return problem_instances


def create_problem(contest_data, question_data, metadata):
    problem = Problem()
    problem.platform = LEETCODE
    problem.contest_number = metadata['contest_number']
    problem.question_number = metadata['question_number']
    problem.code = metadata['code']
    problem.contest_title = contest_data['contest']['title']
    problem.problem_title = question_data['question']['title']
    problem.url = "https://leetcode.com/problems/%s" % question_data['question']['titleSlug']
    problem.difficulty = question_data['question']['difficulty']
    for tag in question_data['question']['topicTags']:
        problem.add_tag(tag['name'])
    return problem

def verify_question_number(problem_instances, question_number, log):
    if len(problem_instances) < question_number:
        log.error("Question %d was not found. Contest only has" \
            " %d questions" % (question_number, len(problem_instances)))
        sys.exit(1)
