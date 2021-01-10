from .problems_service import ProblemsService
from .problem_stats_service import ProblemStatsService

def service_initialization_hook(app):
    app.log.debug("Initializing the problem stats service")
    stats_service = ProblemStatsService(app.db)
    app.extend('stats_service', stats_service)
    app.log.debug("Initializing the problems service")
    app.extend('problems_service', ProblemsService(app.db, stats_service))
