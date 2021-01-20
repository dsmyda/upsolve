from .problems_queue import ProblemsQueue
from .problem_metrics import ProblemMetrics

def service_initialization_hook(app):
    app.log.debug("Initializing the problem stats service")
    stats_service = ProblemMetrics(app.db)
    app.extend('stats_service', stats_service)
    app.log.debug("Initializing the problems service")
    app.extend('problems_service', ProblemsQueue(app.db, stats_service))
