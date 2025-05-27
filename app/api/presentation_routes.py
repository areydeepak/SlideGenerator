from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.presentation_schema import (
    PresentationCreate, 
    PresentationResponse, 
    PresentationUpdate,
    PresentationStyleConfig,
    PresentationListResponse
)
from app.orchestrator.presentation_orchestrator import PresentationOrchestrator
from app.services.pptx_creator import PPTXCreator
from app.models.presentation import Presentation
from app.constants.constants import (
    PresentationStatus,
    APIRoutes,
    ErrorMessages,
    SuccessMessages,
    PPTXConstants,
    FilePaths
)
import os
from datetime import datetime

router = APIRouter()


@router.post(APIRoutes.PRESENTATIONS, response_model=PresentationResponse)
def create_presentation(
    presentation: PresentationCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new presentation with topic, content, and number of slides.
    
    The content will be used by an LLM to generate structured slide data,
    which will then be rendered using preset slide templates.
    """
    orchestrator = PresentationOrchestrator(db)
    return orchestrator.create_presentation(presentation)


@router.get(APIRoutes.PRESENTATION_BY_ID, response_model=PresentationResponse)
def get_presentation(
    presentation_id: str,
    db: Session = Depends(get_db)
):
    """Get a presentation by ID"""
    orchestrator = PresentationOrchestrator(db)
    presentation = orchestrator.get_presentation(presentation_id)
    
    if not presentation:
        raise HTTPException(status_code=404, detail=ErrorMessages.PRESENTATION_NOT_FOUND)
    
    return presentation


@router.get(APIRoutes.PRESENTATIONS, response_model=List[PresentationListResponse])
def list_presentations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List all presentations with pagination"""
    orchestrator = PresentationOrchestrator(db)
    return orchestrator.get_all_presentations(skip=skip, limit=limit)


@router.put(APIRoutes.PRESENTATION_BY_ID, response_model=PresentationResponse)
def update_presentation(
    presentation_id: str,
    presentation_update: PresentationUpdate,
    db: Session = Depends(get_db)
):
    """Update a presentation"""
    orchestrator = PresentationOrchestrator(db)
    presentation = orchestrator.update_presentation(presentation_id, presentation_update)
    
    if not presentation:
        raise HTTPException(status_code=404, detail=ErrorMessages.PRESENTATION_NOT_FOUND)
    
    return presentation


@router.post(APIRoutes.PRESENTATION_STYLE, response_model=PresentationResponse)
def configure_presentation_style(
    presentation_id: str,
    style_config: PresentationStyleConfig,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Configure or update the styling of an existing presentation.
    
    This endpoint allows you to:
    - Apply a theme (professional, corporate, creative, academic, dark, minimal, etc.)
    - Set custom colors for background, title, content, and accents
    - Change the font family
    
    The presentation will be regenerated with the new styling while preserving the content.
    """
    # Get the presentation
    presentation = db.query(Presentation).filter(Presentation.id == presentation_id).first()
    if not presentation:
        raise HTTPException(status_code=404, detail=ErrorMessages.PRESENTATION_NOT_FOUND)
    
    # Check if presentation has slides_data
    if not presentation.slides_data:
        raise HTTPException(
            status_code=400, 
            detail=ErrorMessages.PRESENTATION_INCOMPLETE
        )
    
    # Create a new dictionary for style_config from the request
    new_style_config = style_config.dict(exclude_unset=True, exclude_none=True)
    print(f"New style config from request: {new_style_config}")
    
    # Completely replace the style_config (don't try to update the existing one)
    presentation.style_config = new_style_config
    
    # Create complete config for PPTXCreator
    pptx_config = {
        "theme": new_style_config.get("theme", PPTXConstants.DEFAULT_THEME),
        "font": new_style_config.get("font", PPTXConstants.DEFAULT_FONT),
        "background_color": new_style_config.get("background_color", PPTXConstants.DEFAULT_BACKGROUND_COLOR),
        "aspect_ratio": PPTXConstants.DEFAULT_ASPECT_RATIO
    }
    
    # Add custom colors if specified
    if "title_color" in new_style_config:
        pptx_config["title_color"] = new_style_config["title_color"]
    if "content_color" in new_style_config:
        pptx_config["content_color"] = new_style_config["content_color"]
    if "accent_color" in new_style_config:
        pptx_config["accent_color"] = new_style_config["accent_color"]
    
    print(f"PPTXCreator config: {pptx_config}")
    
    # Regenerate the presentation with new styling
    try:
        pptx_creator = PPTXCreator()
        
        # Delete old file if exists
        if presentation.file_path and os.path.exists(presentation.file_path):
            os.remove(presentation.file_path)
        
        # Generate new presentation with updated styling
        new_file_path = pptx_creator.create_presentation(
            slides_data=presentation.slides_data,
            topic=presentation.topic,
            config=pptx_config
        )
        
        # Update presentation record
        presentation.file_path = new_file_path
        presentation.updated_at = datetime.utcnow()
        
        # Commit the changes to the database
        db.commit()
        
        # Refresh to verify the changes were saved
        db.refresh(presentation)
        print(f"Style config after commit: {presentation.style_config}")
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"{ErrorMessages.STYLE_APPLICATION_FAILED}: {str(e)}"
        )
    
    # Final check - ensure we're returning the updated style_config
    db.refresh(presentation)
    return presentation


@router.delete(APIRoutes.PRESENTATION_BY_ID)
def delete_presentation(
    presentation_id: str,
    db: Session = Depends(get_db)
):
    """Delete a presentation"""
    orchestrator = PresentationOrchestrator(db)
    deleted = orchestrator.delete_presentation(presentation_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail=ErrorMessages.PRESENTATION_NOT_FOUND)
    
    return {"message": SuccessMessages.PRESENTATION_DELETED} 