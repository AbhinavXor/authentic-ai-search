"""
=========================================================
MODULE: Paragraph Composer

Project:
Authentic AI Search

Purpose:
Convert verified facts into natural human readable answers.

Version:
1.0.0
=========================================================
"""

from typing import Dict, List


class ParagraphComposer:

    def compose(
        self,
        query_type: str,
        facts: List[Dict],
        answer_depth: str = "normal",
    ) -> str:

        if not facts:
            return (
                "A clear verified answer could not be generated from the "
                "available evidence."
            )

        texts = [
            fact["fact"]
            for fact in facts
            if fact.get("fact")
        ]

        if query_type == "definition":
            return self._definition(texts, answer_depth)

        if query_type == "entity":
            return self._entity(texts, answer_depth)

        if query_type == "opinion":
            return self._opinion(texts, answer_depth)

        if query_type == "comparison":
            return self._comparison(texts, answer_depth)

        return self._general(texts, answer_depth)

    # -----------------------------------------------------

    def _definition(
        self,
        facts,
        depth,
    ):
        if depth == "normal":
            return " ".join(facts[:2])

        if depth == "detailed":

            answer = facts[0]

            if len(facts) > 1:
                answer += "\n\n" + facts[1]

            if len(facts) > 2:
                answer += "\n\n" + facts[2]

            if len(facts) > 3:
                answer += "\n\n" + facts[3]

            return answer

        return (
            "Overview\n\n"
            + facts[0]
            + "\n\nKey Information\n\n"
            + "\n".join(
                "- " + f
                for f in facts[1:]
            )
        )

    # -----------------------------------------------------

    def _entity(
        self,
        facts,
        depth,
    ):
        if depth == "normal":
            return " ".join(facts[:2])

        if depth == "detailed":

            answer = facts[0]

            if len(facts) > 1:
                answer += "\n\n" + facts[1]

            if len(facts) > 2:
                answer += "\n\n" + facts[2]

            return answer

        return (
            facts[0]
            + "\n\nVerified Information\n\n"
            + "\n".join(
                "- " + x
                for x in facts[1:]
            )
        )

    # -----------------------------------------------------

    def _general(
        self,
        facts,
        depth,
    ):
        if depth == "normal":
            return " ".join(facts[:3])

        if depth == "detailed":
            return "\n\n".join(facts)

        return (
            "Verified Information\n\n"
            + "\n".join(
                "- " + x
                for x in facts
            )
        )

    # -----------------------------------------------------

    def _comparison(
        self,
        facts,
        depth,
    ):
        return self._general(
            facts,
            depth,
        )

    # -----------------------------------------------------

    def _opinion(
        self,
        facts,
        depth,
    ):
        intro = (
            "Based on verified sources, the available evidence suggests:\n\n"
        )

        if depth == "normal":
            return intro + " ".join(facts[:2])

        return intro + "\n\n".join(facts)