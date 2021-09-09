from abc import ABC, abstractmethod
from collections import MutableMapping
from typing import Any

from chess import Board


class TranspositionTable(ABC):
    @abstractmethod
    def __getitem__(self, k: Board) -> MutableMapping[str, Any]:
        pass
