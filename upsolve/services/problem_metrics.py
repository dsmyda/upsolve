from tinydb import where, Query
from ..database.model.tag_metrics import TagMetrics, columns
from collections import Counter

class ProblemMetrics:

    def __init__(self, tinydb):
        self.tags_table = tinydb.table("tag_metrics")

    def list_top_tags(self):
        results = self.tags_table.all()
        metrics = [TagMetrics(stat) for stat in results]
        metrics.sort(key = lambda tag : tag.count, reverse = True)
        return metrics

    def notify(self, *problems):
        for problem in problems:
            for tag in problem.tags:
                self._increment_tag_count(tag)

    def _increment_tag_count(self, tag):
        tag_metrics = self.tags_table.search(
            where(columns.tag) == tag
        )

        if not tag_metrics:
            tag_metrics = TagMetrics()
            tag_metrics.tag = tag
        else:
            tag_metrics = TagMetrics(tag_metrics[0])

        tag_metrics.increment_count()
        self.tags_table.upsert(tag_metrics, where(columns.uuid) == tag_metrics.uuid)
