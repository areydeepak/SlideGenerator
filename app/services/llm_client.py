import openai
import os
import json
import httpx
from typing import List, Dict, Any
from dotenv import load_dotenv
from abc import ABC, abstractmethod

load_dotenv()

# -------------------------------
# Abstract Base for LLM Providers
# -------------------------------
class LLMProvider(ABC):
    @abstractmethod
    def generate_completion(self, prompt: str, system_prompt: str) -> str:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass

# -------------------------------
# OpenAI Provider
# -------------------------------
class OpenAIProvider(LLMProvider):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=api_key) if api_key else None

    def is_available(self) -> bool:
        if not self.client:
            return False
        try:
            self.client.models.list()
            return True
        except Exception:
            return False

    def generate_completion(self, prompt: str, system_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content

# -------------------------------
# Ollama Local Provider
# -------------------------------
class OllamaProvider(LLMProvider):
    def __init__(self, model: str = "mistral", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.client = httpx.Client(timeout=30.0)

    def is_available(self) -> bool:
        try:
            response = self.client.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except Exception:
            return False

    def generate_completion(self, prompt: str, system_prompt: str) -> str:
        full_prompt = f"{system_prompt}\n\n{prompt}"
        response = self.client.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model, "prompt": full_prompt, "stream": False}
        )
        return response.json()["response"]

# -------------------------------
# HuggingFace Inference Provider
# -------------------------------
class HuggingFaceProvider(LLMProvider):
    def __init__(self, model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.model = model
        self.base_url = "https://api-inference.huggingface.co/models"
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate_completion(self, prompt: str, system_prompt: str) -> str:
        client = httpx.Client(timeout=60.0)
        full_prompt = f"{system_prompt}\n\n{prompt}"
        response = client.post(
            f"{self.base_url}/{self.model}",
            headers=self.headers,
            json={
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": 2000,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
        )
        result = response.json()
        if isinstance(result, list) and result:
            return result[0].get("generated_text", "")
        return ""

# -------------------------------
# LLM Client Wrapper
# -------------------------------
class LLMClient:
    def __init__(self):
        self.providers = [
            OpenAIProvider(),
            HuggingFaceProvider(),
            OllamaProvider()
        ]
        self.active_provider = None
        for provider in self.providers:
            if provider.is_available():
                self.active_provider = provider
                print(f"Using LLM provider: {provider.__class__.__name__}")
                break

        if not self.active_provider:
            print("Warning: No LLM provider available, using fallback content")

    def generate_slide_content(self, topic: str, content: str, num_slides: int, config: dict = None) -> List[Dict[str, Any]]:
        actual_slides = max(num_slides, 3)

        # Create example JSON to show expected format
        example_json = json.dumps([
            {
                "title": "Introduction to Machine Learning",
                "slide_type": "title",
                "content": ["Understanding AI and ML", "Key concepts and applications", "What we'll cover today"],
                "notes": "Welcome everyone. Today we'll explore the fundamentals of machine learning.",
                "reference": "source: Stanford CS229"
            },
            {
                "title": "What is Machine Learning?",
                "slide_type": "bullet_points",
                "content": [
                    "Subset of artificial intelligence",
                    "Systems learn from data without explicit programming",
                    "Improves performance through experience",
                    "Used in recommendation systems, image recognition, and more"
                ],
                "notes": "Machine learning is transforming how we interact with technology daily.",
                "reference": "ref: Mitchell, 1997"
            },
            {
                "title": "References",
                "slide_type": "bullet_points",
                "content": ["source: Stanford CS229", "ref: Mitchell, 1997"],
                "notes": "Sources used in this presentation.",
                "reference": "Generated by AI"
            }
        ], indent=2)

        prompt = f"""
Create a presentation on "{topic}" using this content: "{content}".
Generate exactly {actual_slides} slides.

IMPORTANT: Return ONLY a valid JSON array. No explanations, no markdown, just the JSON array.

Required structure for EVERY slide:
- title: string
- slide_type: string (one of: "title", "bullet_points", "two_column", "content_with_image")
- content: array of strings (bullet points)
- notes: string (speaker notes)
- reference: string (source citation, max 50 chars)

Rules:
1. First slide: slide_type MUST be "title"
2. Last slide: title MUST be "References", slide_type MUST be "bullet_points"
3. Middle slides: vary between "bullet_points", "two_column", "content_with_image"

Example of expected JSON format:
{example_json}

Generate the JSON array now:"""

        system_prompt = "You are a presentation expert. Output ONLY valid JSON. No markdown, no explanation, just the JSON array."

        if not self.active_provider:
            return self._generate_fallback_content(topic, actual_slides)

        for provider in [self.active_provider] + [p for p in self.providers if p != self.active_provider and p.is_available()]:
            try:
                output = provider.generate_completion(prompt, system_prompt).strip()
                
                # Debug print
                print(f"Raw output from {provider.__class__.__name__}:")
                print(output[:500] + "..." if len(output) > 500 else output)

                # Clean up common issues
                output = output.strip()
                
                # Remove markdown code blocks
                if "```json" in output:
                    start = output.find("```json") + 7
                    end = output.rfind("```")
                    if end > start:
                        output = output[start:end].strip()
                elif "```" in output:
                    start = output.find("```") + 3
                    end = output.rfind("```")
                    if end > start:
                        output = output[start:end].strip()
                
                # Remove any text before the first [
                first_bracket = output.find('[')
                if first_bracket > 0:
                    output = output[first_bracket:]
                
                # Remove any text after the last ]
                last_bracket = output.rfind(']')
                if last_bracket > 0 and last_bracket < len(output) - 1:
                    output = output[:last_bracket + 1]

                # Try to parse JSON
                slides = json.loads(output)
                
                # Validate it's a list
                if not isinstance(slides, list):
                    raise ValueError("Output is not a JSON array")

                # Ensure we have the right number of slides
                while len(slides) < actual_slides:
                    slides.insert(-1, {
                        "title": f"Key Point {len(slides)}",
                        "slide_type": "bullet_points",
                        "content": [
                            f"Important aspect of {topic}",
                            "Supporting evidence",
                            "Practical applications"
                        ],
                        "notes": "Additional content for completeness",
                        "reference": "ref: AI-generated"
                    })

                slides = slides[:actual_slides]

                # Ensure first slide is title type
                if slides and slides[0].get("slide_type") != "title":
                    slides[0]["slide_type"] = "title"
                
                # Ensure last slide is references
                if slides:
                    slides[-1].update({
                        "title": "References",
                        "slide_type": "bullet_points",
                        "notes": "Sources used in this presentation.",
                        "reference": "Generated by AI"
                    })

                # Validate all required fields exist
                for i, slide in enumerate(slides):
                    required_fields = ["title", "slide_type", "content", "notes", "reference"]
                    for field in required_fields:
                        if field not in slide:
                            if field == "content":
                                slide[field] = ["Content placeholder"]
                            elif field == "notes":
                                slide[field] = "Speaker notes"
                            elif field == "reference":
                                slide[field] = "ref: AI-generated"
                            else:
                                slide[field] = f"Slide {i+1}"

                self.active_provider = provider
                print(f"Successfully used provider: {provider.__class__.__name__}")
                return slides

            except Exception as e:
                print(f"Error with provider {provider.__class__.__name__}: {e}")
                continue

        print("All providers failed, using fallback content")
        return self._generate_fallback_content(topic, actual_slides)

    def _generate_fallback_content(self, topic: str, num_slides: int) -> List[Dict[str, Any]]:
        slides = []

        slides.append({
            "title": f"{topic}",
            "content": ["A comprehensive overview", "Key insights and analysis", "Practical applications"],
            "slide_type": "title",
            "notes": f"Introduction to {topic}",
            "reference": "source: Generated Content"
        })

        intermediate_slide_count = num_slides - 2
        slide_types = ["bullet_points", "two_column", "content_with_image"]
        reference_sources = [
            "ref: Industry Report",
            "source: Academic Research",
            "ref: Expert Analysis",
            "source: Case Studies",
            "ref: Market Data"
        ]

        for i in range(intermediate_slide_count):
            slides.append({
                "title": f"Key Point {i+1}",
                "content": [
                    f"Important aspect of {topic}",
                    "Supporting evidence and examples",
                    "Practical implications",
                    "Real-world applications"
                ],
                "slide_type": slide_types[i % len(slide_types)],
                "notes": f"Detailed discussion of point {i+1}",
                "reference": reference_sources[i % len(reference_sources)]
            })

        slides.append({
            "title": "References",
            "content": [
                "source: Generated Content",
                "ref: Industry Report",
                "source: Academic Research"
            ],
            "slide_type": "bullet_points",
            "notes": "Sources used in this presentation.",
            "reference": "Generated by AI"
        })

        return slides 