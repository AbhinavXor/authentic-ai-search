"""
=========================================================
MODULE: Image Request Detector

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Detect image-related user requests.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict


class ImageRequestDetector:
    """
    Detect image upload, image analysis, OCR,
    screenshot, and image generation intent.
    """

    def __init__(self) -> None:
        self.image_analysis_keywords = [
            "image",
            "photo",
            "picture",
            "screenshot",
            "analyze image",
            "read image",
            "what is in this image",
            "text from image",
            "ocr"
        ]

        self.image_generation_keywords = [
            "generate image",
            "create image",
            "make image",
            "logo",
            "poster",
            "banner",
            "illustration",
            "draw"
        ]

    def detect(
        self,
        query: str,
        has_uploaded_image: bool = False
    ) -> Dict[str, Any]:
        """
        Detect image request.
        """

        query_lower = query.lower()

        analysis_matches = [
            keyword
            for keyword in self.image_analysis_keywords
            if keyword in query_lower
        ]

        generation_matches = [
            keyword
            for keyword in self.image_generation_keywords
            if keyword in query_lower
        ]

        return {
            "has_uploaded_image": has_uploaded_image,
            "needs_image_analysis": (
                has_uploaded_image
                or len(analysis_matches) > 0
            ),
            "needs_image_generation": len(generation_matches) > 0,
            "image_analysis_matches": analysis_matches,
            "image_generation_matches": generation_matches
        }