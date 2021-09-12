from abc import ABC, abstractmethod
from typing import Mapping, Optional, Sequence

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


class PieceSquareEvaluator(Evaluator):
    def __init__(self, piece_square_scores: Mapping[chess.Piece, Sequence[float]]):
        self.piece_square_scores = piece_square_scores

    def eval(self, board: Board) -> float:
        return sum(
            score_table[square]
            for piece, score_table in self.piece_square_scores.items()
            for square in board.pieces(piece.piece_type, piece.color)
        )


class MixEvaluator(Evaluator):
    def __init__(self, evaluators: Sequence[Evaluator], weights: Optional[Sequence[float]]):
        self.evaluators = evaluators
        self.weights = weights if weights else [1.0] * len(self.evaluators)

    def eval(self, board: Board) -> float:
        return sum(
            weight * evaluator.eval(board)
            for evaluator, weight in zip(self.evaluators, self.weights)
        )
