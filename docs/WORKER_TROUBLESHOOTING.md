# Worker Troubleshooting Guide

This guide helps resolve common issues with the presentation generation worker, especially on macOS.

## Common Issues

### 1. macOS Forking Error (objc_initializeAfterForkError)

**Error Message:**
```
objc[PID]: +[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called.
objc[PID]: +[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called. We cannot safely call it or ignore it in the fork() child process. Crashing instead.
```

**Cause:** This happens on macOS when libraries that use Objective-C frameworks (like `python-pptx`) are used in forked processes.

**Solutions:**

#### Option 1: Use the Safe Worker (Recommended)
```bash
python start_worker.py safe
```
or
```bash
python worker_safe.py
```

#### Option 2: Set Environment Variable
```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
python worker.py
```

#### Option 3: Use the Smart Startup Script
```bash
python start_worker.py
```
This automatically detects macOS and uses the appropriate worker.

### 2. Timeout Parameter Error

**Error Message:**
```
TypeError: generate_presentation_task() got an unexpected keyword argument 'timeout'
```

**Solution:** The timeout parameter should be set in the worker configuration, not passed to the task function. This has been fixed in the updated code.

### 3. Redis Connection Issues

**Error Message:**
```
redis.exceptions.ConnectionError: Error connecting to Redis
```

**Solutions:**

#### Install and Start Redis
**macOS:**
```bash
brew install redis
brew services start redis
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

**Check Redis Status:**
```bash
redis-cli ping
# Should return: PONG
```

### 4. Module Import Errors

**Error Message:**
```
ModuleNotFoundError: No module named 'app'
```

**Solutions:**

#### Set PYTHONPATH
```bash
export PYTHONPATH=/path/to/SlideGenerator:$PYTHONPATH
python worker.py
```

#### Run from Project Root
Make sure you're running the worker from the project root directory:
```bash
cd /path/to/SlideGenerator
python worker.py
```

### 5. Database Connection Issues

**Error Message:**
```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: presentations
```

**Solution:** Run database migrations:
```bash
# If using Alembic
alembic upgrade head

# Or create tables directly
python -c "from app.database import create_tables; create_tables()"
```

## Worker Options

### Standard Worker (`worker.py`)
- Uses RQ's default forking mechanism
- Works well on Linux and Windows
- May have issues on macOS with certain libraries

### Safe Worker (`worker_safe.py`)
- Uses multiprocessing with spawn method
- Specifically designed for macOS compatibility
- Slightly higher memory usage but more stable

### Smart Startup (`start_worker.py`)
- Automatically detects the operating system
- Chooses the best worker configuration
- Includes Redis connectivity checks

## Performance Optimization

### 1. Increase Worker Timeout
For large presentations, increase the job timeout:
```python
# In worker.py
worker = Worker(
    ["presentations"], 
    connection=redis_conn,
    job_timeout='30m',  # Increase from 15m to 30m
)
```

### 2. Multiple Workers
Run multiple workers for better throughput:
```bash
# Terminal 1
python worker.py

# Terminal 2
python worker.py

# Terminal 3
python worker.py
```

### 3. Monitor Worker Performance
```bash
# Check queue status
python -c "
from app.task_queue import presentation_queue
print(f'Jobs in queue: {len(presentation_queue)}')
print(f'Failed jobs: {len(presentation_queue.failed_job_registry)}')
"
```

## Debugging Tips

### 1. Enable Verbose Logging
```python
# Add to worker.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. Test Task Function Directly
```python
# Test without queue
from app.workers.tasks import generate_presentation_task
result = generate_presentation_task("your-presentation-id")
```

### 3. Check Process Status
```bash
# Find worker processes
ps aux | grep python | grep worker

# Monitor system resources
top -p $(pgrep -f worker.py)
```

## Environment Setup Checklist

- [ ] Redis server is running
- [ ] Virtual environment is activated
- [ ] All dependencies are installed (`pip install -r requirements.txt`)
- [ ] Database tables are created
- [ ] Environment variables are set (`.env` file)
- [ ] Running from project root directory
- [ ] PYTHONPATH includes project directory (if needed)

## Getting Help

If you're still experiencing issues:

1. **Check the logs** for detailed error messages
2. **Try the safe worker** if on macOS
3. **Test Redis connectivity** with `redis-cli ping`
4. **Verify database setup** by checking if tables exist
5. **Run the smart startup script** for automatic configuration

For persistent issues, consider:
- Using Docker for consistent environment
- Running on a Linux server instead of macOS for development
- Using a different task queue system (Celery) if RQ continues to have issues 