from cement import Controller, ex
from ..constants import DIFFICULTIES, difficulty_display
from ..database.model.tag_metrics import TagMetrics

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
        self.app.log.info("Top 10 problem tags")
        tag_metrics = self.app.stats_service.list_top_tags()
        metrics_display = [metric.display_values() for metric in tag_metrics[:10]]
        self.app.render(metrics_display, headers=TagMetrics.headers())
