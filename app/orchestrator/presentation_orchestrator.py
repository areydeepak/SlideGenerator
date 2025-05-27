from app.models.presentation import Presentation, PresentationStatus
from app.schemas.presentation_schema import PresentationCreate, PresentationUpdate
from app.task_queue import get_queue
from app.workers.tasks import generate_presentation_task
from sqlalchemy.orm import Session
from typing import Optional
import uuid


class PresentationOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.queue = get_queue()
    
    def create_presentation(self, presentation_data: PresentationCreate) -> Presentation:
        """Create a new presentation and queue it for generation"""
        
        # Create presentation record
        presentation = Presentation(
            id=str(uuid.uuid4()),
            topic=presentation_data.topic,
            content=presentation_data.content,
            num_slides=presentation_data.num_slides or 10,
            status=PresentationStatus.PENDING
        )
        
        self.db.add(presentation)
        self.db.commit()
        self.db.refresh(presentation)
        
        # Queue the presentation generation task
        job = self.queue.enqueue(
            generate_presentation_task,
            presentation.id,
            job_timeout='10m'
        )
        
        return presentation
    
    def get_presentation(self, presentation_id: str) -> Optional[Presentation]:
        """Get a presentation by ID"""
        return self.db.query(Presentation).filter(Presentation.id == presentation_id).first()
    
    def update_presentation(self, presentation_id: str, update_data: PresentationUpdate) -> Optional[Presentation]:
        """Update presentation configuration"""
        
        presentation = self.get_presentation(presentation_id)
        if not presentation:
            return None
        
        # Update fields if provided
        if update_data.num_slides is not None:
            presentation.num_slides = update_data.num_slides
        
        self.db.commit()
        self.db.refresh(presentation)
        
        return presentation
    
    def get_all_presentations(self, skip: int = 0, limit: int = 100):
        """Get all presentations with pagination"""
        return self.db.query(Presentation).offset(skip).limit(limit).all()
    
    def delete_presentation(self, presentation_id: str) -> bool:
        """Delete a presentation"""
        presentation = self.get_presentation(presentation_id)
        if not presentation:
            return False
        
        self.db.delete(presentation)
        self.db.commit()
        return True 