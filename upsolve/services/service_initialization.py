from .problems_queue import ProblemsQueue
from .problem_metrics import ProblemMetrics

def service_initialization_hook(app):
    app.log.debug("Initializing the problem stats service")
    metrics_service = ProblemMetrics(app.db)
    app.extend('problem_metrics', metrics_service)
    app.log.debug("Initializing the problems service")
    app.extend('problems_queue', ProblemsQueue(app.db, metrics_service))
