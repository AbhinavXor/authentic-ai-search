"""
=========================================================
MODULE: Sensitive Topic Detector
=========================================================
"""

from typing import Dict, Any


class SensitiveTopicDetector:

    def __init__(self) -> None:

        self.sensitive_topics = {

            "medical": [
                "medical",
                "disease",
                "treatment",
                "medicine"
            ],

            "legal": [
                "legal",
                "law",
                "court",
                "lawsuit"
            ],

            "financial": [
                "invest",
                "stock",
                "crypto",
                "financial"
            ],

            "political": [
                "election",
                "politics",
                "government"
            ]
        }

    def detect(
        self,
        query: str
    ) -> Dict[str, Any]:

        query_lower = query.lower()

        detected_topics = []

        for topic, keywords in (
            self.sensitive_topics.items()
        ):

            for keyword in keywords:

                if keyword in query_lower:

                    detected_topics.append(
                        topic
                    )

                    break

        return {

            "sensitive_topics":
            detected_topics,

            "requires_extra_verification":
            len(detected_topics) > 0
        }