"""
=========================================================
MODULE: Tone Selector

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Select response tone.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Dict, Any


class ToneSelector:

    def select(
        self,
        emotion_result: Dict[str, Any]
    ) -> Dict[str, Any]:

        emotion = emotion_result.get(
            "primary_emotion",
            "neutral"
        )

        tone = "professional"

        if emotion == "sad":
            tone = "empathetic"

        elif emotion == "happy":
            tone = "enthusiastic"

        elif emotion == "angry":
            tone = "calm"

        elif emotion == "confused":
            tone = "educational"

        elif emotion == "anxious":
            tone = "reassuring"

        return {
            "tone": tone
        }