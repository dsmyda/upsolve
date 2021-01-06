from collections.abc import Mapping
from ..constants import DIFFICULTY_DISPLAY, PLATFORM_DISPLAY
from .constants import UUID, CONTEST, PLATFORM, TITLE, URL, \
DIFFICULTY, CONTEST_NUMBER, PROBLEM_NUMBER
import uuid

class ProblemMetadata(Mapping):
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
