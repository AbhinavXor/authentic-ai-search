"""
=========================================================
MODULE: Gemini Answer Generator

Project:
Authentic AI Search

Purpose:
Generate final answers using Gemini from VRA verified evidence.

Version:
2.1.0
=========================================================
"""

import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from google import genai


load_dotenv()


class GeminiAnswerGenerator:
    """
    Gemini-based final answer writer.

    Rules:
    - Gemini does not choose sources.
    - Gemini does not verify sources.
    - Gemini only writes from VRA-provided evidence.
    - Citations are handled by VRA/frontend, not invented by Gemini.
    """

    ANSWER_MODE_VERIFIED = "verified"
    ANSWER_MODE_AI_ASSISTED = "ai_assisted"
    ANSWER_MODE_PERSONAL_RESPONSE = "personal_response"

    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

        self.client: Optional[genai.Client] = None

        if self.api_key:
            self.client = genai.Client(
                api_key=self.api_key
            )

    def _safe_text(
        self,
        value: Any
    ) -> str:
        if value is None:
            return ""

        return str(value).strip()

    def _source_label(
        self,
        record: Dict[str, Any]
    ) -> str:
        return (
            self._safe_text(record.get("source_name"))
            or self._safe_text(record.get("page_title"))
            or self._safe_text(record.get("domain"))
            or "Unknown source"
        )

    def _is_personal_query(
        self,
        query_intent: str
    ) -> bool:
        return query_intent in {
            "health_support",
            "personal_support",
            "mental_health",
            "emotional_support",
            "relationship",
            "career_advice",
            "life_advice",
            "self_help",
            "motivation",
        }

    def _build_ai_fallback_prompt(
        self,
        query_text: str,
        answer_plan: Optional[Dict[str, Any]] = None
    ) -> str:
        answer_plan = answer_plan or {}

        answer_depth = answer_plan.get(
            "answer_depth",
            "normal"
        )

        style = answer_plan.get(
            "style",
            "general"
        )

        max_paragraphs = answer_plan.get(
            "max_paragraphs",
            3
        )

        return f"""
Answer the user naturally and helpfully.

Question:
{query_text}

Answer depth:
{answer_depth}

Style:
{style}

Maximum paragraphs:
{max_paragraphs}

Rules:
1. If the user is emotional, respond empathetically.
2. Do not claim the answer is verified.
3. If the answer depth is normal, keep it short and direct.
4. If the answer depth is detailed, explain with useful context.
5. If the answer depth is research, use clear structured sections.

Write answer:
"""

    def _fallback_answer(
        self,
        consensus_answer: str,
        query_text: str = ""
    ) -> str:
        consensus_answer = self._safe_text(consensus_answer)
        query_lower = self._safe_text(query_text).lower()

        if (
            "what do people think" in query_lower
            or "people think about" in query_lower
            or "opinions on" in query_lower
            or "public opinion" in query_lower
        ):
            return (
                "A reliable opinion summary could not be generated from the "
                "available verified evidence."
            )

        if (
            "rbi" in query_lower
            or "reserve bank of india" in query_lower
        ):
            return (
                "RBI stands for the Reserve Bank of India. "
                "It is the central bank of India."
            )

        if (
            "gdp" in query_lower
            or "gross domestic product" in query_lower
        ):
            return (
                "GDP stands for Gross Domestic Product. It measures the total "
                "value of final goods and services produced in an economy "
                "during a specific period."
            )

        if "inflation" in query_lower:
            return (
                "Inflation is a general increase in the prices of goods and "
                "services over time, which reduces the purchasing power of money."
            )

        if "mospi" in query_lower:
            return (
                "MOSPI stands for the Ministry of Statistics and Programme "
                "Implementation, Government of India."
            )

        if (
            "what is who" in query_lower
            or query_lower.strip() == "who"
        ):
            return "WHO stands for the World Health Organization."

        if "imf" in query_lower:
            return "IMF stands for the International Monetary Fund."

        if consensus_answer and len(consensus_answer) <= 350:
            return consensus_answer

        return (
            "A clear answer could not be generated from the available "
            "verified evidence."
        )

    def _generate_ai_answer(
        self,
        prompt: str,
        consensus_answer: str,
        query_text: str = ""
    ) -> str:
        if not self.client:
            return self._fallback_answer(
                consensus_answer,
                query_text
            )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "temperature": 0.15,
                "max_output_tokens": 900,
            },
        )

        answer_text = getattr(
            response,
            "text",
            None
        )

        if not answer_text:
            return self._fallback_answer(
                consensus_answer,
                query_text
            )

        return answer_text.strip()

    def _max_sources_from_plan(
        self,
        answer_plan: Optional[Dict[str, Any]]
    ) -> int:
        answer_plan = answer_plan or {}
        answer_depth = answer_plan.get("answer_depth", "normal")

        if answer_depth == "research":
            return 12

        if answer_depth == "detailed":
            return 10

        return 8

    def _build_evidence_text(
        self,
        evidence_records: List[Dict[str, Any]],
        answer_plan: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Build compact, safe evidence for Gemini.

        Important:
        - Do not pass full raw page text.
        - Use extracted claims and supporting claims only.
        """

        evidence_items = []

        max_sources = self._max_sources_from_plan(
            answer_plan
        )

        usable_records = [
            record
            for record in evidence_records
            if record.get("retrieval_status") == "success"
        ]

        usable_records = sorted(
            usable_records,
            key=lambda record: (
                float(record.get("rank_score", 0) or 0),
                float(record.get("authority_score", 0) or 0),
                float(record.get("relevance_score", 0) or 0),
            ),
            reverse=True
        )

        for index, record in enumerate(
            usable_records[:max_sources],
            start=1
        ):
            primary_claim = self._safe_text(
                record.get("primary_claim")
                or record.get("extracted_claim")
            )

            supporting_claims = record.get(
                "supporting_claims",
                []
            ) or []

            source_name = self._source_label(record)
            domain = self._safe_text(record.get("domain"))
            url = self._safe_text(record.get("source_url"))

            authority_score = record.get("authority_score", 0)
            rank_score = record.get("rank_score", 0)
            is_official = record.get("is_official", False)
            is_trusted = record.get("is_trusted", False)

            facts = []

            if primary_claim:
                facts.append(f"- {primary_claim}")

            for claim in supporting_claims[:3]:
                claim_text = self._safe_text(claim)

                if claim_text:
                    facts.append(f"- {claim_text}")

            if not facts:
                description = self._safe_text(
                    record.get("page_description")
                )

                if description:
                    facts.append(f"- {description}")

            if not facts:
                continue

            evidence_items.append(
                f"""
Evidence {index}
Source name: {source_name}
Domain: {domain}
URL: {url}
Official source: {is_official}
Trusted source: {is_trusted}
Authority score: {authority_score}
Rank score: {rank_score}
Allowed facts:
{chr(10).join(facts)}
"""
            )

        return "\n".join(evidence_items).strip()

    def _build_prompt(
        self,
        query_text: str,
        evidence_text: str,
        consensus_answer: str,
        answer_plan: Optional[Dict[str, Any]] = None
    ) -> str:
        answer_plan = answer_plan or {}

        answer_depth = answer_plan.get(
            "answer_depth",
            "normal"
        )

        style = answer_plan.get(
            "style",
            "general"
        )

        max_paragraphs = answer_plan.get(
            "max_paragraphs",
            3
        )

        return f"""
You are the final answer writer for Authentic AI Search.

Your job:
Write a helpful answer using ONLY the verified evidence below.

Strict rules:
1. Answer in the same language as the user's question.
2. Use only the facts explicitly present in the verified evidence.
3. Do not add facts from your own knowledge.
4. Do not invent numbers, dates, names, claims, or sources.
5. Do not mention scores, internal ranking, or internal pipeline details.
6. For each factual statement, append [[SOURCE]].
7. Only use citations where evidence exists.
8. If evidence is limited, briefly say the answer is based on limited verified evidence.
9. If evidence does not fully answer the question, say that clearly.
10. Do not use markdown tables.
11. Answer depth: {answer_depth}
12. Style: {style}
13. Maximum paragraphs: {max_paragraphs}
14. If answer depth is normal, keep the answer short and direct.
15. If answer depth is detailed, explain with useful context and enough detail.
16. If answer depth is research, use clear structured sections and fuller explanation.

User question:
{query_text}

Current consensus answer:
{consensus_answer}

Verified evidence:
{evidence_text}

Write the final answer:
"""

    def generate(
        self,
        query_text: str,
        evidence_records: List[Dict[str, Any]],
        consensus_answer: str,
        query_intent: str = "general_factual",
        allow_ai_fallback: bool = True,
        answer_plan: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate final answer using Gemini.

        Returns answer result payload.
        """

        usable_records = [
            record
            for record in evidence_records
            if record.get("retrieval_status") == "success"
        ]

        official_count = sum(
            1
            for record in usable_records
            if record.get("is_official")
        )

        trusted_count = sum(
            1
            for record in usable_records
            if record.get("is_trusted")
        )

        verified_support_count = sum(
            1
            for record in usable_records
            if record.get("can_support_verified_answer") is True
        )

        strong_verification = (
            official_count >= 1
            or trusted_count >= 2
            or verified_support_count >= 1
        )

        if (
            self._is_personal_query(query_intent)
            and len(usable_records) < 2
        ):
            fallback_prompt = self._build_ai_fallback_prompt(
                query_text=query_text,
                answer_plan=answer_plan,
            )

            try:
                generated_text = self._generate_ai_answer(
                    prompt=fallback_prompt,
                    consensus_answer=consensus_answer,
                    query_text=query_text,
                )

                return {
                    "answer": generated_text,
                    "answer_mode": self.ANSWER_MODE_PERSONAL_RESPONSE,
                    "used_ai_reasoning": True,
                    "is_personal_response": True,
                    "evidence_based": False,
                }

            except Exception as error:
                print(
                    "Gemini personal response generation failed:",
                    error
                )

                return {
                    "answer": self._fallback_answer(
                        consensus_answer,
                        query_text
                    ),
                    "answer_mode": self.ANSWER_MODE_PERSONAL_RESPONSE,
                    "used_ai_reasoning": True,
                    "is_personal_response": True,
                    "evidence_based": False,
                }

        evidence_text = self._build_evidence_text(
            evidence_records=evidence_records,
            answer_plan=answer_plan,
        )

        if (
            not evidence_text
            or not strong_verification
        ):
            if allow_ai_fallback:
                ai_prompt = self._build_ai_fallback_prompt(
                    query_text=query_text,
                    answer_plan=answer_plan,
                )

                try:
                    ai_answer = self._generate_ai_answer(
                        prompt=ai_prompt,
                        consensus_answer=consensus_answer,
                        query_text=query_text,
                    )

                    return {
                        "answer": ai_answer,
                        "answer_mode": self.ANSWER_MODE_AI_ASSISTED,
                        "used_ai_reasoning": True,
                        "is_personal_response": False,
                        "evidence_based": False,
                    }

                except Exception as error:
                    print(
                        "Gemini AI fallback generation failed:",
                        error
                    )

            return {
                "answer": self._fallback_answer(
                    consensus_answer,
                    query_text
                ),
                "answer_mode": self.ANSWER_MODE_AI_ASSISTED,
                "used_ai_reasoning": True,
                "is_personal_response": False,
                "evidence_based": False,
            }

        if not self.client:
            return {
                "answer": self._fallback_answer(
                    consensus_answer,
                    query_text
                ),
                "answer_mode": self.ANSWER_MODE_AI_ASSISTED,
                "used_ai_reasoning": True,
                "is_personal_response": False,
                "evidence_based": False,
            }

        prompt = self._build_prompt(
            query_text=query_text,
            evidence_text=evidence_text,
            consensus_answer=consensus_answer,
            answer_plan=answer_plan,
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "temperature": 0.15,
                    "max_output_tokens": 900,
                },
            )

            answer_text = getattr(
                response,
                "text",
                None
            )

            if not answer_text:
                return {
                    "answer": self._fallback_answer(
                        consensus_answer,
                        query_text
                    ),
                    "answer_mode": self.ANSWER_MODE_AI_ASSISTED,
                    "used_ai_reasoning": True,
                    "is_personal_response": False,
                    "evidence_based": False,
                }

            return {
                "answer": answer_text.strip(),
                "answer_mode": self.ANSWER_MODE_VERIFIED,
                "used_ai_reasoning": False,
                "is_personal_response": False,
                "evidence_based": True,
            }

        except Exception as error:
            print(
                "Gemini answer generation failed:",
                error
            )

            return {
                "answer": self._fallback_answer(
                    consensus_answer,
                    query_text
                ),
                "answer_mode": self.ANSWER_MODE_AI_ASSISTED,
                "used_ai_reasoning": True,
                "is_personal_response": False,
                "evidence_based": False,
            }