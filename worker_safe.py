#!/usr/bin/env python3
"""
Safe worker script for macOS that avoids forking issues.
This version uses multiprocessing with spawn method.
"""

import os
import sys
import multiprocessing

# Set multiprocessing start method to spawn (safer for macOS)
if sys.platform == 'darwin':  # macOS
    multiprocessing.set_start_method('spawn', force=True)

# Fix for macOS forking issue with Objective-C runtime
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'

from rq import Worker
from app.task_queue import redis_conn

def run_worker():
    """Run the worker in a separate process"""
    worker = Worker(
        ["presentations"],
        connection=redis_conn,
        # job_timeout='15m',
        # result_ttl=86400,
    )
    print(f"Worker {os.getpid()} started...")
    worker.work(with_scheduler=True)

if __name__ == "__main__":
    print("Starting safe presentation worker for macOS...")
    print("Using multiprocessing spawn method")
    print("Press Ctrl+C to stop")
    
    try:
        # Run worker in a separate process
        worker_process = multiprocessing.Process(target=run_worker)
        worker_process.start()
        worker_process.join()
    except KeyboardInterrupt:
        print("\nStopping worker...")
        if 'worker_process' in locals():
            worker_process.terminate()
            worker_process.join()
        print("Worker stopped by user")
        sys.exit(0) 