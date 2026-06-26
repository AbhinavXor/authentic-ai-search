"""
=========================================================
MODULE: Visual Type Selector

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Select the most suitable visual output type.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict


class VisualTypeSelector:
    """
    Select visual type based on query.
    """

    def select(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Select visual type.
        """

        query_lower = query.lower()

        visual_type = "none"

        if "timeline" in query_lower:
            visual_type = "timeline"

        elif "pie" in query_lower:
            visual_type = "pie_chart"

        elif "bar" in query_lower:
            visual_type = "bar_chart"

        elif "line" in query_lower or "trend" in query_lower:
            visual_type = "line_chart"

        elif "scatter" in query_lower:
            visual_type = "scatter_chart"

        elif "compare" in query_lower or "comparison" in query_lower:
            visual_type = "comparison_table"

        elif "table" in query_lower:
            visual_type = "table"

        elif "dashboard" in query_lower:
            visual_type = "dashboard"

        elif "graph" in query_lower or "chart" in query_lower:
            visual_type = "auto_chart"

        return {
            "visual_type": visual_type
        }