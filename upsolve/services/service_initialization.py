from .problems_service import ProblemsService
from .tag_stats_service import TagStatsService
from ..database.tables.problems_table import ProblemsTable
from ..database.tables.tag_stats_table import TagStatsTable

def service_initialization_hook(app):
    app.log.debug("Initializing the tags stats service")
    tag_stats_service = TagStatsService(TagStatsTable(app.db))
    app.extend('tags_stats_service', tag_stats_service)
    app.log.debug("Initializing the problems service")
    app.extend('problems_service', ProblemsService(ProblemsTable(app.db), tag_stats_service))
