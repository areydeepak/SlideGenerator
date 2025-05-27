from sqlalchemy import Column, String, Integer, DateTime, JSON, Enum, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.constants.constants import PresentationStatus, PresentationTheme, SlideLayoutType, Defaults

Base = declarative_base()


class Presentation(Base):
    __tablename__ = "presentations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    topic = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String, default=PresentationStatus.PENDING.value)
    file_path = Column(String)
    num_slides = Column(Integer, default=Defaults.DEFAULT_NUM_SLIDES)
    slides_data = Column(JSON)  # Stores the generated slide content
    style_config = Column(JSON)  # Stores the styling configuration
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    job = relationship("Job", back_populates="presentation", uselist=False)
    
    @property
    def theme(self):
        """Get the presentation theme"""
        if self.slides_data and 'theme' in self.slides_data:
            return self.slides_data['theme']
        return PresentationTheme.PROFESSIONAL.value  # Default theme
    
    @property
    def has_speaker_notes(self):
        """Check if the presentation includes speaker notes"""
        if self.slides_data and 'include_speaker_notes' in self.slides_data:
            return self.slides_data['include_speaker_notes']
        return True  # Default to include speaker notes


class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(String, primary_key=True)
    presentation_id = Column(String, ForeignKey("presentations.id"))
    status = Column(String, default=PresentationStatus.PENDING.value)
    error = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    presentation = relationship("Presentation", back_populates="job") 