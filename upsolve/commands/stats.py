from cement import Controller, ex
from ..constants import DIFFICULTIES, difficulty_display
from ..database.model.problem_stats import ProblemStats

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
        self.app.log.info("Top 5 problem tags")
        headers = ['Tag', 'Count']
        self.app.render(self.app.stats_service.list_top_tags()[:5], headers=headers)

        self.app.log.info("Breakdown by difficulty and tag, timing stats included")
        print()
        headers = ProblemStats.display_headers()
        for difficulty in reversed(DIFFICULTIES):
            stats_by_difficulty = self.app.stats_service.list_by_difficulty(difficulty)
            print(difficulty_display(difficulty))
            self.app.render([stat.display_values() for stat in stats_by_difficulty], headers=headers)
