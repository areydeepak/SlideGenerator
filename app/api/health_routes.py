from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.task_queue import get_queue
from datetime import datetime

router = APIRouter()


@router.get("/health")
def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "presentation-generator"
    }


@router.get("/health/detailed")
def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check with component status"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {}
    }
    
    # Check database
    try:
        db.execute("SELECT 1")
        health_status["components"]["database"] = {
            "status": "healthy",
            "message": "Database connection successful"
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["components"]["database"] = {
            "status": "unhealthy",
            "message": f"Database error: {str(e)}"
        }
    
    # Check Redis queue
    try:
        queue = get_queue()
        job_count = len(queue)
        health_status["components"]["queue"] = {
            "status": "healthy",
            "message": f"Queue operational with {job_count} jobs"
        }
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["components"]["queue"] = {
            "status": "unhealthy",
            "message": f"Queue error: {str(e)}"
        }
    
    return health_status 