#!/usr/bin/env python3
"""
Simple test script to verify the slide generator application works.
This script tests the core functionality without requiring Redis or OpenAI.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.llm_client import LLMClient
from app.services.pptx_creator import PPTXCreator


def test_llm_fallback():
    """Test LLM client fallback functionality"""
    print("Testing LLM client fallback...")
    
    llm_client = LLMClient()
    
    # This will use fallback since no OpenAI key is set
    slides = llm_client._generate_fallback_content("Artificial Intelligence", 5)
    
    print(f"Generated {len(slides)} slides")
    for i, slide in enumerate(slides):
        print(f"Slide {i+1}: {slide['title']} ({slide['slide_type']})")
    
    return slides


def test_pptx_creation():
    """Test PowerPoint creation"""
    print("\nTesting PowerPoint creation...")
    
    # Generate test content
    slides_data = [
        {
            "title": "Artificial Intelligence",
            "content": ["Overview of AI", "Machine Learning", "Deep Learning"],
            "slide_type": "title",
            "notes": "Introduction to AI"
        },
        {
            "title": "Machine Learning Basics",
            "content": [
                "Supervised Learning",
                "Unsupervised Learning", 
                "Reinforcement Learning",
                "Neural Networks"
            ],
            "slide_type": "content",
            "notes": "Core ML concepts"
        },
        {
            "title": "Conclusion",
            "content": [
                "AI is transforming industries",
                "Machine learning is the key",
                "Future looks promising"
            ],
            "slide_type": "conclusion",
            "notes": "Wrap up the presentation"
        }
    ]
    
    # Create presentation
    pptx_creator = PPTXCreator()
    file_path = pptx_creator.create_presentation(slides_data, "Test AI Presentation")
    
    print(f"Created presentation: {file_path}")
    
    # Check if file exists
    if os.path.exists(file_path):
        print("✅ PowerPoint file created successfully!")
        file_size = os.path.getsize(file_path)
        print(f"File size: {file_size} bytes")
        return True
    else:
        print("❌ PowerPoint file creation failed!")
        return False


def main():
    """Run all tests"""
    print("🧪 Running Slide Generator Tests\n")
    
    try:
        # Test LLM fallback
        slides = test_llm_fallback()
        
        # Test PowerPoint creation
        success = test_pptx_creation()
        
        if success:
            print("\n✅ All tests passed! The application is working correctly.")
            print("\nNext steps:")
            print("1. Set up your OpenAI API key in .env file")
            print("2. Start Redis server: redis-server")
            print("3. Start the worker: python worker.py")
            print("4. Start the API: python app/main.py")
        else:
            print("\n❌ Some tests failed. Please check the error messages above.")
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 