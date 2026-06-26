"""
=========================================================
MODULE: Task Classifier

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Classify user request into task types for VRA Intelligence
and VIAA worker allocation.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict, List


class TaskClassifier:
    """
    Classifies user query into one or more task types.

    This module is independent for now.
    It will be integrated into VIAA later.
    """

    def __init__(self) -> None:
        self.task_keywords = {
            "search": [
                "what is",
                "who is",
                "when",
                "where",
                "latest",
                "source",
                "verify",
                "fact"
            ],
            "research": [
                "research",
                "deep analysis",
                "analyze",
                "compare",
                "study",
                "report",
                "explain in detail"
            ],
            "pdf": [
                "pdf",
                "make pdf",
                "create pdf",
                "professional pdf",
                "report pdf"
            ],
            "ppt": [
                "ppt",
                "presentation",
                "slides",
                "pitch deck"
            ],
            "docx": [
                "docx",
                "document",
                "proposal",
                "write document"
            ],
            "chart": [
                "chart",
                "graph",
                "plot",
                "visualize",
                "trend",
                "bar chart",
                "pie chart"
            ],
            "image_analysis": [
                "image",
                "photo",
                "picture",
                "screenshot",
                "analyze this image",
                "read this image"
            ],
           "image_generation": [
                "generate",
               "generate image",
               "create image",
                "make image",
                 "make logo",
                  "logo",
                   "poster",
                  "banner",
                  "illustration",
                  "draw"
            ],
            "coding": [
                "code",
                "python",
                "javascript",
                "react",
                "fastapi",
                "debug",
                "error",
                "function",
                "class"
            ],
            "math_science": [
                "solve",
                "equation",
                "math",
                "physics",
                "chemistry",
                "formula",
                "derive",
                "calculate"
            ],
            "emotional": [
                "sad",
                "angry",
                "confused",
                "depressed",
                "stressed",
                "motivate",
                "feeling"
            ],
            "general_chat": [
                "hello",
                "hi",
                "thanks",
                "explain",
                "tell me"
            ]
        }

    def _match_keywords(
        self,
        query_lower: str,
        keywords: List[str]
    ) -> int:
        """
        Count keyword matches.
        """

        count = 0

        for keyword in keywords:
            if keyword in query_lower:
                count += 1

        return count

    def classify(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Classify query into task types.
        """

        query_lower = query.lower().strip()

        scores: Dict[str, int] = {}

        for task_type, keywords in self.task_keywords.items():
            score = self._match_keywords(
                query_lower=query_lower,
                keywords=keywords
            )

            scores[task_type] = score

        matched_tasks = [
            task
            for task, score in scores.items()
            if score > 0
        ]

        if not matched_tasks:
            matched_tasks = ["general_chat"]

        primary_task = max(
            scores,
            key=scores.get
        )

        if scores.get(primary_task, 0) == 0:
            primary_task = "general_chat"

        return {
            "primary_task": primary_task,
            "matched_tasks": matched_tasks,
            "task_scores": scores
        }