from cement import Controller, ex
from ..database.problem_metadata import ProblemMetadata

class View(Controller):

    class Meta:
        label = 'view'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='view questions'
    )
    def view(self):
        headers = ProblemMetadata.headers()
        problems = self.app.problems_table.all()
        values = []
        for problem in problems:
            values.append(problem.values())
        self.app.render(values, headers=headers)
