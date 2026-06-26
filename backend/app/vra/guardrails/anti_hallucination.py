"""
=========================================================
MODULE: Anti Hallucination Guardrail
Version: 3.0.0
=========================================================
"""

from typing import Any, Dict, List


class AntiHallucinationGuardrail:
    def evaluate(
        self,
        trust_score: float,
        agreement_score: float,
        consensus_status: str,
        verified_sources: List[Dict[str, Any]],
        answer_text: str,
        query_intent: str = "general_factual",
    ) -> Dict[str, Any]:

        if query_intent in {
            "personal_support",
            "emotional_support",
            "health_support",
            "mental_health",
        }:
            return {"allowed": True, "reason": None}

        if not answer_text or not str(answer_text).strip():
            return {
                "allowed": False,
                "reason": "No answer text was generated.",
            }

        successful_sources = [
            s for s in verified_sources
            if s.get("retrieval_status") == "success"
        ]

        if not successful_sources:
            return {
                "allowed": False,
                "reason": "No verified source was available.",
            }

        if consensus_status == "contradiction_detected":
            return {
                "allowed": False,
                "reason": "Conflicting claims were detected across trusted sources.",
            }

        if trust_score < 45:
            return {
                "allowed": False,
                "reason": "Trust score is too low for a verified factual answer.",
            }

        return {"allowed": True, "reason": None}