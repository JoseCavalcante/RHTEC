from workers.celery_app import celery

@celery.task
def background_task(x):
    return x * 2
