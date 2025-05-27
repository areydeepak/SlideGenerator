#!/usr/bin/env python3
"""
Script to create sample presentations for demonstration purposes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.llm_client import LLMClient
from app.services.pptx_creator import PPTXCreator


def create_climate_change_presentation():
    """Create a sample presentation about climate change"""
    
    slides_data = [
        {
            "title": "Climate Change: A Global Challenge",
            "content": [
                "Understanding the science behind climate change",
                "Examining current impacts and future projections",
                "Exploring solutions and mitigation strategies"
            ],
            "slide_type": "title",
            "notes": "Welcome to our presentation on climate change"
        },
        {
            "title": "What is Climate Change?",
            "content": [
                "Long-term shifts in global temperatures and weather patterns",
                "Primarily driven by human activities since the 1800s",
                "Greenhouse gas emissions trap heat in Earth's atmosphere",
                "Carbon dioxide levels have increased by 40% since pre-industrial times"
            ],
            "slide_type": "content",
            "notes": "Define climate change and its primary causes"
        },
        {
            "title": "Current Impacts",
            "content": [
                "Rising global temperatures and sea levels",
                "More frequent extreme weather events",
                "Melting ice caps and glaciers",
                "Ecosystem disruption and species migration",
                "Agricultural challenges and food security issues"
            ],
            "slide_type": "content",
            "notes": "Discuss the observable impacts we're seeing today"
        },
        {
            "title": "Future Projections",
            "content": [
                "Temperature increases of 1.5-4°C by 2100",
                "Sea level rise of 0.3-2.5 meters",
                "Increased frequency of heat waves and droughts",
                "Potential for irreversible tipping points"
            ],
            "slide_type": "content",
            "notes": "Share scientific projections for the future"
        },
        {
            "title": "Mitigation Strategies",
            "content": [
                "Transition to renewable energy sources",
                "Improve energy efficiency in buildings and transportation",
                "Protect and restore natural ecosystems",
                "Develop carbon capture and storage technologies",
                "Implement carbon pricing mechanisms"
            ],
            "slide_type": "content",
            "notes": "Outline key strategies to reduce emissions"
        },
        {
            "title": "Individual Actions",
            "content": [
                "Reduce energy consumption at home",
                "Choose sustainable transportation options",
                "Support renewable energy initiatives",
                "Make conscious consumer choices",
                "Advocate for climate-friendly policies"
            ],
            "slide_type": "content",
            "notes": "Empower audience with actionable steps"
        },
        {
            "title": "Conclusion",
            "content": [
                "Climate change is an urgent global challenge",
                "Immediate action is required at all levels",
                "Technology and policy solutions exist",
                "Individual actions collectively make a difference",
                "The time to act is now"
            ],
            "slide_type": "conclusion",
            "notes": "Summarize key points and call to action"
        }
    ]
    
    pptx_creator = PPTXCreator()
    file_path = pptx_creator.create_presentation(slides_data, "Climate Change")
    
    # Move to output_samples
    import shutil
    os.makedirs("output_samples", exist_ok=True)
    shutil.move(file_path, "output_samples/climate_change.pptx")
    print("✅ Created climate_change.pptx")


def create_ai_future_presentation():
    """Create a sample presentation about the future of AI"""
    
    slides_data = [
        {
            "title": "The Future of Artificial Intelligence",
            "content": [
                "Exploring AI's transformative potential",
                "Current state and emerging trends",
                "Opportunities and challenges ahead"
            ],
            "slide_type": "title",
            "notes": "Introduction to AI's future prospects"
        },
        {
            "title": "Current State of AI",
            "content": [
                "Machine learning and deep learning breakthroughs",
                "Natural language processing advances",
                "Computer vision and image recognition",
                "AI in healthcare, finance, and transportation",
                "Growing investment and research activity"
            ],
            "slide_type": "content",
            "notes": "Overview of where AI stands today"
        },
        {
            "title": "Emerging AI Technologies",
            "content": [
                "Generative AI and large language models",
                "Autonomous systems and robotics",
                "Quantum machine learning",
                "Neuromorphic computing",
                "AI-human collaboration interfaces"
            ],
            "slide_type": "content",
            "notes": "Discuss cutting-edge AI developments"
        },
        {
            "title": "Industry Transformation",
            "content": [
                "Healthcare: Personalized medicine and drug discovery",
                "Transportation: Autonomous vehicles and smart logistics",
                "Education: Adaptive learning and intelligent tutoring",
                "Manufacturing: Predictive maintenance and optimization",
                "Finance: Algorithmic trading and risk assessment"
            ],
            "slide_type": "content",
            "notes": "How AI will reshape various industries"
        },
        {
            "title": "Challenges and Considerations",
            "content": [
                "Ethical AI development and bias mitigation",
                "Job displacement and workforce adaptation",
                "Privacy and data security concerns",
                "Regulatory frameworks and governance",
                "Ensuring AI safety and alignment"
            ],
            "slide_type": "content",
            "notes": "Address important challenges and concerns"
        },
        {
            "title": "Preparing for the AI Future",
            "content": [
                "Invest in AI education and skills development",
                "Foster responsible AI research and development",
                "Create adaptive regulatory frameworks",
                "Promote inclusive AI that benefits everyone",
                "Maintain human agency and oversight"
            ],
            "slide_type": "content",
            "notes": "Steps to prepare for AI's future impact"
        },
        {
            "title": "Conclusion",
            "content": [
                "AI will fundamentally transform society",
                "Proactive preparation is essential",
                "Collaboration between stakeholders is key",
                "The future of AI is in our hands",
                "Let's shape it responsibly"
            ],
            "slide_type": "conclusion",
            "notes": "Wrap up with key takeaways and call to action"
        }
    ]
    
    pptx_creator = PPTXCreator()
    file_path = pptx_creator.create_presentation(slides_data, "AI Future")
    
    # Move to output_samples
    import shutil
    shutil.move(file_path, "output_samples/ai_future.pptx")
    print("✅ Created ai_future.pptx")


def create_internet_history_presentation():
    """Create a sample presentation about the history of the internet"""
    
    slides_data = [
        {
            "title": "History of the Internet",
            "content": [
                "From ARPANET to the World Wide Web",
                "Key milestones and innovations",
                "Impact on society and communication"
            ],
            "slide_type": "title",
            "notes": "Journey through internet history"
        },
        {
            "title": "Early Foundations (1960s-1970s)",
            "content": [
                "ARPANET: The first packet-switching network",
                "TCP/IP protocol development",
                "Email invention and early adoption",
                "University and research institution connections"
            ],
            "slide_type": "content",
            "notes": "Discuss the foundational period of networking"
        },
        {
            "title": "Network Expansion (1980s)",
            "content": [
                "NSFNET and academic network growth",
                "Domain Name System (DNS) introduction",
                "First commercial internet service providers",
                "International network connections"
            ],
            "slide_type": "content",
            "notes": "Cover the expansion beyond research institutions"
        },
        {
            "title": "The World Wide Web (1990s)",
            "content": [
                "Tim Berners-Lee creates the Web at CERN",
                "First web browser and web server",
                "HTML, HTTP, and URL standards",
                "Mosaic browser brings graphics to the web",
                "Commercial internet boom begins"
            ],
            "slide_type": "content",
            "notes": "The revolutionary introduction of the Web"
        },
        {
            "title": "Dot-Com Era and Beyond (2000s)",
            "content": [
                "Broadband adoption and faster connections",
                "Social media platforms emerge",
                "E-commerce and online services growth",
                "Mobile internet and smartphone revolution",
                "Cloud computing and web services"
            ],
            "slide_type": "content",
            "notes": "The internet becomes mainstream"
        },
        {
            "title": "Modern Internet (2010s-Present)",
            "content": [
                "Internet of Things (IoT) expansion",
                "Streaming services and digital content",
                "Social media dominance",
                "Cybersecurity challenges",
                "Net neutrality debates"
            ],
            "slide_type": "content",
            "notes": "Current state and ongoing developments"
        },
        {
            "title": "Impact and Legacy",
            "content": [
                "Transformed global communication",
                "Revolutionized commerce and business",
                "Democratized access to information",
                "Created new forms of social interaction",
                "Continues to shape our digital future"
            ],
            "slide_type": "conclusion",
            "notes": "Reflect on the internet's profound impact"
        }
    ]
    
    pptx_creator = PPTXCreator()
    file_path = pptx_creator.create_presentation(slides_data, "History of Internet")
    
    # Move to output_samples
    import shutil
    shutil.move(file_path, "output_samples/history_of_internet.pptx")
    print("✅ Created history_of_internet.pptx")


def main():
    """Create all sample presentations"""
    print("🎨 Creating sample presentations...\n")
    
    try:
        create_climate_change_presentation()
        create_ai_future_presentation()
        create_internet_history_presentation()
        
        print("\n✅ All sample presentations created successfully!")
        print("📁 Check the output_samples/ directory for the files:")
        print("   - climate_change.pptx")
        print("   - ai_future.pptx")
        print("   - history_of_internet.pptx")
        
    except Exception as e:
        print(f"\n❌ Error creating samples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 