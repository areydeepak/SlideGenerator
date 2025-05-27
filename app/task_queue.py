import redis
from rq import Queue
import os
from dotenv import load_dotenv

load_dotenv()

# Redis connection
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_conn = redis.from_url(redis_url)

# Create queue
presentation_queue = Queue("presentations", connection=redis_conn)

def get_queue():
    """Get the presentation queue"""
    return presentation_queue 