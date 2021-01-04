from tinydb import where, Query
from .problem_metadata import ProblemMetadata

class ProblemsTable:

    def __init__(self, tinydb):
        self._table_name = "problems"
        self.table = tinydb.table(self._table_name)

    def add(self, *args):
        return self.table.insert_multiple(args)

    def all(self):
        metadata_instances = []
        for raw_json in self.table.all():
            metadata_instances.append(ProblemMetadata(raw_json))
        return metadata_instances

    def exists(self, contest_number, question_number):
        return self.table.contains(
            (where('contest_number') == contest_number) &
            (where('question_number') == question_number)
        )

    def delete_all(self):
        self.table.truncate()

    def pop(self):
        if self.size():
            problem = next(iter(self.table))
            self.table.remove(where('uuid') == problem['uuid'])
            return ProblemMetadata(problem)

    def size(self):
        return len(self.table)
