"""
=========================================================
MODULE: Visual Plan Builder

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Build visual output plan for frontend/artifact rendering.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict

from backend.app.vra_intelligence.visual_planning.chart_need_detector import (
    ChartNeedDetector
)

from backend.app.vra_intelligence.visual_planning.visual_type_selector import (
    VisualTypeSelector
)


class VisualPlanBuilder:
    """
    Builds visual response plan.
    """

    def __init__(self) -> None:
        self.chart_need_detector = ChartNeedDetector()
        self.visual_type_selector = VisualTypeSelector()

    def build(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Build visual plan.
        """

        need_result = self.chart_need_detector.detect(
            query
        )

        type_result = self.visual_type_selector.select(
            query
        )

        return {
            "needs_visual": need_result.get(
                "needs_visual",
                False
            ),
            "matched_visual_keywords": need_result.get(
                "matched_visual_keywords",
                []
            ),
            "visual_type": type_result.get(
                "visual_type",
                "none"
            )
        }