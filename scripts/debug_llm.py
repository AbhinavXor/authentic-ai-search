import sys

from pathlib import Path

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from backend.app.vra_intelligence.llm.local_llm_router import (
    LocalLLMRouter
)


router = LocalLLMRouter()

result = router.generate(
    query="What is Artificial Intelligence?",
    task_type="chat"
)

print(result)