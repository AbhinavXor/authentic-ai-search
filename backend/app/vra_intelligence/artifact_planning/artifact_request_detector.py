"""
=========================================================
MODULE: Artifact Request Detector
=========================================================
"""

from typing import Any, Dict


class ArtifactRequestDetector:

    def detect(
        self,
        query: str
    ) -> Dict[str, Any]:

        query_lower = query.lower()

        artifact_keywords = [
            "pdf",
            "ppt",
            "presentation",
            "slides",
            "docx",
            "document",
            "report",
            "chart",
            "graph",
            "dashboard",
            "mindmap",
            "table"
        ]

        matched_keywords = [
            keyword
            for keyword in artifact_keywords
            if keyword in query_lower
        ]

        return {
            "needs_artifact": len(matched_keywords) > 0,
            "matched_artifact_keywords": matched_keywords
        }