"""
=========================================================
MODULE: Fetch Cache

Project:
Authentic AI Search

Engine:
VRA Search Engine

Purpose:
Simple file-based cache for fetched source content.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict, Optional


class FetchCache:
    """
    File-based cache for fetched URLs.

    This module is intentionally independent.
    It will be integrated into source_fetcher.py later.
    """

    def __init__(
        self,
        cache_dir: str = "data/cache/fetch",
        ttl_seconds: int = 86400
    ) -> None:
        self.cache_dir = Path(cache_dir)
        self.ttl_seconds = ttl_seconds

        self.cache_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def _hash_url(
        self,
        url: str
    ) -> str:
        """
        Create stable cache key for URL.
        """

        return hashlib.sha256(
            url.encode("utf-8")
        ).hexdigest()

    def _cache_path(
        self,
        url: str
    ) -> Path:
        """
        Return cache file path for URL.
        """

        cache_key = self._hash_url(url)

        return self.cache_dir / f"{cache_key}.json"

    def get(
        self,
        url: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get cached fetch result if valid.
        """

        path = self._cache_path(url)

        if not path.exists():
            return None

        try:
            with path.open(
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            created_at = float(
                data.get("created_at", 0)
            )

            age = time.time() - created_at

            if age > self.ttl_seconds:
                return None

            return data.get("payload")

        except Exception:
            return None

    def set(
        self,
        url: str,
        payload: Dict[str, Any]
    ) -> None:
        """
        Save fetch result to cache.
        """

        path = self._cache_path(url)

        data = {
            "url": url,
            "created_at": time.time(),
            "payload": payload
        }

        try:
            with path.open(
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

        except Exception:
            return

    def clear_expired(self) -> int:
        """
        Remove expired cache files.
        """

        removed_count = 0

        for path in self.cache_dir.glob("*.json"):
            try:
                with path.open(
                    "r",
                    encoding="utf-8"
                ) as file:
                    data = json.load(file)

                created_at = float(
                    data.get("created_at", 0)
                )

                if time.time() - created_at > self.ttl_seconds:
                    path.unlink()
                    removed_count += 1

            except Exception:
                continue

        return removed_count