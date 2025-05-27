#!/usr/bin/env python3
"""
Smart worker startup script that chooses the best configuration
based on the operating system and available options.
"""

import os
import sys
import subprocess
import platform

def detect_system():
    """Detect the operating system and recommend the best worker"""
    system = platform.system().lower()
    
    if system == 'darwin':  # macOS
        return 'macos'
    elif system == 'linux':
        return 'linux'
    elif system == 'windows':
        return 'windows'
    else:
        return 'unknown'

def check_redis():
    """Check if Redis is running"""
    try:
        import redis
        from app.task_queue import redis_conn
        redis_conn.ping()
        return True
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False

def start_worker():
    """Start the appropriate worker based on the system"""
    system = detect_system()
    
    print("🚀 Slide Generator Worker Startup")
    print("=" * 40)
    print(f"Detected system: {system}")
    
    # Check Redis connection
    if not check_redis():
        print("\n💡 Make sure Redis is running:")
        if system == 'macos':
            print("   brew install redis")
            print("   brew services start redis")
        elif system == 'linux':
            print("   sudo apt-get install redis-server")
            print("   sudo systemctl start redis")
        else:
            print("   Install and start Redis server")
        return False
    
    print("✅ Redis connection successful")
    
    # Choose worker script based on system
    if system == 'macos':
        print("\n🍎 Starting macOS-optimized worker...")
        print("Using spawn method to avoid forking issues")
        
        # Try the safe worker first
        try:
            subprocess.run([sys.executable, "worker_safe.py"])
        except KeyboardInterrupt:
            print("\nWorker stopped")
        except Exception as e:
            print(f"Safe worker failed: {e}")
            print("Falling back to standard worker...")
            try:
                subprocess.run([sys.executable, "worker.py"])
            except KeyboardInterrupt:
                print("\nWorker stopped")
    
    else:
        print(f"\n🐧 Starting standard worker for {system}...")
        try:
            subprocess.run([sys.executable, "worker.py"])
        except KeyboardInterrupt:
            print("\nWorker stopped")
    
    return True

if __name__ == "__main__":
    print("Starting Slide Generator Worker...")
    
    if len(sys.argv) > 1:
        worker_type = sys.argv[1].lower()
        if worker_type == 'safe':
            print("🔒 Using safe worker (multiprocessing)")
            subprocess.run([sys.executable, "worker_safe.py"])
        elif worker_type == 'standard':
            print("⚡ Using standard worker")
            subprocess.run([sys.executable, "worker.py"])
        else:
            print("Usage: python start_worker.py [safe|standard]")
            sys.exit(1)
    else:
        start_worker() 