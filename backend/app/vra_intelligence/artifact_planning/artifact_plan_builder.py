"""
=========================================================
MODULE: Artifact Plan Builder
=========================================================
"""

from typing import Any, Dict

from backend.app.vra_intelligence.artifact_planning.artifact_request_detector import (
    ArtifactRequestDetector
)

from backend.app.vra_intelligence.artifact_planning.artifact_type_selector import (
    ArtifactTypeSelector
)

from backend.app.vra_intelligence.artifact_planning.artifact_style_selector import (
    ArtifactStyleSelector
)


class ArtifactPlanBuilder:

    def __init__(self) -> None:

        self.request_detector = ArtifactRequestDetector()
        self.type_selector = ArtifactTypeSelector()
        self.style_selector = ArtifactStyleSelector()

    def build(
        self,
        query: str
    ) -> Dict[str, Any]:

        request_result = self.request_detector.detect(
            query
        )

        type_result = self.type_selector.select(
            query
        )

        style_result = self.style_selector.select(
            query
        )

        return {
            "needs_artifact":
            request_result.get("needs_artifact", False),

            "matched_artifact_keywords":
            request_result.get("matched_artifact_keywords", []),

            "artifact_type":
            type_result.get("artifact_type", "none"),

            "artifact_style":
            style_result.get("artifact_style", "standard")
        }