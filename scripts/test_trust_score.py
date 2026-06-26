"""
=========================================================
SCRIPT: Test Trust Score Engine

Purpose:
Test VRA trust score calculation.

Run:
python3 scripts/test_trust_score.py
=========================================================
"""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_APP_PATH = PROJECT_ROOT / "backend" / "app"

sys.path.append(str(PROJECT_ROOT))


from backend.app.vra.source_selection.source_registry_loader import SourceRegistryLoader
from backend.app.vra.source_selection.source_selector import SourceSelector
from backend.app.vra.scoring.trust_score import TrustScoreEngine


def main() -> None:
    """
    Run trust score engine test.
    """

    loader = SourceRegistryLoader(
        registry_root=str(PROJECT_ROOT / "source_registry")
    )

    all_sources = loader.load_all_sources()

    selector = SourceSelector()

    selected_sources = selector.select_sources(
        sources=all_sources,
        category="government",
        limit=2
    )

    trust_engine = TrustScoreEngine()

    score = trust_engine.calculate(selected_sources)

    print("=" * 60)
    print("VRA TRUST SCORE TEST")
    print("=" * 60)
    print(f"Selected sources: {len(selected_sources)}")
    print(f"Final trust score: {score}")


if __name__ == "__main__":
    main()