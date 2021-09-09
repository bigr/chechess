from abc import ABC, abstractmethod
from typing import Iterator

from chess import Board, Move


class MoveGenerator(ABC):
    @abstractmethod
    def generate(self, board: Board) -> Iterator[Move]:
        pass
