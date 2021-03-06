from ...constants import DIFFICULTY_DISPLAY, PLATFORM_DISPLAY, contest_display, platform_display, difficulty_display
from collections.abc import Mapping
from ...namespace import Namespace
import uuid

# column keys
columns = Namespace(
    uuid =           "uuid",
    contest_title =  "contest_title",
    platform =       "platform",
    problem_title =  "problem_title",
    url =            "url",
    difficulty =     "difficulty",
    contest_number = "contest_number",
    problem_number = "problem_number",
    contest_code =   "contest_code",
    tags =           "tags"
)

class Problem(Mapping):
    ''' Represents a problem metadata document in the database '''

    def __init__(self, info=None):
        if info is None:
            info = dict()
        self._info = info
        if columns.uuid not in self._info:
            self._info[columns.uuid] = str(uuid.uuid1())
        if columns.tags not in self._info:
            self._info[columns.tags] = []

    def display_values(self):
        ''' Table values for display '''

        return [
            platform_display(self.platform),
            contest_display(self.contest_title),
            self.problem_title,
            difficulty_display(self.difficulty)
        ]

    @staticmethod
    def display_headers():
        ''' Table headers for display '''

        return [columns.platform, columns.contest_title, columns.problem_title, columns.difficulty]

    @property
    def tags(self):
        return self._info[columns.tags]

    def add_tag(self, tag):
        normalized_tag = tag.lower().strip()
        self._info[columns.tags].append(normalized_tag)

    @property
    def contest_code(self):
        return self._info[columns.contest_code]

    @contest_code.setter
    def contest_code(self, code):
        self._info[columns.contest_code] = code

    @property
    def contest_number(self):
        return self._info[columns.contest_number]

    @contest_number.setter
    def contest_number(self, number):
        self._info[columns.contest_number] = number

    @property
    def question_number(self):
        return self._info[columns.problem_number]

    @question_number.setter
    def question_number(self, number):
        self._info[columns.problem_number] = number

    @property
    def contest_title(self):
        return self._info[columns.contest_title]

    @contest_title.setter
    def contest_title(self, contest_title):
        self._info[columns.contest_title] = contest_title

    @property
    def platform(self):
        return self._info[columns.platform]

    @platform.setter
    def platform(self, platform):
        self._info[columns.platform] = platform

    @property
    def problem_title(self):
        return self._info[columns.problem_title]

    @problem_title.setter
    def problem_title(self, problem_title):
        self._info[columns.problem_title] = problem_title

    @property
    def url(self):
        return self._info[columns.url]

    @url.setter
    def url(self, url):
        self._info[columns.url] = url

    @property
    def difficulty(self):
        return self._info[columns.difficulty]

    @difficulty.setter
    def difficulty(self, difficulty):
        self._info[columns.difficulty] = difficulty

    def __getitem__(self, key):
        return self._info[key]

    def __iter__(self):
        return iter(self._info)

    def __len__(self):
        return len(self._info)

    def __str__(self):
        return str(self._info)
