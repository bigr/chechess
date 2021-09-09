from abc import ABC, abstractmethod
from typing import Optional, Tuple, Sequence

import numpy as np

from chess import Board

from chechess.eval import Evaluator
from chechess.table import TranspositionTable


class AlphaBetaSearchNodePhase(ABC):
    @abstractmethod
    def eval(
        self, searcher, board: Board, depth: int, alpha: float, beta: float
    ) -> Tuple[float, float, Optional[float]]:
        pass


class AlphaBetaSearcher(Evaluator):
    def __init__(self, depth: int, search_node_phases: Sequence[AlphaBetaSearchNodePhase],
                 transposition_table: TranspositionTable):
        self.depth = depth
        self.search_node_phases = search_node_phases
        self.transposition_table = transposition_table

    def eval(self, board: Board) -> float:
        return self.search(board, self.depth, -np.inf, np.inf)

    def _store_to_transposition_table(self, board: Board, depth: int, value: float, alpha: float,
                                      beta: float):
        tt_entry = self.transposition_table[board]
        if depth >= tt_entry['depth']:
            tt_entry['depth'] = depth
            tt_entry['score'] = value
            if value < alpha:
                tt_entry['node_type'] = 'all'
            elif value >= beta:
                tt_entry['node_type'] = 'cut'
            else:
                tt_entry['node_type'] = 'pv'

    def search(self, board: Board, depth: int, alpha: float, beta: float) -> float:
        original_alpha, original_beta = alpha, beta
        value = None
        for search_stage in self.search_node_phases:
            alpha, beta, value = search_stage.eval(self, board, depth, alpha, beta)
            if alpha == beta:
                break
        self._store_to_transposition_table(board, depth, value, original_alpha, original_beta)

        return value
