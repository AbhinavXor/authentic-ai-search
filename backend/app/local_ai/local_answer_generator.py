"""
=========================================================
MODULE: Local Answer Generator

Project:
Authentic AI Search

Purpose:
Generate answers using local LLMs with VRA evidence.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from typing import Any, Dict, List

from backend.app.local_ai.ollama_client import (
    OllamaClient
)


class LocalAnswerGenerator:
    """
    Local LLM answer generator.
    """

    def __init__(
        self,
        model: str = "qwen2.5:7b"
    ) -> None:
        self.model = model
        self.client = OllamaClient()

    def _build_evidence_text(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> str:
        """
        Build compact evidence text.
        """

        chunks = []

        for index, record in enumerate(
            evidence_records,
            start=1
        ):
            if record.get("retrieval_status") != "success":
                continue

            chunks.append(
                f"""
Evidence {index}
Source: {record.get("source_name")}
Domain: {record.get("domain")}
Claim: {record.get("extracted_claim")}
Evidence: {record.get("compressed_evidence") or record.get("page_text") or ""}
"""
            )

        return "\n".join(chunks).strip()

    def generate(
        self,
        query: str,
        evidence_records: List[Dict[str, Any]],
        fallback_answer: str = ""
    ) -> Dict[str, Any]:
        """
        Generate local answer.
        """

        evidence_text = self._build_evidence_text(
            evidence_records
        )

        if not evidence_text:
            return {
                "status": "failed",
                "answer": fallback_answer,
                "error": "No verified evidence available"
            }

        prompt = f"""
You are Authentic AI local answer writer.

Rules:
- Answer in the same language as the user.
- Use only verified evidence.
- Do not invent facts.
- If evidence is limited, say it clearly.
- Keep answer helpful and natural.

User question:
{query}

Verified evidence:
{evidence_text}

Write final answer:
"""

        result = self.client.generate(
            model=self.model,
            prompt=prompt
        )

        if result.get("status") != "success":
            return {
                "status": "failed",
                "answer": fallback_answer,
                "error": result.get("error")
            }

        return {
            "status": "success",
            "answer": result.get("text"),
            "error": None
        }