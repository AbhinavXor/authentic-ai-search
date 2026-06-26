"""
=========================================================
MODULE: Output Safety Planner
=========================================================
"""

from typing import Dict, Any


class OutputSafetyPlanner:

    def build(
        self,
        safety_result: Dict[str, Any],
        sensitive_result: Dict[str, Any]
    ) -> Dict[str, Any]:

        return {

            "allow_response":
            not safety_result.get(
                "unsafe_intent_detected",
                False
            ),

            "requires_warning":
            sensitive_result.get(
                "requires_extra_verification",
                False
            ),

            "requires_vra_verification":
            True
        }