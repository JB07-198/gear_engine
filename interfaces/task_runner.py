"""Task runner that prefers Celery+Redis if available, otherwise falls back to threaded execution."""
import os
import threading
from typing import Callable, Any

USE_CELERY = False
celery_app = None

REDIS_URL = os.environ.get('REDIS_URL') or os.environ.get('CELERY_BROKER_URL')

try:
    if REDIS_URL:
        from celery import Celery

        celery_app = Celery('gear_engine', broker=REDIS_URL)
        USE_CELERY = True
except Exception:
    USE_CELERY = False


def submit_task(fn: Callable, *args, **kwargs):
    """Submit a task. If Celery is available, use it; otherwise run in background thread."""
    if USE_CELERY and celery_app is not None:
        # wrap function as a celery task dynamically
        task = celery_app.task(fn)
        return task.delay(*args, **kwargs)
    else:
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
