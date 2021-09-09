from abc import ABC, abstractmethod
from typing import Optional, Sequence, Tuple

import numpy as np
from chess import Board

from chechess.eval import Evaluator
from chechess.move_generator import MoveGenerator
from chechess.table import TranspositionTable


class AlphaBetaSearchNodePhase(ABC):
    @abstractmethod
    def eval(
        self, searcher, board: Board, depth: int, alpha: float, beta: float
    ) -> Tuple[float, float, Optional[float]]:
        pass


class AlphaBetaSearcher(Evaluator):
    def __init__(
        self,
        depth: int,
        search_node_phases: Sequence[AlphaBetaSearchNodePhase],
        transposition_table: TranspositionTable,
    ):
        self.depth = depth
        self.search_node_phases = search_node_phases
        self.transposition_table = transposition_table

    def eval(self, board: Board) -> float:
        return self.search(board, self.depth, -np.inf, np.inf)

    def _store_to_transposition_table(
        self, board: Board, depth: int, value: float, alpha: float, beta: float
    ) -> None:
        tt_entry = self.transposition_table[board]
        if depth >= tt_entry["depth"]:
            tt_entry["depth"] = depth
            tt_entry["score"] = value
            if value < alpha:
                tt_entry["node_type"] = "all"
            elif value >= beta:
                tt_entry["node_type"] = "cut"
            else:
                tt_entry["node_type"] = "pv"

    def search(self, board: Board, depth: int, alpha: float, beta: float) -> float:
        original_alpha, original_beta = alpha, beta
        value = -np.inf
        for search_stage in self.search_node_phases:
            alpha, beta, value = search_stage.eval(self, board, depth, alpha, beta)
            if alpha == beta:
                break
        self._store_to_transposition_table(board, depth, value, original_alpha, original_beta)

        return value


class TranspositionTableAlphaBetaSearchNodePhase(AlphaBetaSearchNodePhase):
    def __init__(self, transposition_table: TranspositionTable):
        self.transposition_table = transposition_table

    def eval(
        self, searcher: AlphaBetaSearcher, board: Board, depth: int, alpha: float, beta: float
    ) -> Tuple[float, float, Optional[float]]:
        tt_entry = self.transposition_table[board]
        if tt_entry.get("depth", -1) >= depth:
            if tt_entry["node_type"] == "pv":
                alpha, beta = tt_entry["score"], tt_entry["score"]
            elif tt_entry["node_type"] == "all":
                beta = min(beta, tt_entry["score"])
            elif tt_entry["node_type"] == "cut":
                alpha = max(alpha, tt_entry["score"])

            if alpha >= beta:
                return tt_entry["score"], tt_entry["score"], tt_entry["score"]

        return alpha, beta, None


class GameOverAlphaBetaSearchNodePhase(AlphaBetaSearchNodePhase):
    def eval(
        self, searcher: AlphaBetaSearcher, board: Board, depth: int, alpha: float, beta: float
    ) -> Tuple[float, float, Optional[float]]:
        outcome = board.outcome()
        if outcome is not None:
            if outcome.winner == board.turn:
                return np.inf, np.inf, np.inf
            elif outcome.winner is None:
                return 0.0, 0.0, 0.0
            else:
                return -np.inf, -np.inf, -np.inf
        return alpha, beta, None


class SimpleHorizonAlphaBetaSearchNodePhase(AlphaBetaSearchNodePhase):
    def __init__(self, horizon_evaluator: Evaluator):
        self.horizon_evaluator = horizon_evaluator

    def eval(
        self, searcher: AlphaBetaSearcher, board: Board, depth: int, alpha: float, beta: float
    ) -> Tuple[float, float, Optional[float]]:
        if not depth:
            value = self.horizon_evaluator.eval(board)
            return value, value, value
        else:
            return alpha, beta, None


class CoreAlphaBetaSearchNodePhase(AlphaBetaSearchNodePhase):
    def __init__(self, move_generator: MoveGenerator):
        self.move_generator = move_generator

    def eval(
        self, searcher: AlphaBetaSearcher, board: Board, depth: int, alpha: float, beta: float
    ) -> Tuple[float, float, Optional[float]]:
        value = -np.inf
        for move in self.move_generator.generate(board):
            try:
                board.push(move)
                value = max(value, -searcher.search(board, depth - 1, -beta, -alpha))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            finally:
                board.pop()

        return alpha, beta, value
