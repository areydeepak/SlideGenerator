from typing import Dict, Any


class LayoutPicker:
    """Utility class for selecting appropriate slide layouts based on content"""
    
    @staticmethod
    def get_layout_index(slide_data: Dict[str, Any]) -> int:
        """
        Return the appropriate layout index based on slide type and content
        
        Layout indices (standard PowerPoint layouts):
        0: Title Slide
        1: Title and Content
        2: Section Header
        3: Two Content
        4: Comparison
        5: Title Only
        6: Blank
        7: Content with Caption
        8: Picture with Caption
        """
        
        slide_type = slide_data.get("slide_type", "content")
        content = slide_data.get("content", [])
        
        if slide_type == "title":
            return 0  # Title slide layout
        elif slide_type == "section":
            return 2  # Section header layout
        elif slide_type == "conclusion":
            return 1  # Title and content (same as regular content)
        elif slide_type == "image":
            return 8  # Picture with caption
        elif slide_type == "comparison" or len(content) > 6:
            return 3  # Two content layout for complex content
        elif slide_type == "title_only":
            return 5  # Title only
        else:
            return 1  # Default: Title and content
    
    @staticmethod
    def should_split_content(content: list, max_bullets: int = 6) -> bool:
        """Determine if content should be split across multiple slides"""
        return len(content) > max_bullets
    
    @staticmethod
    def split_content(content: list, max_bullets: int = 6) -> list:
        """Split content into multiple chunks for separate slides"""
        chunks = []
        for i in range(0, len(content), max_bullets):
            chunks.append(content[i:i + max_bullets])
        return chunks 