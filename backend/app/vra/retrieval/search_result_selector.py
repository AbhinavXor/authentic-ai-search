"""
=========================================================
MODULE: Search Result Selector

Project:
Authentic AI Search

Purpose:
Select best matching page for a query.

Author:
Abhinav

Version:
0.1.0
=========================================================
"""

from typing import Dict, List


class SearchResultSelector:
    """
    Select best result from search results.
    """

    def select_best_result(
        self,
        search_results: List[Dict]
    ) -> Dict:

        if not search_results:
            return {}

        return search_results[0]