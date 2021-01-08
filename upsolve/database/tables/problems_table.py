from tinydb import where, Query
from ...constants import DIFFICULTY_DISPLAY, PLATFORM_DISPLAY
from collections.abc import Mapping
import uuid

TABLE_NAME = "problems"

# columns
UUID = "uuid"
CONTEST = "contest"
PLATFORM = "platform"
TITLE = "title"
URL = "url"
DIFFICULTY = "difficulty"
CONTEST_NUMBER = "contest_number"
PROBLEM_NUMBER = "problem_number"
CONTEST_CODE = "contest_code"

class ProblemsTable:

    def __init__(self, tinydb):
        self.table = tinydb.table(TABLE_NAME)

    def add(self, *args):
        ''' Add problems to the table '''

        return self.table.insert_multiple(args)

    def all(self):
        ''' Return all problems in the table '''

        metadata_instances = []
        for raw_json in self.table.all():
            metadata_instances.append(Problem(raw_json))
        return metadata_instances

    def exists(self, contest_code, contest_number, question_number):
        ''' Query if the problem with primary key
            (contest_code, contest_number, question_number) is already present '''

        return self.table.contains(
            (where(CONTEST_CODE) == contest_code) &
            (where(CONTEST_NUMBER) == contest_number) &
            (where(PROBLEM_NUMBER) == question_number)
        )

    def drop(self):
        ''' Drop all problems in the table '''

        self.table.truncate()

    def pop(self):
        ''' Pop off the first problem in the table '''

        if self.size():
            problem = next(iter(self.table))
            self.table.remove(where(UUID) == problem[UUID])
            return Problem(problem)

    def size(self):
        ''' Return the number of problems in the table '''

        return len(self.table)

class Problem(Mapping):
    ''' Represents a problem metadata document in the database '''

    def __init__(self, info=dict()):
        self._info = info
        if UUID not in self._info:
            self._info[UUID] = str(uuid.uuid1())

    def values(self):
        ''' Table values for display '''

        return [
            PLATFORM_DISPLAY[self.platform],
            self.contest,
            self.title,
            DIFFICULTY_DISPLAY[self.difficulty]
        ]

    @staticmethod
    def headers():
        ''' Table headers for display '''

        return [PLATFORM, CONTEST, TITLE, DIFFICULTY]

    def __getitem__(self, key):
        return self._info[key]

    def __iter__(self):
        return iter(self._info)

    def __len__(self):
        return len(self._info)

    def __str__(self):
        return str(self._info)

    @property
    def contest_code(self):
        return self._info[CONTEST_CODE]

    @contest_code.setter
    def contest_code(self, code):
        self._info[CONTEST_CODE] = code

    @property
    def contest_number(self):
        return self._info[CONTEST_NUMBER]

    @contest_number.setter
    def contest_number(self, number):
        self._info[CONTEST_NUMBER] = number

    @property
    def question_number(self):
        return self._info[PROBLEM_NUMBER]

    @question_number.setter
    def question_number(self, number):
        self._info[PROBLEM_NUMBER] = number

    @property
    def contest(self):
        return self._info[CONTEST]

    @contest.setter
    def contest(self, contest):
        self._info[CONTEST] = contest

    @property
    def platform(self):
        return self._info[PLATFORM]

    @platform.setter
    def platform(self, platform):
        self._info[PLATFORM] = platform

    @property
    def title(self):
        return self._info[TITLE]

    @title.setter
    def title(self, title):
        self._info[TITLE] = title

    @property
    def url(self):
        return self._info[URL]

    @url.setter
    def url(self, url):
        self._info[URL] = url

    @property
    def difficulty(self):
        return self._info[DIFFICULTY]

    @difficulty.setter
    def difficulty(self, difficulty):
        self._info[DIFFICULTY] = difficulty
