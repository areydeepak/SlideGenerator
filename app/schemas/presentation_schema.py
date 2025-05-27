from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from app.constants.constants import (
    PresentationStatus, 
    PresentationTheme, 
    SlideLayoutType,
    Defaults
)




class SlideColorScheme(BaseModel):
    """Color scheme for presentation slides"""
    primary: str = Field("#1F497D", description="Primary color (hex code)")
    secondary: str = Field("#4472C4", description="Secondary color (hex code)")
    accent: str = Field("#ED7D31", description="Accent color (hex code)")
    background: str = Field("#FFFFFF", description="Background color (hex code)")


class PresentationConfig(BaseModel):
    """Detailed configuration for presentation generation"""
    theme: Optional[PresentationTheme] = Field(
        PresentationTheme.PROFESSIONAL, 
        description="Visual theme for the presentation"
    )
    colors: Optional[SlideColorScheme] = None
    font_name: Optional[str] = Field("Calibri", description="Main font for the presentation")
    include_table_of_contents: Optional[bool] = Field(
        False, 
        description="Whether to include a table of contents slide"
    )
    include_speaker_notes: Optional[bool] = Field(
        True, 
        description="Whether to generate speaker notes for each slide"
    )
    aspect_ratio: Optional[str] = Field(
        "16:9", 
        description="Slide aspect ratio (16:9 or 4:3)"
    )
    slide_transitions: Optional[bool] = Field(
        False, 
        description="Whether to add slide transitions"
    )
    slide_layouts: Optional[List[SlideLayoutType]] = Field(
        None,
        description="Specific slide layouts to use in the presentation"
    )
    additional_settings: Optional[Dict[str, Any]] = Field(
        None, 
        description="Any additional custom settings"
    )


class PresentationCreate(BaseModel):
    topic: str = Field(
        ..., 
        description="The topic for the presentation",
        example="Artificial Intelligence and Machine Learning"
    )
    content: str = Field(
        ..., 
        description="The content to be used for generating the presentation",
        example="AI is transforming industries through automation and data analysis. Machine learning enables computers to learn from data without explicit programming."
    )
    num_slides: int = Field(
        ge=Defaults.MIN_SLIDES, 
        le=Defaults.MAX_SLIDES, 
        default=Defaults.DEFAULT_NUM_SLIDES
    )

    class Config:
        schema_extra = {
            "example": {
                "topic": "Introduction to Quantum Computing",
                "content": "Quantum computing leverages quantum mechanics principles like superposition and entanglement. It promises exponential speedups for certain computational problems. Applications include cryptography, drug discovery, and optimization.",
                "num_slides": 8
            }
        }


class PresentationUpdate(BaseModel):
    topic: Optional[str] = None
    content: Optional[str] = None
    num_slides: Optional[int] = Field(
        None, 
        ge=Defaults.MIN_SLIDES, 
        le=Defaults.MAX_SLIDES
    )


class PresentationStyleConfig(BaseModel):
    """Configuration for presentation styling"""
    theme: Optional[str] = None
    background_color: Optional[str] = None
    font: Optional[str] = None
    title_color: Optional[str] = None
    content_color: Optional[str] = None
    accent_color: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "theme": PresentationTheme.CORPORATE.value,
                "background_color": "#F5F5F5",
                "font": "Helvetica",
                "title_color": "#003366",
                "content_color": "#333333",
                "accent_color": "#FF6600"
            }
        }


class SlideData(BaseModel):
    """Structure for individual slide data"""
    title: str = Field(..., description="The slide title")
    slide_type: str = Field(
        ..., 
        description="Type of slide layout",
        example=SlideLayoutType.BULLET_POINTS.value
    )
    content: List[str] = Field(
        ..., 
        description="List of bullet points or content items",
        example=["Point 1", "Point 2", "Point 3"]
    )
    notes: str = Field(..., description="Speaker notes for the slide")
    reference: str = Field(
        ..., 
        description="Citation or source reference",
        example="source: WHO Report 2023"
    )


class PresentationResponse(BaseModel):
    id: str
    topic: str
    content: str
    status: str
    file_path: Optional[str] = None
    num_slides: int
    slides_data: Optional[List[Dict[str, Any]]] = None
    style_config: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PresentationListResponse(BaseModel):
    id: str
    topic: str
    content: str
    status: str
    file_path: Optional[str] = None
    num_slides: int
    style_config: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class JobResponse(BaseModel):
    id: str
    presentation_id: str
    status: str
    error: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 