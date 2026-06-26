"""
=========================================================
SCRIPT: Test Source Registry Loader

Project:
Authentic AI Search

Purpose:
Test whether the VRA Source Registry Loader
can correctly read trusted source JSON files.

How to run:
python3 scripts/test_source_registry_loader.py

Author:
Abhinav

Version:
0.1.0
=========================================================
"""

import sys
from pathlib import Path


# Add backend/app to Python import path.
# This allows this script to import VRA modules.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_APP_PATH = PROJECT_ROOT / "backend" / "app"

sys.path.append(str(BACKEND_APP_PATH))


from vra.source_selection.source_registry_loader import SourceRegistryLoader


def main() -> None:
    """
    Run source registry loader test.
    """

    loader = SourceRegistryLoader(
        registry_root=str(PROJECT_ROOT / "source_registry")
    )

    sources = loader.load_all_sources()

    print("=" * 60)
    print("VRA SOURCE REGISTRY LOADER TEST")
    print("=" * 60)

    print(f"Total sources loaded: {len(sources)}")
    print()

    for source in sources:
        print(f"- {source.get('name')} | {source.get('domain')} | Score: {source.get('authority_score')}")


if __name__ == "__main__":
    main()