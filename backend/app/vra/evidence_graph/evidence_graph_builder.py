from typing import Any, Dict, List


class EvidenceGraphBuilder:
    """
    Builds evidence graph from verified sources.
    """

    def build(
        self,
        evidence_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        graph = []

        for record in evidence_records:

            graph.append(
                {
                    "source": record.get("source_name"),
                    "domain": record.get("domain"),
                    "claim": record.get("extracted_claim"),
                    "authority_score": record.get(
                        "authority_score",
                        0
                    ),
                    "status": record.get(
                        "retrieval_status"
                    )
                }
            )

        return graph