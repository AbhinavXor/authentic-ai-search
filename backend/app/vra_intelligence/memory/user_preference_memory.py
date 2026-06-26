"""
=========================================================
MODULE: User Preference Memory
=========================================================
"""

from typing import Any, Dict


class UserPreferenceMemory:

    def __init__(self) -> None:
        self.preferences: Dict[str, Any] = {}

    def set_preference(
        self,
        key: str,
        value: Any
    ) -> None:

        self.preferences[key] = value

    def get_preference(
        self,
        key: str,
        default: Any = None
    ) -> Any:

        return self.preferences.get(
            key,
            default
        )

    def get_all(
        self
    ) -> Dict[str, Any]:

        return self.preferences