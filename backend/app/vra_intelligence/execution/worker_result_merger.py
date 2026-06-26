"""
=========================================================
MODULE: Worker Result Merger

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Merge outputs from multiple VIAA workers into one
structured result.

Author:
Abhinav

Version:
2.0.0
=========================================================
"""

from typing import Any
from typing import Dict
from typing import List


class WorkerResultMerger:
    """
    Merge worker outputs.

    This merger prefers:
    1. Search / research answers
    2. Verified evidence
    3. Verification worker result
    4. Artifact / chart / code outputs
    """

    def _extract_successful_results(
        self,
        results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        successful_results = []

        for item in results:

            if item.get("status") != "success":
                continue

            result = item.get("result", {})

            if result.get("status") == "completed":
                successful_results.append(result)

        return successful_results

    def _find_primary_answer(
        self,
        successful_results: List[Dict[str, Any]]
    ) -> str:

        for result in successful_results:

            if result.get("research_answer"):
                return result.get("research_answer", "")

            if result.get("answer"):
                return result.get("answer", "")

        return ""

    def _collect_sources(
        self,
        successful_results: List[Dict[str, Any]]
    ) -> List[Any]:

        sources = []

        for result in successful_results:

            result_sources = result.get("sources", [])

            if result_sources:
                sources.extend(result_sources)

        return sources

    def _collect_citations(
        self,
        successful_results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        citations = []

        seen_urls = set()

        for result in successful_results:

            for citation in result.get("citations", []):

                url = citation.get("url")

                if url and url in seen_urls:
                    continue

                if url:
                    seen_urls.add(url)

                citations.append(citation)

        return citations

    def _collect_evidence_records(
        self,
        successful_results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        evidence_records = []

        for result in successful_results:

            records = result.get(
                "evidence_records",
                []
            )

            if records:
                evidence_records.extend(records)

        return evidence_records

    def _find_verification_result(
        self,
        successful_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        for result in successful_results:

            if result.get("worker") == "verification_worker":
                return result

        return {}

    def merge(
        self,
        results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        successful_results = (
            self._extract_successful_results(
                results
            )
        )

        answer = self._find_primary_answer(
            successful_results
        )

        sources = self._collect_sources(
            successful_results
        )

        citations = self._collect_citations(
            successful_results
        )

        evidence_records = self._collect_evidence_records(
            successful_results
        )

        verification_result = (
            self._find_verification_result(
                successful_results
            )
        )

        return {

            "status":
            "completed"
            if successful_results
            else "failed",

            "answer":
            answer,

            "sources":
            sources,

            "citations":
            citations,

            "evidence_records":
            evidence_records,

            "verification_result":
            verification_result,

            "worker_results":
            results,

            "successful_worker_count":
            len(successful_results),

            "total_worker_count":
            len(results)
        }