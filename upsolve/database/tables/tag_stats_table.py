from tinydb import where, Query

TABLE_NAME = "tag_stats"

class TagStatsTable:

    def __init__(self, tinydb):
        self.table = tinydb.table(TABLE_NAME)

    def record_time(self, problem, duration):
        # Use problem tag, difficulty to index duration
        pass

    def all(self, difficulty):
        return []

    def update_tag_counts(self, *problems):
        pass
