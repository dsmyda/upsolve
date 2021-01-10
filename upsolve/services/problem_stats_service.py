from tinydb import where, Query
from ..database.model.problem_stats import ProblemStats, columns
from ..constants import DIFFICULTIES
from collections import Counter

class ProblemStatsService:

    def __init__(self, tinydb):
        self.table = tinydb.table("stats")

    def update(self, problem, duration):
        for tag in problem.tags:
            self._add_time(problem.difficulty, tag, duration)

    def list_by_difficulty(self, difficulty):
        results = self.table.search(
            where(columns.difficulty) == difficulty
        )
        return [ProblemStats(result) for result in results]

    def list_top_tags(self):
        tags = Counter()
        for difficulty in DIFFICULTIES:
            results = self.table.search(
                where(columns.difficulty) == difficulty
            )
            for stats in results:
                instance = ProblemStats(stats)
                tags[instance.tag] += instance.count
        return tags.most_common()

    def update_counts(self, *problems):
        for problem in problems:
            for tag in problem.tags:
                self._update_count(problem.difficulty, tag)

    def _add_time(self, difficulty, tag, time):
        problem_stat = self.table.search(
            (where(columns.difficulty) == difficulty) &
            (where(columns.tag) == tag)
        )

        assert problem_stat
        problem_stat = ProblemStats(problem_stat[0])
        problem_stat.times.append(time)
        self.table.update(problem_stat, where(columns.uuid) == problem_stat.uuid)

    def _update_count(self, difficulty, tag):
        problem_stat = self.table.search(
            (where(columns.difficulty) == difficulty) &
            (where(columns.tag) == tag)
        )

        if not problem_stat:
            problem_stat = ProblemStats()
            problem_stat.difficulty = difficulty
            problem_stat.tag = tag
        else:
            problem_stat = ProblemStats(problem_stat[0])

        problem_stat.increment_count()
        self.table.upsert(problem_stat, where(columns.uuid) == problem_stat.uuid)
