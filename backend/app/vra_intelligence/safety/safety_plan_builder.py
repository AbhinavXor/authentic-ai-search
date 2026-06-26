"""
=========================================================
MODULE: Safety Plan Builder
=========================================================
"""

from typing import Dict, Any

from backend.app.vra_intelligence.safety.safety_intent_detector import (
    SafetyIntentDetector
)

from backend.app.vra_intelligence.safety.sensitive_topic_detector import (
    SensitiveTopicDetector
)

from backend.app.vra_intelligence.safety.output_safety_planner import (
    OutputSafetyPlanner
)


class SafetyPlanBuilder:

    def __init__(self) -> None:

        self.intent_detector = (
            SafetyIntentDetector()
        )

        self.topic_detector = (
            SensitiveTopicDetector()
        )

        self.output_planner = (
            OutputSafetyPlanner()
        )

    def build(
        self,
        query: str
    ) -> Dict[str, Any]:

        safety_result = (
            self.intent_detector.detect(
                query
            )
        )

        sensitive_result = (
            self.topic_detector.detect(
                query
            )
        )

        output_plan = (
            self.output_planner.build(
                safety_result,
                sensitive_result
            )
        )

        return {

            "safety_result":
            safety_result,

            "sensitive_result":
            sensitive_result,

            "output_plan":
            output_plan
        }