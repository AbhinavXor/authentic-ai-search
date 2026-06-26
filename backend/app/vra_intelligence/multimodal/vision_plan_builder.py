"""
=========================================================
MODULE: Vision Plan Builder

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Build vision/OCR/image plan.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict


class VisionPlanBuilder:
    """
    Build vision execution plan.
    """

    def build(
        self,
        image_result: Dict[str, Any],
        document_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build vision plan.
        """

        needs_ocr = False
        needs_vision_model = False
        needs_document_parser = False

        if image_result.get("needs_image_analysis"):
            needs_ocr = True
            needs_vision_model = True

        if document_result.get("needs_document_analysis"):
            needs_document_parser = True

        return {
            "needs_ocr": needs_ocr,
            "needs_vision_model": needs_vision_model,
            "needs_document_parser": needs_document_parser,
            "preferred_local_tools": [
                "pytesseract",
                "paddleocr",
                "pymupdf",
                "pdfplumber"
            ],
            "api_fallback_chain": [
                "mistral_ocr",
                "gemini_vision",
                "openai_vision"
            ]
        }