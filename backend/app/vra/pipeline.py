"""
=========================================================
MODULE: VRA Pipeline

Project:
Authentic AI Search

Engine:
Verified Resource Algorithm (VRA)

Purpose:
Main orchestration layer for the VRA system.

Author:
Abhinav

Version:
3.0.0
=========================================================
"""

from pathlib import Path
from typing import Any, Dict, List

from backend.app.vra.types import UserQuery, AnswerResult, SourceInfo

from backend.app.search.free_search_provider import FreeSearchProvider
from backend.app.search.dynamic_source_builder import DynamicSourceBuilder

from backend.app.vra.intent.intent_detector import IntentDetector
from backend.app.vra.source_selection.source_registry_loader import SourceRegistryLoader
from backend.app.vra.source_selection.source_selector import SourceSelector
from backend.app.vra.query_retrieval.query_retriever import QueryRetriever
from backend.app.vra.retrieval.source_fetcher import SourceFetcher
from backend.app.vra.extraction.claim_extractor import ClaimExtractor
from backend.app.vra.consensus.consensus_engine import ConsensusEngine
from backend.app.vra.scoring.trust_score import TrustScoreEngine
from backend.app.vra.scoring.freshness_score import FreshnessScoreEngine
from backend.app.vra.reputation.reputation_engine import ReputationEngine
from backend.app.vra.evidence_graph.evidence_graph_builder import EvidenceGraphBuilder
from backend.app.vra.lineage.claim_lineage import ClaimLineageEngine
from backend.app.vra.ml.source_ranking_model import SourceRankingModel
from backend.app.vra.citations.citation_engine import CitationEngine
from backend.app.vra.guardrails.anti_hallucination import AntiHallucinationGuardrail
from backend.app.vra.answer.gemini_answer_generator import GeminiAnswerGenerator
from backend.app.vra.ml.hallucination_risk_model import HallucinationRiskModel
from backend.app.vra.ml.answer_quality_model import AnswerQualityModel
from backend.app.vra.ml.answer_safety_model import AnswerSafetyModel
from backend.app.vra.claim_similarity.claim_similarity_engine import ClaimSimilarityEngine
from backend.app.vra.contradiction.contradiction_detector import ContradictionDetector
from backend.app.vra.clustering.evidence_cluster_engine import EvidenceClusterEngine
from backend.app.vra.multihop.multihop_verifier import MultiHopVerifier
from backend.app.db.query_history_repository import save_query_history
from backend.app.vra.source_discovery.official_source_detector import OfficialSourceDetector
from backend.app.vra.source_discovery.source_discovery_ranker import SourceDiscoveryRanker

from backend.app.vra.answer.extractive_answer_generator import (
    ExtractiveAnswerGenerator
)

from backend.app.vra.answer.answer_length_planner import (
    AnswerLengthPlanner
)


class VRAPipeline:
    """
    Main VRA Pipeline Controller.
    """

    MAX_SEARCH_RESULTS = 80
    MAX_SELECTED_SOURCES = 20
    MAX_VERIFIED_EVIDENCE = 12

    PERSONAL_QUERY_TERMS = {
        "i am not feeling good",
        "i feel sad",
        "i am sad",
        "i feel lonely",
        "i am lonely",
        "i feel depressed",
        "i am depressed",
        "i feel anxious",
        "i am anxious",
        "i need help",
    }

    def __init__(self) -> None:
        self.project_root = Path(__file__).resolve().parents[3]

        self.intent_detector = IntentDetector()
        self.registry_loader = SourceRegistryLoader(
            registry_root=str(self.project_root / "source_registry")
        )
        self.source_selector = SourceSelector()
        self.query_retriever = QueryRetriever()
        self.source_fetcher = SourceFetcher()
        self.claim_extractor = ClaimExtractor()
        self.consensus_engine = ConsensusEngine()
        self.trust_score_engine = TrustScoreEngine()
        self.freshness_engine = FreshnessScoreEngine()
        self.reputation_engine = ReputationEngine()
        self.evidence_graph_builder = EvidenceGraphBuilder()
        self.lineage_engine = ClaimLineageEngine()
        self.source_ranking_model = SourceRankingModel()
        self.citation_engine = CitationEngine()
        self.guardrail = AntiHallucinationGuardrail()
        self.answer_generator = GeminiAnswerGenerator()
        self.extractive_answer_generator = ExtractiveAnswerGenerator()
        self.hallucination_model = HallucinationRiskModel()
        self.answer_length_planner = AnswerLengthPlanner()
        self.answer_quality_model = AnswerQualityModel()
        self.answer_safety_model = AnswerSafetyModel()
        self.free_search_provider = FreeSearchProvider()
        self.dynamic_source_builder = DynamicSourceBuilder()
        self.official_source_detector = OfficialSourceDetector()
        self.source_discovery_ranker = SourceDiscoveryRanker()
        self.claim_similarity_engine = ClaimSimilarityEngine()
        self.contradiction_detector = ContradictionDetector()
        self.evidence_cluster_engine = EvidenceClusterEngine()
        self.multi_hop_verifier = MultiHopVerifier()

        print("VRA Pipeline Initialized")

    def _is_personal_query(self, query_text: str) -> bool:
        query_lower = query_text.lower().strip()

        return any(term in query_lower for term in self.PERSONAL_QUERY_TERMS)

    def _safe_call(self, func, fallback, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            print(f"VRA safe call failed: {error}")
            return fallback

    def _build_verification_metadata(
        self,
        trust_score: float,
        confidence_score: float,
        consensus_status: str,
        verified_source_count: int,
        is_personal_response: bool = False,
    ) -> Dict[str, Any]:
        if is_personal_response:
            return {
                "answer_type": "personal_answer",
                "verification_status": "not_applicable",
                "verification_badge": None,
            }

        if verified_source_count <= 0:
            return {
                "answer_type": "unverified_answer",
                "verification_status": "unverified",
                "verification_badge": "❌ Unverified",
            }

        if (
            trust_score >= 90
            and verified_source_count >= 2
            and consensus_status != "contradiction_detected"
        ):
            return {
                "answer_type": "verified_answer",
                "verification_status": "verified",
                "verification_badge": "✅ Verified",
            }

        if (
           trust_score >= 50
           and consensus_status != "contradiction_detected"
        ):
            return {
                "answer_type": "partially_verified_answer",
                "verification_status": "partially_verified",
                "verification_badge": "⚠️ Partially Verified",
            }

        return {
            "answer_type": "unverified_answer",
            "verification_status": "unverified",
            "verification_badge": "❌ Unverified",
        }

    def _evaluate_freshness(self, record: Dict[str, Any]) -> Dict[str, Any]:
        return self._safe_call(
            self.freshness_engine.evaluate,
            {"freshness_score": 40.0, "freshness_status": "unknown"},
            record,
        )

    def _build_evidence_summary(
        self,
        evidence_records: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        evidence_summary = []

        for record in evidence_records:
            freshness_result = self._evaluate_freshness(record)

            evidence_summary.append(
                {
                    "source": record.get("source_name"),
                    "domain": record.get("domain"),
                    "status": (
                        "verified"
                        if record.get("retrieval_status") == "success"
                        else "failed"
                    ),
                    "claim": record.get("extracted_claim") or record.get("primary_claim"),
                    "url": record.get("source_url"),
                    "authority_score": record.get("authority_score", 0),
                    "rank_score": record.get("rank_score", 0),
                    "relevance_score": record.get("relevance_score", 0),
                    "official_confidence_score": record.get(
                        "official_confidence_score",
                        0,
                    ),
                    "is_official": record.get("is_official", False),
                    "is_trusted": record.get("is_trusted", False),
                    "source_risk_level": record.get("source_risk_level"),
                    "source_reliability_score": record.get(
                        "source_reliability_score",
                        0,
                    ),
                    "source_reliability_level": record.get(
                        "source_reliability_level",
                        "unknown",
                    ),
                    "freshness_score": freshness_result.get("freshness_score", 0),
                    "freshness_status": freshness_result.get(
                        "freshness_status",
                        "unknown",
                    ),
                    "error": record.get("error"),
                }
            )

        return evidence_summary

    def _select_sources(
        self,
        query: UserQuery,
        detected_category: str,
    ) -> List[Dict[str, Any]]:
        """
        Dynamic source discovery:
        user query -> internet search -> dynamic source builder -> official enrich
        -> discovery ranker -> top diverse sources.
        """

        search_results = self._safe_search(
            query_text=query.query_text,
            max_results=self.MAX_SEARCH_RESULTS,
        )

        dynamic_sources = self.dynamic_source_builder.build_sources(
            search_results=search_results,
            query_text=query.query_text,
        )

        enriched_sources = self.official_source_detector.enrich_sources(
            dynamic_sources
        )

        ranked_sources = self.source_discovery_ranker.rank(
            enriched_sources,
            max_sources=self.MAX_SELECTED_SOURCES,
        )

        if ranked_sources:
            return ranked_sources

        all_sources = self.registry_loader.load_all_sources()

        return self.source_selector.select_sources(
            sources=all_sources,
            category=detected_category,
            query_text=query.query_text,
            limit=5,
        )

    def _safe_search(
        self,
        query_text: str,
        max_results: int,
    ) -> List[Dict[str, Any]]:
        try:
            return self.free_search_provider.search(
                query_text=query_text,
                max_results=max_results,
                max_runtime_seconds=25,
            )
        except TypeError:
            return self.free_search_provider.search(
                query_text=query_text,
                max_results=max_results,
            )
        except Exception as error:
            print("Dynamic search failed:", error)
            return []

    def _extract_claims(
        self,
        evidence_records: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        if hasattr(self.claim_extractor, "extract_claims"):
            return self.claim_extractor.extract_claims(
                evidence_records=evidence_records
            )

        if hasattr(self.claim_extractor, "extract_batch"):
            return self.claim_extractor.extract_batch(evidence_records)

        return evidence_records

    def _filter_verified_evidence(
        self,
        evidence_records: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        successful_records = [
            record
            for record in evidence_records
            if record.get("retrieval_status") == "success"
        ]

        def is_bad_record(record):
            claim = (
                record.get("extracted_claim")
                or record.get("primary_claim")
                or record.get("page_description")
                or ""
            ).lower()
            if not claim:
                return True
            bad_phrases = [
                "placeholder solution",
                "headless browser",
                "challenge proof of work",
                "font rendering",
                "access denied",
                "enable javascript",
                "captcha",
                "robot check",
                "forbidden",
                "page not found",
                "mind-bogglingly large amount",
                "byproduct of supply-and-demand",
                "current estimated value of the uk",
                "world bank: data",
                "current us$",
            ]
            return any(phrase in claim for phrase in bad_phrases)

        successful_records = [
            record
            for record in successful_records
            if not is_bad_record(record)
        ]
        if not successful_records:
            return []

        verified_records = [
            record
            for record in successful_records
            if record.get("can_support_verified_answer") is True
            or record.get("is_official") is True
            or record.get("is_trusted") is True
            or float(record.get("authority_score", 0) or 0) >= 75
        ]

        if not verified_records:
            verified_records = [
                record
                for record in successful_records
                if (
                    record.get("extracted_claim")
                    and float(record.get("authority_score", 0) or 0) >= 50
                )
            ]

        if not verified_records:
            verified_records = [
                record
                for record in successful_records
                if record.get("extracted_claim")
            ]

        ranked_records = self.source_ranking_model.rank(verified_records)

        ranked_records = sorted(
            ranked_records,
            key=lambda record: (
                1 if record.get("extracted_claim") else 0,
                float(record.get("rank_score", 0) or 0),
                float(record.get("authority_score", 0) or 0),
                float(record.get("relevance_score", 0) or 0),
            ),
            reverse=True,
        )

        return ranked_records[: self.MAX_VERIFIED_EVIDENCE]

    def _build_sources(
        self,
        verified_sources: List[Dict[str, Any]],
    ) -> List[SourceInfo]:
        formatted_sources = []

        for record in verified_sources:
            freshness_result = self._evaluate_freshness(record)

            formatted_sources.append(
                SourceInfo(
                    title=record.get("source_name") or record.get("page_title") or "",
                    url=record.get("source_url") or "",
                    domain=record.get("domain") or "",
                    source_type=record.get("source_type") or "web",
                    authority_score=float(record.get("authority_score", 0) or 0),
                    freshness_score=float(
                        freshness_result.get("freshness_score", 0) or 0
                    ),
                    verified=record.get("can_support_verified_answer", False),
                    is_official=record.get("is_official", False),
                    is_trusted=record.get("is_trusted", False),
                    source_category=record.get("source_category") or "web",
                    authenticity_category=record.get("authenticity_category")
                    or "unknown",
                    discovery_score=float(record.get("discovery_score", 0) or 0),
                    reputation_score=float(record.get("reputation_score", 0) or 0),
                    retrieval_status=record.get("retrieval_status") or "unknown",
                )
            )

        return formatted_sources

    def _personal_answer(self, query: UserQuery) -> AnswerResult:
        answer_text = (
            "I’m sorry you’re feeling this way. Take a moment to breathe, drink some "
            "water, and try to sit somewhere safe and comfortable. If this feeling is "
            "strong, lasting, or you might hurt yourself, please contact someone you "
            "trust or local emergency support right now."
        )

        safety_result = self.answer_safety_model.evaluate(
            query_text=query.query_text,
            answer_text=answer_text,
        )

        return AnswerResult(
            answer=answer_text,
            trust_score=0.0,
            confidence_score=0.0,
            agreement_score=0.0,
            answer_quality_score=75.0,
            answer_quality_level="supportive",
            safety_score=safety_result.get("safety_score", 85.0),
            safety_level=safety_result.get("safety_level", "supportive_context"),
            matched_safety_keywords=safety_result.get(
                "matched_safety_keywords",
                [],
            ),
            hallucination_risk_score=0.0,
            hallucination_risk_level="low",
            consensus_status="not_applicable",
            claim_count=0,
            unique_claim_count=0,
            answer_type="personal_answer",
            verification_status="not_applicable",
            verification_badge=None,
            source_count=0,
            verified_source_count=0,
            failed_source_count=0,
            verification_summary="Verification badge is not applied to personal support answers.",
            sources=[],
            citations=[],
            source_cards=[],
            query_intent="personal_support",
            answer_mode="personal_assistant",
            is_personal_response=True,
            used_ai_reasoning=True,
            warning_message=None,
        )

    def process_query(self, query: UserQuery) -> AnswerResult:
        if self._is_personal_query(query.query_text):
            return self._personal_answer(query)

        detected_category = self.intent_detector.detect_category(
            query_text=query.query_text
        )

        query.category = detected_category

        selected_sources = self._select_sources(
            query=query,
            detected_category=detected_category,
        )

        search_records = self.query_retriever.build_search_queries(
            query_text=query.query_text,
            sources=selected_sources,
        )

        evidence_records = self.source_fetcher.fetch_from_search_records(
            query_text=query.query_text,
            search_records=search_records,
        )

        evidence_records = self._extract_claims(evidence_records)

        evidence_records = self._safe_call(
            self.reputation_engine.enrich_records,
            evidence_records,
            evidence_records,
        )

        for record in evidence_records:
            freshness_result = self._evaluate_freshness(record)
            record["freshness_score"] = freshness_result.get("freshness_score", 40)
            record["freshness_status"] = freshness_result.get(
                "freshness_status",
                "unknown",
            )

        verified_sources = self._filter_verified_evidence(evidence_records)

        failed_sources = [
            record
            for record in evidence_records
            if record.get("retrieval_status") != "success"
        ]

        source_count = len(evidence_records)
        verified_source_count = len(verified_sources)
        failed_source_count = len(failed_sources)

        evidence_summary = self._build_evidence_summary(verified_sources)

        consensus_result = self.consensus_engine.generate(
            evidence_records=verified_sources
        )

        agreement_score = float(consensus_result.get("agreement_score", 0.0) or 0.0)
        consensus_status = consensus_result.get("consensus_status", "unknown")
        claim_count = consensus_result.get("claim_count", 0)
        unique_claim_count = consensus_result.get("unique_claim_count", 0)
        consensus_answer = consensus_result.get("consensus") or ""

        answer_plan = self.answer_length_planner.plan(
          query_text=query.query_text,
        )

        claim_texts = [
            record.get("extracted_claim") or record.get("primary_claim")
            for record in verified_sources
            if record.get("extracted_claim") or record.get("primary_claim")
        ]

        contradiction_result = self.contradiction_detector.detect(claim_texts)

        if contradiction_result.get("contradiction"):
            consensus_status = "contradiction_detected"

        trust_score = self.trust_score_engine.calculate(
            evidence_records=verified_sources
        )

        confidence_score = min(trust_score, agreement_score)

        hallucination_result = self.hallucination_model.evaluate(
            trust_score=trust_score,
            agreement_score=agreement_score,
            source_count=verified_source_count,
        )

        citations = self.citation_engine.build(verified_sources)

        source_cards = self.citation_engine.build_source_cards(
            verified_sources
        )

        answer_result = self.answer_generator.generate(
           query_text=query.query_text,
           evidence_records=verified_sources,
           consensus_answer=consensus_answer,
           query_intent=detected_category,
        )

        answer_text_for_check = answer_result.get("answer", "") or ""
        answer_text_for_check_lower = answer_text_for_check.lower()

        weak_fallback_phrases = [
            "mind-bogglingly large amount",
            "byproduct of supply-and-demand",
            "clear answer could not be generated",
            "a verified answer could not be safely generated",
            "a clear answer could not be generated from the available verified evidence",
            "a reliable opinion summary could not be generated",
        ]

        should_try_extractive_fallback = (
            answer_result.get("answer_mode") == "ai_assisted"
            or answer_result.get("evidence_based") is False
            or any(
                phrase in answer_text_for_check_lower
                for phrase in weak_fallback_phrases
            )
        )

        if should_try_extractive_fallback:
            extractive_result = self.extractive_answer_generator.generate(
                query_text=query.query_text,
                evidence_records=verified_sources,
                consensus_answer=consensus_answer,
                answer_plan=answer_plan,
            )

            extractive_answer = extractive_result.get("answer", "") or ""
            extractive_answer_lower = extractive_answer.lower()

            if (
                int(extractive_result.get("claim_count_used", 0) or 0) > 0
                and extractive_answer.strip()
                and "clear answer could not be generated"
                not in extractive_answer_lower
            ):
                answer_result = extractive_result

        answer_text = answer_result.get("answer", "")

        answer_mode = answer_result.get(
            "answer_mode",
            "verified_search"
        )

        used_ai_reasoning = answer_result.get(
            "used_ai_reasoning",
            True
        )

        is_personal_response = answer_result.get(
            "is_personal_response",
            False
        )
        if not answer_text:
            answer_text = (
                consensus_answer
                or "A clear verified answer could not be generated."
        )
        safety_result = self.answer_safety_model.evaluate(
            query_text=query.query_text,
            answer_text=answer_text,
        )

        try:
            answer_quality_result = self.answer_quality_model.evaluate(
                answer_text=answer_text,
                evidence_records=verified_sources,
                citation_count=len(citations),
            )
            answer_quality_score = answer_quality_result.get(
                "quality_score",
                answer_quality_result.get("answer_quality_score", 0),
            )
            answer_quality_level = answer_quality_result.get(
                "quality_level",
                answer_quality_result.get("answer_quality_level", "unknown"),
            )
        except TypeError:
            answer_quality_result = self.answer_quality_model.evaluate(
                trust_score=trust_score,
                agreement_score=agreement_score,
                hallucination_risk_score=hallucination_result.get(
                    "hallucination_risk_score",
                    0,
                ),
                citation_count=len(citations),
                verified_source_count=verified_source_count,
                claim_count=claim_count,
            )
            answer_quality_score = answer_quality_result.get(
                "answer_quality_score",
                0,
            )
            answer_quality_level = answer_quality_result.get(
                "answer_quality_level",
                "unknown",
            )

        verification_metadata = self._build_verification_metadata(
            trust_score=trust_score,
            confidence_score=confidence_score,
            consensus_status=consensus_status,
            verified_source_count=verified_source_count,
        )

        if answer_mode == "personal_response":
            verification_metadata = {
                "answer_type": "personal_answer",
                "verification_status": "not_applicable",
                "verification_badge": None,
            }

        elif answer_mode == "extractive_fallback":
            if (
                verified_source_count >= 1
                and trust_score >= 50
                and consensus_status != "contradiction_detected"
            ):
                verification_metadata = {
                    "answer_type": "source_verified_fallback_answer",
                    "verification_status": "partially_verified",
                    "verification_badge": "⚠️ Partially Verified",
                }

        elif answer_mode == "ai_assisted":
            if (
                verified_source_count >= 2
                and trust_score >= 80
                and consensus_status != "contradiction_detected"
            ):
                verification_metadata = {
                    "answer_type": "source_verified_fallback_answer",
                    "verification_status": "partially_verified",
                    "verification_badge": "⚠️ Partially Verified",
                }
            else:
                verification_metadata = {
                    "answer_type": "ai_assisted_answer",
                    "verification_status": "not_verified",
                    "verification_badge": None,
                }
        guardrail_result = self.guardrail.evaluate(
            trust_score=trust_score,
            agreement_score=agreement_score,
            consensus_status=consensus_status,
            verified_sources=verified_sources,
            answer_text=answer_text,
            query_intent=detected_category,
        )

        if answer_mode in {"ai_assisted", "personal_response", "extractive_fallback"}:
            guardrail_result = {
              "allowed": True,
              "reason": None,
            }

        warning_message = None

        if not guardrail_result.get("allowed"):
            answer_text = "A verified answer could not be safely generated."
            verification_metadata = {
                "answer_type": "unverified_answer",
                "verification_status": "unverified",
                "verification_badge": "❌ Unverified",
            }
            warning_message = guardrail_result.get("reason")

        elif failed_sources:
            warning_message = (
                "Some sources could not be reached. The result is based on reachable verified sources."
            )

        if citations and answer_mode in {"verified", "extractive_fallback"}:
            answer_text = self.citation_engine.replace_citation_placeholders(
             answer_text=answer_text,
             citations=citations,
            )

            answer_text = self.citation_engine.attach_inline_citation_labels(
                answer_text=answer_text,
                citations=citations,
            )
        else:
            answer_text = self.citation_engine.replace_citation_placeholders(
                answer_text=answer_text,
                citations=[],
            )

        verification_summary = (
            f"Verified by {verified_source_count} trusted source(s)."
        )

        formatted_sources = self._build_sources(verified_sources)

        evidence_graph = self._safe_call(
            self.evidence_graph_builder.build,
            [],
            verified_sources,
        )

        claim_lineage = self._safe_call(
            self.lineage_engine.build,
            [],
            verified_sources,
        )

        claim_groups = consensus_result.get("claim_groups") or self._safe_call(
            self.claim_similarity_engine.group_claims,
            [],
            verified_sources,
        )

        evidence_clusters = self._safe_call(
            self.evidence_cluster_engine.build,
            [],
            verified_sources,
        )

        multi_hop_chains = self._safe_call(
            self.multi_hop_verifier.build,
            [],
            verified_sources,
        )

        ranked_sources = self.source_ranking_model.rank(verified_sources)

        save_query_history(
            query_text=query.query_text,
            answer=answer_text,
            trust_score=trust_score,
            verification_status=verification_metadata["verification_status"],
        )

        return AnswerResult(
            answer=answer_text,
            trust_score=trust_score,
            confidence_score=confidence_score,
            agreement_score=agreement_score,
            answer_quality_score=answer_quality_score,
            answer_quality_level=answer_quality_level,
            safety_score=safety_result.get("safety_score", 0),
            safety_level=safety_result.get("safety_level", "unknown"),
            matched_safety_keywords=safety_result.get(
                "matched_safety_keywords",
                [],
            ),
            hallucination_risk_score=hallucination_result.get(
                "hallucination_risk_score",
                0,
            ),
            hallucination_risk_level=hallucination_result.get(
                "hallucination_risk_level",
                "unknown",
            ),
            consensus_status=consensus_status,
            claim_count=claim_count,
            unique_claim_count=unique_claim_count,
            answer_type=verification_metadata["answer_type"],
            verification_status=verification_metadata["verification_status"],
            verification_badge=verification_metadata["verification_badge"],
            source_count=source_count,
            verified_source_count=verified_source_count,
            failed_source_count=failed_source_count,
            verification_summary=verification_summary,
            sources=formatted_sources,
            source_cards=source_cards,
            citations=citations,
            evidence_summary=evidence_summary,
            evidence_graph=evidence_graph,
            claim_lineage=claim_lineage,
            ranked_sources=ranked_sources,
            claim_groups=claim_groups,
            contradiction_result=contradiction_result,
            evidence_clusters=evidence_clusters,
            multi_hop_chains=multi_hop_chains,
            evidence_records=verified_sources,
            verified_sources=verified_sources,
            failed_sources=failed_sources,
            query_intent=detected_category,
            answer_mode=answer_mode,
            warning_message=warning_message,
            is_personal_response=is_personal_response,
            used_ai_reasoning=used_ai_reasoning,
        )
