class TagStatsService:

    def __init__(self, tag_stats_table):
        self.tag_stats_table = tag_stats_table

    def update_tag_counts(self, *problems):
        self.tag_stats_table.update_tag_counts(*problems)
