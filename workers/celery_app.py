from celery import Celery
from app.core.config import REDIS_URL

celery = Celery("hrtech", broker=REDIS_URL, backend=REDIS_URL)
