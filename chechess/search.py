from abc import ABC, abstractmethod
from typing import Optional, Tuple

from chess import Board


class AlphaBetaSearchNodePhase(ABC):
    @abstractmethod
    def eval(
        self, searcher, board: Board, depth: int, alpha: float, beta: float
    ) -> Tuple[float, float, Optional[float]]:
        pass
