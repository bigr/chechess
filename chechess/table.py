from abc import ABC, abstractmethod
from collections import MutableMapping
from typing import Any

from chess import Board
from chess.polyglot import zobrist_hash


class TranspositionTable(ABC):
    @abstractmethod
    def __getitem__(self, k: Board) -> MutableMapping[str, Any]:
        pass


class DictTable(TranspositionTable):
    HASH_KEY = "__hash__"

    def __init__(self, table_capacity):
        self.data = {}
        self.capacity = table_capacity

    def __getitem__(self, board: Board) -> MutableMapping[str, Any]:
        board_full_hash = self._board_hash(board)
        board_short_hash = board_full_hash % self.capacity
        if (
            board_short_hash not in self.data
            or self.data[board_short_hash][self.HASH_KEY] != board_full_hash
        ):
            self.data[board_short_hash] = {self.HASH_KEY: board_full_hash}

        return self.data[board_short_hash]

    def _board_hash(self, board: Board) -> int:
        return zobrist_hash(board)
