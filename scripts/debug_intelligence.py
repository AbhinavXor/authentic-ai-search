import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.vra_intelligence.intelligence_service import IntelligenceService


def test(query: str) -> None:
    service = IntelligenceService()
    result = service.process(query=query)

    print("\n==============================")
    print("QUERY:", query)
    print("ANSWER:", result.get("answer"))
    print("OUTPUT PLAN:", result.get("output_plan"))
    print("METRICS:", result.get("metrics"))


def main() -> None:
    queries = [
        "What is MOSPI?",
        "Create a professional PDF report on MOSPI",
        "Make a bar chart comparing India population data",
        "I am confused about statistics, explain it simply",
        "Write Python code for a calculator",
        "Generate a logo for Authentic AI"
    ]

    for query in queries:
        test(query)


if __name__ == "__main__":
    main()