"""
=========================================================
MODULE: Document Request Detector

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Detect document/file/PDF related requests.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict


class DocumentRequestDetector:
    """
    Detect document analysis requests.
    """

    def __init__(self) -> None:
        self.document_keywords = [
            "pdf",
            "document",
            "docx",
            "ppt",
            "presentation",
            "excel",
            "spreadsheet",
            "csv",
            "file",
            "upload",
            "summarize this",
            "analyze this file",
            "extract text"
        ]

    def detect(
        self,
        query: str,
        has_uploaded_file: bool = False
    ) -> Dict[str, Any]:
        """
        Detect document request.
        """

        query_lower = query.lower()

        matched_keywords = [
            keyword
            for keyword in self.document_keywords
            if keyword in query_lower
        ]

        return {
            "has_uploaded_file": has_uploaded_file,
            "needs_document_analysis": (
                has_uploaded_file
                or len(matched_keywords) > 0
            ),
            "document_matches": matched_keywords
        }