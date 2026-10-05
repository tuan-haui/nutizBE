import os
import redis
from rq import Worker, Queue, Connection
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

redis_conn = redis.from_url(settings.REDIS_URL)

def run_worker():
    logger.info("Starting media worker...")
    with Connection(redis_conn):
        worker = Worker(map(Queue, ['default']))
        worker.work()

if __name__ == '__main__':
    run_worker()
