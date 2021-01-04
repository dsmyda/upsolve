from collections.abc import Mapping
import uuid

WHITE   = '\033[0m'  # white
RED     = '\033[31m' # red
GREEN   = '\033[32m' # green
ORANGE  = '\033[33m' # orange
BLUE    = '\033[34m' # blue
PURPLE  = '\033[35m' # purple

DIFFICULTY = {
    "Easy" : GREEN + "Easy" + WHITE,
    "Medium" : ORANGE + "Medium" + WHITE,
    "Hard" : RED + "Hard" + WHITE
}

PLATFORM = {
    "leetcode" : GREEN + "leetcode" + WHITE,
    "binarysearch": BLUE + "binarysearch" + WHITE
}

class ProblemMetadata(Mapping):
    ''' Represents a metadata document in the database '''

    def __init__(self, info=dict()):
        self._info = info
        if 'uuid' not in self._info:
            self._info['uuid'] = str(uuid.uuid1())

    def values(self):
        return [
            PLATFORM[self.platform],
            self.contest,
            self.title,
            DIFFICULTY[self.difficulty]
        ]

    @staticmethod
    def headers():
        return ['platform', 'contest', 'title', 'difficulty']

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
        return self._info['contest_number']

    @contest_number.setter
    def contest_number(self, number):
        self._info['contest_number'] = number

    @property
    def question_number(self):
        return self._info['question_number']

    @question_number.setter
    def question_number(self, number):
        self._info['question_number'] = number

    @property
    def contest(self):
        return self._info['contest']

    @contest.setter
    def contest(self, contest):
        self._info['contest'] = contest

    @property
    def platform(self):
        return self._info['platform']

    @platform.setter
    def platform(self, platform):
        self._info['platform'] = platform

    @property
    def title(self):
        return self._info['title']

    @title.setter
    def title(self, title):
        self._info['title'] = title

    @property
    def url(self):
        return self._info['url']

    @url.setter
    def url(self, url):
        self._info['url'] = url

    @property
    def difficulty(self):
        return self._info['difficulty']

    @difficulty.setter
    def difficulty(self, difficulty):
        self._info['difficulty'] = difficulty
