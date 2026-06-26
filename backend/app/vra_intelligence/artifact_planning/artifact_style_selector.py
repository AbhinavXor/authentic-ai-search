"""
=========================================================
MODULE: Artifact Style Selector
=========================================================
"""

from typing import Any, Dict


class ArtifactStyleSelector:

    def select(
        self,
        query: str
    ) -> Dict[str, Any]:

        query_lower = query.lower()

        style = "standard"

        if "professional" in query_lower:
            style = "professional"

        elif "corporate" in query_lower:
            style = "corporate"

        elif "academic" in query_lower:
            style = "academic"

        elif "simple" in query_lower:
            style = "simple"

        elif "colorful" in query_lower:
            style = "colorful"

        elif "executive" in query_lower:
            style = "executive"

        return {
            "artifact_style": style
        }