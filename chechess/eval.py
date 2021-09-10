from abc import ABC, abstractmethod
from typing import Mapping

import chess
from chess import Board


class Evaluator(ABC):
    @abstractmethod
    def eval(self, board: Board) -> float:
        pass


class MaterialEvaluator(Evaluator):
    def __init__(self, piece_scores: Mapping[chess.Piece, float]):
        self.piece_scores = piece_scores

    def eval(self, board: Board) -> float:
        return sum(
            score * len(board.pieces(piece.piece_type, piece.color))
            for piece, score in self.piece_scores.items()
        )
