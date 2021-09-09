from abc import ABC, abstractmethod
from typing import Iterator

from chess import Board, Move


class MoveGenerator(ABC):
    @abstractmethod
    def generate(self, board: Board) -> Iterator[Move]:
        pass


class SimpleMoveGenerator(MoveGenerator):
    def generate(self, board: Board) -> Iterator[Move]:
        yield from board.legal_moves
