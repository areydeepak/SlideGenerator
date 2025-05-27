from app.database import get_db
from app.models.presentation import Presentation, PresentationStatus
from app.services.llm_client import LLMClient
from app.services.pptx_creator import PPTXCreator
import time
import os
import traceback
from datetime import datetime

def generate_presentation_task(presentation_id):
    """Task to generate a presentation"""
    
    # Get database session
    db = next(get_db())
    
    try:
        # Get presentation from database
        presentation = db.query(Presentation).filter(Presentation.id == presentation_id).first()
        
        if not presentation:
            print(f"Presentation with ID {presentation_id} not found")
            return
        
        # Update status to processing
        presentation.status = PresentationStatus.PROCESSING
        db.commit()
        
        # Initialize services
        llm_client = LLMClient()
        pptx_creator = PPTXCreator()
        
        # Generate slide content using LLM with the provided content
        slides_data = llm_client.generate_slide_content(
            topic=presentation.topic,
            content=presentation.content,
            num_slides=presentation.num_slides
        )
        
        # Store the generated slides data in the database
        presentation.slides_data = slides_data
        db.commit()
        
        # Define preset template configuration based on slide types
        # This allows for easy customization and consistent styling
        preset_config = {
            "theme": "professional",
            "font": "Calibri",
            "background_color": "#FFFFFF",
            "aspect_ratio": "16:9",
            # Preset templates determine layout and design
            "slide_templates": {
                "title": {
                    "layout": "title_slide",
                    "font_size": {"title": 44, "subtitle": 24},
                    "alignment": "center"
                },
                "bullet_points": {
                    "layout": "content_slide",
                    "font_size": {"title": 36, "content": 20},
                    "bullet_style": "standard"
                },
                "two_column": {
                    "layout": "comparison_slide",
                    "font_size": {"title": 36, "content": 18},
                    "column_split": "50/50"
                },
                "content_with_image": {
                    "layout": "picture_with_caption",
                    "font_size": {"title": 36, "content": 20},
                    "image_placeholder": True
                }
            }
        }
        
        # Generate PowerPoint using the content and preset templates
        file_path = pptx_creator.create_presentation(
            slides_data=slides_data,
            topic=presentation.topic,
            config=preset_config
        )
        
        # Update presentation record with file path
        presentation.file_path = file_path
        presentation.status = PresentationStatus.COMPLETED
        presentation.updated_at = datetime.utcnow()
        db.commit()
        
        print(f"Successfully generated presentation: {file_path}")
        
    except Exception as e:
        # Log error and update presentation status
        error_msg = f"Error generating presentation: {str(e)}"
        traceback_str = traceback.format_exc()
        print(error_msg)
        print(traceback_str)
        
        try:
            presentation.status = PresentationStatus.FAILED
            presentation.updated_at = datetime.utcnow()
            db.commit()
        except:
            print("Failed to update presentation status")
        
    finally:
        db.close() 