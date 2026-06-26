"""
=========================================================
MODULE: Safety Intent Detector

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Detect potentially unsafe intent.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Dict, Any


class SafetyIntentDetector:

    def __init__(self) -> None:

        self.high_risk_keywords = [

            "hack",
            "bypass",
            "exploit",
            "malware",
            "virus",
            "ddos",
            "phishing",
            "credential",
            "steal password",
            "ransomware"
        ]

    def detect(
        self,
        query: str
    ) -> Dict[str, Any]:

        query_lower = query.lower()

        matches = [

            keyword

            for keyword in self.high_risk_keywords

            if keyword in query_lower
        ]

        return {

            "unsafe_intent_detected":
            len(matches) > 0,

            "matched_keywords":
            matches
        }