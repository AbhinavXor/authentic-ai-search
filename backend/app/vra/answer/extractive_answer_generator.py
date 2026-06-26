"""
=========================================================
MODULE: Extractive Answer Generator

Project:
Authentic AI Search

Purpose:
Generate fallback answers from verified evidence
without external APIs or LLM dependency.

Version:
2.0.0
=========================================================
"""

from typing import Any, Dict, List, Optional
import re

from backend.app.vra.answer.evidence_summarizer import EvidenceSummarizer
from backend.app.vra.answer.paragraph_composer import ParagraphComposer


class ExtractiveAnswerGenerator:
    """
    Clean local fallback answer generator.

    Flow:
    verified evidence
        -> EvidenceSummarizer
        -> ParagraphComposer
        -> citation markers
        -> final answer
    """

    DEFAULT_MAX_FACTS = 5

    def __init__(self) -> None:
        self.evidence_summarizer = EvidenceSummarizer()
        self.paragraph_composer = ParagraphComposer()

    def _safe_text(self, value: Any) -> str:
        if value is None:
            return ""

        return str(value).strip()

    def _answer_depth(
        self,
        answer_plan: Optional[Dict[str, Any]],
    ) -> str:
        answer_plan = answer_plan or {}

        depth = self._safe_text(
            answer_plan.get("answer_depth") or "normal"
        )

        if depth not in {"normal", "detailed", "research"}:
            return "normal"

        return depth

    def _max_facts_from_plan(
        self,
        answer_plan: Optional[Dict[str, Any]],
    ) -> int:
        answer_plan = answer_plan or {}

        try:
            max_claims = int(
                answer_plan.get("max_claims") or 0
            )

            if max_claims > 0:
                return max(1, min(max_claims, 12))

        except Exception:
            pass

        depth = self._answer_depth(answer_plan)

        if depth == "research":
            return 10

        if depth == "detailed":
            return 7

        return self.DEFAULT_MAX_FACTS

    def _clean_answer(self, answer: str) -> str:
        answer = self._safe_text(answer)
        answer = re.sub(r"\s+\n", "\n", answer)
        answer = re.sub(r"\n\s+", "\n", answer)
        answer = re.sub(r"\n{3,}", "\n\n", answer)
        answer = answer.replace(" ,", ",")
        answer = answer.replace(" .", ".")
        answer = answer.strip()

        return answer

    def _ensure_period(self, text: str) -> str:
        text = self._safe_text(text).strip()

        if not text:
            return ""

        if text.endswith((".", "?", "!", ":")):
            return text

        return text + "."

    def _is_heading(self, text: str) -> bool:
        clean = text.strip()

        headings = {
            "Overview",
            "Key Information",
            "Verified Information",
            "Verified comparison context",
            "Key signals:",
            "Definition",
            "Summary",
        }

        return clean in headings

    def _add_citation_markers(
        self,
        answer: str,
    ) -> str:
        """
        Adds simple local citation markers like [1], [2].
        Frontend/citation engine can later map them to real source cards.
        """

        answer = self._clean_answer(answer)

        if not answer:
            return answer

        paragraphs = [
            paragraph.strip()
            for paragraph in answer.split("\n\n")
            if paragraph.strip()
        ]

        cited_paragraphs = []
        citation_index = 1

        for paragraph in paragraphs:
            if self._is_heading(paragraph):
                cited_paragraphs.append(paragraph)
                continue

            lines = [
                line.strip()
                for line in paragraph.split("\n")
                if line.strip()
            ]

            cited_lines = []

            for line in lines:
                is_bullet = line.startswith("- ")
                content = line[2:].strip() if is_bullet else line

                if self._is_heading(content):
                    cited_lines.append(line)
                    continue

                content = self._ensure_period(content)

                if not re.search(r"\[\d+\]\.?$", content):
                    content = f"{content} [{citation_index}]"
                    citation_index += 1

                if is_bullet:
                    content = f"- {content}"

                cited_lines.append(content)

            cited_paragraphs.append("\n".join(cited_lines))

        return "\n\n".join(cited_paragraphs)

    def _fallback_from_consensus(
        self,
        consensus_answer: str,
    ) -> str:
        consensus_answer = self._safe_text(consensus_answer)

        if not consensus_answer.strip():
            return ""

        return self._add_citation_markers(consensus_answer)

    def generate(
        self,
        query_text: str,
        evidence_records: List[Dict[str, Any]],
        consensus_answer: str = "",
        answer_plan: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        depth = self._answer_depth(answer_plan)
        max_facts = self._max_facts_from_plan(answer_plan)

        summary = self.evidence_summarizer.summarize(
            query_text=query_text,
            evidence_records=evidence_records,
            max_facts=max_facts,
        )

        fact_count = int(summary.get("fact_count", 0) or 0)

        if fact_count > 0:
            composed_answer = self.paragraph_composer.compose(
                query_type=summary.get("query_type", "general"),
                facts=summary.get("facts", []),
                answer_depth=depth,
            )

            answer = self._add_citation_markers(
                composed_answer
            )

            return {
                "answer": answer.strip(),
                "answer_mode": "extractive_fallback",
                "used_ai_reasoning": False,
                "is_personal_response": False,
                "evidence_based": True,
                "fallback_engine": "evidence_summarizer_composer",
                "answer_depth": depth,
                "claim_count_used": fact_count,
            }

        fallback_answer = self._fallback_from_consensus(
            consensus_answer
        )

        if not fallback_answer:
            fallback_answer = (
                "A clear answer could not be generated from the "
                "available verified evidence."
            )

        return {
            "answer": fallback_answer.strip(),
            "answer_mode": "extractive_fallback",
            "used_ai_reasoning": False,
            "is_personal_response": False,
            "evidence_based": False,
            "fallback_engine": "extractive_answer_generator_v2",
            "answer_depth": depth,
            "claim_count_used": 0,
        }