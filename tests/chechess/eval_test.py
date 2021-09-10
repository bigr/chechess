import chess
import pytest

from chechess.eval import MaterialEvaluator


@pytest.fixture
def piece_scores():
    return {
        chess.Piece(chess.PAWN, chess.WHITE): 1.0,
        chess.Piece(chess.PAWN, chess.BLACK): -1.0,
        chess.Piece(chess.KNIGHT, chess.WHITE): 3.0,
        chess.Piece(chess.KNIGHT, chess.BLACK): -3.0,
        chess.Piece(chess.BISHOP, chess.WHITE): 3.0,
        chess.Piece(chess.BISHOP, chess.BLACK): -3.0,
        chess.Piece(chess.ROOK, chess.WHITE): 5.0,
        chess.Piece(chess.ROOK, chess.BLACK): -5.0,
        chess.Piece(chess.QUEEN, chess.WHITE): 9.0,
        chess.Piece(chess.QUEEN, chess.BLACK): -9.0,
        chess.Piece(chess.KING, chess.WHITE): 0.0,
        chess.Piece(chess.KING, chess.BLACK): 0.0,
    }


@pytest.mark.parametrize(
    "board, expected",
    [
        (chess.Board(), 0.0),
        (chess.Board("8/8/2k2P2/5P2/1K6/8/8/8 w - - 0 1"), 2.0),
        (chess.Board("8/8/2k2P2/5PQ1/1K6/8/8/8 w - - 0 1"), 11.0),
        (
            chess.Board("3b2q1/2P1pP2/RPbr1p1N/1Pp3BK/3r1p1P/p1ppn1P1/PP1k3p/1Q3n2 w - - 0 1"),
            -11.0,
        ),
        (chess.Board("1n1Bk3/1p1pr1P1/1pP2pP1/b1PqPb2/2N2PrP/4Q3/RKp2Pp1/n7 w - - 0 1"), -9.0),
    ],
)
def test_material_evaluator_eval(piece_scores, board, expected):
    material_evaluator = MaterialEvaluator(piece_scores)

    actual = material_evaluator.eval(board)
    assert actual == expected

    actual = material_evaluator.eval(board.mirror())
    assert -actual == expected
