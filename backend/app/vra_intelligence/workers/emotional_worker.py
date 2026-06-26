"""
=========================================================
MODULE: Emotional Worker

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Handle emotional context and tone adaptation.

Author:
Abhinav

Version:
2.1.0
=========================================================
"""

from typing import Any, Dict

from backend.app.vra_intelligence.workers.base_worker import (
    BaseWorker
)


class EmotionalWorker(BaseWorker):
    @property
    def worker_name(self) -> str:
        return "emotional_worker"

    def _detect_emotion(self, query: str) -> str:
        query_lower = query.lower()

        if any(word in query_lower for word in ["sad", "lonely", "upset", "depressed", "hurt"]):
            return "sad"

        if any(word in query_lower for word in ["angry", "frustrated", "annoyed", "mad"]):
            return "angry"

        if any(word in query_lower for word in ["confused", "unclear", "don't understand"]):
            return "confused"

        if any(word in query_lower for word in ["stress", "stressed", "anxious", "worried"]):
            return "anxious"

        if any(word in query_lower for word in ["happy", "excited", "great", "awesome"]):
            return "happy"

        return "neutral"

    def _tone_for_emotion(self, emotion: str) -> str:
        return {
            "sad": "empathetic",
            "angry": "calm",
            "confused": "educational",
            "anxious": "reassuring",
            "happy": "enthusiastic",
            "neutral": "professional"
        }.get(emotion, "professional")

    def _build_answer(self, query: str, emotion: str, tone: str) -> str:
        if emotion == "confused":
            return (
                "No worries — I’ll explain it simply. "
                "Statistics is the method of collecting, organizing, analyzing, and interpreting data. "
                "In simple words, it helps us understand numbers and make better decisions from them."
            )

        if emotion == "anxious":
            return (
                "I understand. Let’s take it step by step and keep it simple. "
                "You do not need to understand everything at once."
            )

        if emotion == "sad":
            return (
                "I’m sorry you’re feeling this way. I’ll respond gently and help you one step at a time."
            )

        return (
            "I’ll adjust the response tone to be "
            f"{tone} and helpful for your situation."
        )

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        query = context.get("query", "")
        existing_answer = context.get("answer", "")

        emotion = self._detect_emotion(query)
        tone = self._tone_for_emotion(emotion)

        answer = existing_answer or self._build_answer(
            query=query,
            emotion=emotion,
            tone=tone
        )

        return {
            "worker": self.worker_name,
            "status": "completed",
            "query": query,
            "answer": answer,
            "emotion_detected": emotion,
            "recommended_tone": tone,
            "empathy_mode": emotion != "neutral",
            "tone_plan": {
                "tone": tone,
                "style": "human_supportive" if emotion != "neutral" else "professional_clear",
                "should_be_brief": emotion in {"angry", "anxious"},
                "should_explain_step_by_step": emotion == "confused"
            }
        }