from tinydb import where, Query
from ..model.tag_stats import columns, TagStats

TABLE_NAME = "tag_stats"

class TagStatsTable:

    def __init__(self, tinydb):
        self.table = tinydb.table(TABLE_NAME)

    def record_time(self, problem, duration):
        for tag in problem.tags:
            self._add_time(problem.difficulty, tag, duration)

    def find_all(self, difficulty):
        results = self.table.search(
            where(columns.difficulty) == difficulty
        )
        return [TagStats(result) for result in results]

    def get_all(self):
        return self.table.all()

    def update_tag_counts(self, *problems):
        pass

    def _add_time(self, difficulty, tag, time):
        pass
