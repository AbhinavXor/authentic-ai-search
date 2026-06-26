"""
=========================================================
SCRIPT: Test Source Selector

Purpose:
Test source selection based on registry category.

Run:
python3 scripts/test_source_selector.py
=========================================================
"""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_APP_PATH = PROJECT_ROOT / "backend" / "app"

sys.path.append(str(BACKEND_APP_PATH))


from vra.source_selection.source_registry_loader import SourceRegistryLoader
from vra.source_selection.source_selector import SourceSelector


def main() -> None:
    """
    Run source selector test.
    """

    loader = SourceRegistryLoader(
        registry_root=str(PROJECT_ROOT / "source_registry")
    )

    all_sources = loader.load_all_sources()

    selector = SourceSelector()

    selected_sources = selector.select_sources(
        sources=all_sources,
        category="government",
        limit=3
    )

    print("=" * 60)
    print("VRA SOURCE SELECTOR TEST")
    print("=" * 60)

    for source in selected_sources:
        print(
            f"{source.get('name')} | "
            f"{source.get('domain')} | "
            f"Authority: {source.get('authority_score')}"
        )


if __name__ == "__main__":
    main()