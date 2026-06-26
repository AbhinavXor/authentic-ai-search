"""
=========================================================
MODULE: Emotion Detector

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Detect emotional context from user query.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Dict, Any


class EmotionDetector:

    def __init__(self) -> None:

        self.emotion_keywords = {

            "sad": [
                "sad",
                "upset",
                "hurt",
                "cry",
                "depressed",
                "lonely"
            ],

            "happy": [
                "happy",
                "excited",
                "great",
                "awesome",
                "joy"
            ],

            "angry": [
                "angry",
                "mad",
                "frustrated",
                "annoyed"
            ],

            "confused": [
                "confused",
                "don't understand",
                "unclear"
            ],

            "anxious": [
                "anxiety",
                "worried",
                "stress",
                "stressed",
                "nervous"
            ]
        }

    def detect(
        self,
        query: str
    ) -> Dict[str, Any]:

        query_lower = query.lower()

        detected_emotions = []

        for emotion, keywords in (
            self.emotion_keywords.items()
        ):

            for keyword in keywords:

                if keyword in query_lower:

                    detected_emotions.append(
                        emotion
                    )

                    break

        primary_emotion = (
            detected_emotions[0]
            if detected_emotions
            else "neutral"
        )

        return {
            "primary_emotion":
            primary_emotion,

            "detected_emotions":
            detected_emotions
        }