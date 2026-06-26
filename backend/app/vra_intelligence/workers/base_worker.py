"""
=========================================================
MODULE: Base Worker

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Base class for all VIAA workers.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""

from abc import ABC
from abc import abstractmethod

from typing import Any
from typing import Dict


class BaseWorker(ABC):
    """
    Base worker interface.
    """

    @property
    @abstractmethod
    def worker_name(self) -> str:
        pass

    @abstractmethod
    def execute(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass