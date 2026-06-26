"""
=========================================================
MODULE: Artifact Type Selector
=========================================================
"""

from typing import Any, Dict


class ArtifactTypeSelector:

    def select(
        self,
        query: str
    ) -> Dict[str, Any]:

        query_lower = query.lower()

        artifact_type = "none"

        if "pdf" in query_lower or "report" in query_lower:
            artifact_type = "pdf"

        elif "ppt" in query_lower or "presentation" in query_lower or "slides" in query_lower:
            artifact_type = "ppt"

        elif "docx" in query_lower or "document" in query_lower:
            artifact_type = "docx"

        elif "chart" in query_lower or "graph" in query_lower:
            artifact_type = "chart"

        elif "dashboard" in query_lower:
            artifact_type = "dashboard"

        elif "mindmap" in query_lower:
            artifact_type = "mindmap"

        elif "table" in query_lower:
            artifact_type = "table"

        return {
            "artifact_type": artifact_type
        }