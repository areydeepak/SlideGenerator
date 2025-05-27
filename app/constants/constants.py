from enum import Enum
from typing import Dict, Any

# Presentation Status Constants
class PresentationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# Presentation Theme Constants
class PresentationTheme(str, Enum):
    PROFESSIONAL = "professional"
    CORPORATE = "corporate"
    CREATIVE = "creative"
    ACADEMIC = "academic"
    DARK = "dark"
    MINIMAL = "minimal"
    MODERN_STARTUP = "modern startup"
    YOUTHFUL = "youthful"
    LIGHT = "light"

# Slide Layout Constants
class SlideLayoutType(str, Enum):
    TITLE = "title"
    BULLET_POINTS = "bullet_points"
    TWO_COLUMN = "two_column"
    CONTENT_WITH_IMAGE = "content_with_image"

# LLM Provider Constants
class LLMProvider(str, Enum):
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    OLLAMA = "ollama"
    TEMPLATE = "template"

# Default Style Configurations
DEFAULT_STYLES: Dict[str, Dict[str, Any]] = {
    "professional": {
        "background_color": "#FFFFFF",
        "title_color": "#1F497D",
        "content_color": "#444444",
        "accent_color": "#ED7D31",
        "font": "Calibri"
    },
    "corporate": {
        "background_color": "#F5F5F5",
        "title_color": "#003366",
        "content_color": "#333333",
        "accent_color": "#FF6600",
        "font": "Arial"
    },
    "creative": {
        "background_color": "#FFFAF0",
        "title_color": "#B22222",
        "content_color": "#2F4F4F",
        "accent_color": "#4682B4",
        "font": "Georgia"
    },
    "academic": {
        "background_color": "#FFFFFF",
        "title_color": "#8B0000",
        "content_color": "#000000",
        "accent_color": "#DAA520",
        "font": "Times New Roman"
    },
    "dark": {
        "background_color": "#121212",
        "title_color": "#BB86FC",
        "content_color": "#E0E0E0",
        "accent_color": "#03DAC6",
        "font": "Helvetica"
    },
    "minimal": {
        "background_color": "#FFFFFF",
        "title_color": "#333333",
        "content_color": "#555555",
        "accent_color": "#999999",
        "font": "Helvetica"
    }
}

# PPTX Constants
class PPTXConstants:
    # Layout indices
    TITLE_LAYOUT_INDEX = 0
    CONTENT_LAYOUT_INDEX = 1
    TWO_COLUMN_LAYOUT_INDEX = 3
    PICTURE_LAYOUT_INDEX = 5
    
    # Default values
    DEFAULT_ASPECT_RATIO = "16:9"
    DEFAULT_FONT = "Calibri"
    DEFAULT_BACKGROUND_COLOR = "#FFFFFF"
    DEFAULT_THEME = "professional"
    
    # Sizes
    TITLE_FONT_SIZE = 36
    TITLE_SLIDE_FONT_SIZE = 44
    SUBTITLE_FONT_SIZE = 24
    BULLET_FONT_SIZE = 20
    CONCLUSION_FONT_SIZE = 22
    REFERENCE_FONT_SIZE = 10
    
    # Positioning
    REFERENCE_LEFT = 0.5  # in inches
    REFERENCE_TOP = 7.0   # in inches
    REFERENCE_WIDTH = 12.0  # in inches
    REFERENCE_HEIGHT = 0.3  # in inches

# LLM Constants
class LLMConstants:
    # OpenAI
    OPENAI_DEFAULT_MODEL = "gpt-3.5-turbo"
    
    # HuggingFace
    HUGGINGFACE_DEFAULT_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    HUGGINGFACE_BASE_URL = "https://api-inference.huggingface.co/models"
    HUGGINGFACE_MAX_TOKENS = 2000
    HUGGINGFACE_TEMPERATURE = 0.7
    
    # Ollama
    OLLAMA_DEFAULT_MODEL = "mistral"
    OLLAMA_BASE_URL = "http://localhost:11434"
    
    # Prompt construction
    SYSTEM_PROMPT = "You are a presentation expert. Output ONLY valid JSON. No markdown, no explanation, just the JSON array."
    SLIDE_TYPES_INSTRUCTION = "slide_type: string (one of: \"title\", \"bullet_points\", \"two_column\", \"content_with_image\")"
    
    # Formatting
    TITLE_SLIDE_TYPE = "title"
    REFERENCES_TITLE = "References"
    BULLET_POINTS_TYPE = "bullet_points"

# File paths
class FilePaths:
    PRESENTATIONS_DIR = "presentations"
    
# API routes
class APIRoutes:
    API_PREFIX = "/api/v1"
    PRESENTATIONS = "/presentations/"
    PRESENTATION_BY_ID = "/presentations/{presentation_id}"
    PRESENTATION_STYLE = "/presentations/{presentation_id}/configure-style"
    
# Error messages
class ErrorMessages:
    PRESENTATION_NOT_FOUND = "Presentation not found"
    PRESENTATION_INCOMPLETE = "Presentation must be completed before styling can be applied"
    STYLE_APPLICATION_FAILED = "Failed to apply style configuration"
    
# Success messages
class SuccessMessages:
    PRESENTATION_DELETED = "Presentation deleted successfully"
    
# Default values
class Defaults:
    DEFAULT_NUM_SLIDES = 10
    MAX_SLIDES = 20
    MIN_SLIDES = 1 