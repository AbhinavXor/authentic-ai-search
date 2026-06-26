"""
=========================================================
MODULE: Authority Scorer

Project:
Authentic AI Search

Purpose:
Score website/domain authority automatically.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from urllib.parse import urlparse


class AuthorityScorer:
    """
    Scores source authority using domain rules.
    """

    HIGH_TRUST_DOMAINS = {
        "rbi.org.in": 98,
        "who.int": 98,
        "imf.org": 97,
        "worldbank.org": 97,
        "un.org": 97,
        "data.gov.in": 96,
        "mospi.gov.in": 98,
        "censusindia.gov.in": 99,
        "isro.gov.in": 97,
        "sebi.gov.in": 97,
        "openai.com": 95,
    }

    MEDIUM_TRUST_DOMAINS = {
        "wikipedia.org": 75,
        "en.wikipedia.org": 75,
        "britannica.com": 82,
        "investopedia.com": 78,
        "reuters.com": 85,
        "apnews.com": 85,
        "nature.com": 90,
        "sciencedirect.com": 88,
    }

    LOW_TRUST_DOMAINS = {
        "knittystash.com",
        "grokipedia.com",
        "dictionary.com",
        "quora.com",
        "reddit.com",
        "youtube.com",
    }

    def extract_domain(self, url: str) -> str:
        """
        Extract clean domain from URL.
        """

        if not url:
            return ""

        parsed = urlparse(url)

        return parsed.netloc.replace("www.", "").lower()

    def score_domain(self, domain: str) -> float:
        """
        Score domain authority from 0 to 100.
        """

        if not domain:
            return 0.0

        domain = domain.lower().replace("www.", "")

        if domain in self.HIGH_TRUST_DOMAINS:
            return float(self.HIGH_TRUST_DOMAINS[domain])

        if domain in self.MEDIUM_TRUST_DOMAINS:
            return float(self.MEDIUM_TRUST_DOMAINS[domain])

        if domain in self.LOW_TRUST_DOMAINS:
            return 25.0

        if domain.endswith(".gov") or domain.endswith(".gov.in"):
            return 95.0

        if domain.endswith(".edu") or domain.endswith(".ac.in"):
            return 88.0

        if domain.endswith(".int"):
            return 92.0

        if domain.endswith(".org"):
            return 65.0

        return 50.0

    def score_url(self, url: str) -> float:
        """
        Score authority directly from URL.
        """

        domain = self.extract_domain(url)

        return self.score_domain(domain)

    def is_official(self, domain: str) -> bool:
        """
        Decide if source is official/high authority.
        """

        return self.score_domain(domain) >= 90