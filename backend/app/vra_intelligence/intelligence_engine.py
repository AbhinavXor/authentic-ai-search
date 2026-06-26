"""
=========================================================
MODULE: Intelligence Engine

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Build intelligence execution plan.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict

from backend.app.vra_intelligence.task_classifier import (
    TaskClassifier
)

from backend.app.vra_intelligence.complexity_analyzer import (
    ComplexityAnalyzer
)

from backend.app.vra_intelligence.worker_selector import (
    WorkerSelector
)

from backend.app.vra_intelligence.output_planner import (
    OutputPlanner
)


class IntelligenceEngine:
    """
    VRA Intelligence orchestrator.

    Future:
    - VIAA integration
    - Multi-worker execution
    - Local LLM routing
    - API fallback routing
    """

    def __init__(self) -> None:

        self.task_classifier = (
            TaskClassifier()
        )

        self.complexity_analyzer = (
            ComplexityAnalyzer()
        )

        self.worker_selector = (
            WorkerSelector()
        )

        self.output_planner = (
            OutputPlanner()
        )

    def analyze_query(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Create intelligence plan.
        """

        task_result = (
            self.task_classifier.classify(
                query=query
            )
        )

        complexity_result = (
            self.complexity_analyzer.analyze(
                query=query
            )
        )

        worker_result = (
            self.worker_selector.select(
                task_result=task_result,
                complexity_result=complexity_result
            )
        )

        output_plan = (
            self.output_planner.plan(
                task_result=task_result,
                complexity_result=complexity_result,
                worker_result=worker_result
            )
        )

        return {
            "query": query,
            "task_result": task_result,
            "complexity_result": complexity_result,
            "worker_result": worker_result,
            "output_plan": output_plan
        }