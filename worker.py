#!/usr/bin/env python3
"""
Worker script to process background presentation generation jobs.
Run this script to start processing jobs from the Redis queue.
"""

import os
import sys

# Fix for macOS forking issue with Objective-C runtime
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'

from rq import Worker
from app.task_queue import redis_conn

if __name__ == "__main__":
    # Create worker with fork safety disabled for macOS
    worker = Worker(
        ["presentations"], 
        connection=redis_conn,
        # Use spawn instead of fork on macOS to avoid Objective-C issues
        # job_timeout='15m',  # 15 minute timeout for long-running tasks
        # result_ttl=86400,   # Keep results for 24 hours
    )
    
    print("Starting presentation worker...")
    print("Listening for jobs on 'presentations' queue")
    print("Press Ctrl+C to stop")
    
    try:
        worker.work(with_scheduler=True)
    except KeyboardInterrupt:
        print("\nWorker stopped by user")
        sys.exit(0) 