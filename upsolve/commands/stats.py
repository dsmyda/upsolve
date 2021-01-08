from cement import Controller, ex
from ..constants import DIFFICULTIES, DIFFICULTY_DISPLAY
from ..database.problem_stats import ProblemStats

class Stats(Controller):

    class Meta:
        label = 'stats'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='List personalized stats on performance'
    )
    def stats(self):
        print()
        self.app.log.info("Top 5 most failed problem tags")
        headers = ['tag', '# of problems']
        self.app.render([], headers=headers)

        self.app.log.info("Timing stats by tag and difficulty")
        print()
        headers = ProblemStats.headers()
        for difficulty in reversed(DIFFICULTIES):
            print(DIFFICULTY_DISPLAY[difficulty])
            difficulty_stats = self.app.stats_table.all(difficulty)
            self.app.render(difficulty_stats, headers=headers)
