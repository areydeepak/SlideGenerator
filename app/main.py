from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import presentation_router, health_router
from app.database import engine, Base
import uvicorn

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Presentation Generator API",
    description="""
    A presentation generation service that creates structured PowerPoint presentations.
    
    ## Features
    
    * **Content-based Generation**: Provide a topic and content, get a structured presentation
    * **LLM-powered**: Uses AI to generate appropriate slide content with proper structure
    * **Preset Templates**: Each slide type (title, bullet_points, two_column, content_with_image) 
      has a predefined template for consistent styling
    * **Separation of Concerns**: Content generation is separate from slide rendering, 
      allowing for easy customization and multiple export formats
    
    ## How it works
    
    1. Submit a topic, content, and desired number of slides
    2. The LLM generates a structured JSON array of slides
    3. Each slide includes: title, slide_type, content, notes, and reference
    4. Preset templates are applied based on slide_type for consistent design
    5. The final PowerPoint file is generated and made available for download
    """,
    version="2.0.0",
    contact={
        "name": "SlideGenerator Support",
        "email": "support@slidegenerator.example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, tags=["health"])
app.include_router(presentation_router, prefix="/api/v1", tags=["presentations"])

@app.get("/")
def root():
    return {
        "message": "Presentation Generator API",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 