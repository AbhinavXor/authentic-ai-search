"""
=========================================================
MODULE: Emotion Plan Builder

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Build emotional response plan.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Dict, Any

from backend.app.vra_intelligence.emotion.emotion_detector import (
    EmotionDetector
)

from backend.app.vra_intelligence.emotion.tone_selector import (
    ToneSelector
)


class EmotionPlanBuilder:

    def __init__(self) -> None:

        self.emotion_detector = (
            EmotionDetector()
        )

        self.tone_selector = (
            ToneSelector()
        )

    def build(
        self,
        query: str
    ) -> Dict[str, Any]:

        emotion_result = (
            self.emotion_detector.detect(
                query
            )
        )

        tone_result = (
            self.tone_selector.select(
                emotion_result
            )
        )

        return {
            "primary_emotion":
            emotion_result.get(
                "primary_emotion"
            ),

            "detected_emotions":
            emotion_result.get(
                "detected_emotions",
                []
            ),

            "tone":
            tone_result.get(
                "tone"
            )
        }