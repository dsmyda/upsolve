class ProblemsService:

    def __init__(self, problems_table, tag_stats_service):
        self.problems_table = problems_table
        self.tag_stats_service = tag_stats_service

    def save(self, *problems):
        self.problems_table.add(*problems)
        self.tag_stats_service.update_tag_counts(*problems)

    def get_next(self):
        return self.problems_table.pop()

    def delete_all(self):
        self.problems_table.drop()

    def get_all(self):
        return self.problems_table.all()

    def size(self):
        return self.problems_table.size()
