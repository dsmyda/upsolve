from cement import Controller, ex
from ..database.problem_metadata import ProblemMetadata

class List(Controller):

    class Meta:
        label = 'list'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='List all problems in the queue'
    )
    def list(self):
        headers = ProblemMetadata.headers()
        problems = self.app.problems_table.all()
        values = [problem.values() for problem in problems]
        self.app.render(values, headers=headers)
