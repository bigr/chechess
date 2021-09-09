from abc import ABC, abstractmethod

from chess import Board


class Evaluator(ABC):
    @abstractmethod
    def eval(self, board: Board) -> float:
        pass
