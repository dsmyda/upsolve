from cement import Controller, ex
from ..database.problem import Problem

class List(Controller):

    class Meta:
        label = 'list'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='List all problems in the queue'
    )
    def list(self):
        headers = Problem.headers()
        problems = self.app.problems_table.all()
        values = [problem.values() for problem in problems]
        self.app.render(values, headers=headers)
