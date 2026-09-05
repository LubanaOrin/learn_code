import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "chess_capture_analyzer.py"
SPEC = importlib.util.spec_from_file_location("chess_capture_analyzer", MODULE_PATH)
chess = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(chess)


class ChessCaptureAnalyzerTest(unittest.TestCase):
    def test_validates_pieces_and_positions(self):
        self.assertTrue(chess.is_valid_piece("queen"))
        self.assertFalse(chess.is_valid_piece("dragon"))
        self.assertTrue(chess.is_valid_position("h8"))
        self.assertFalse(chess.is_valid_position("i9"))

    def test_prevents_occupied_squares(self):
        board = {}

        self.assertTrue(chess.add_piece(board, "rook", "e4"))
        self.assertFalse(chess.add_piece(board, "bishop", "e4"))
        self.assertEqual(board, {"e4": "rook"})

    def test_rook_captures_nearest_pieces_by_rank_and_file(self):
        board = {
            "e4": "rook",
            "e8": "bishop",
            "h4": "pawn",
            "e2": "queen",
            "a4": "knight",
            "e7": "pawn",
        }

        self.assertEqual(
            chess.get_capturable_pieces(board, "rook", "e4"),
            ["e7", "e2", "h4", "a4"],
        )

    def test_knight_captures_only_l_shaped_targets(self):
        board = {
            "d4": "knight",
            "b3": "pawn",
            "b5": "rook",
            "c6": "bishop",
            "e6": "queen",
            "d5": "king",
        }

        self.assertEqual(
            sorted(chess.get_capturable_pieces(board, "knight", "d4")),
            ["b3", "b5", "c6", "e6"],
        )

    def test_bishop_queen_king_and_pawn_capture_rules(self):
        bishop_board = {"c1": "bishop", "f4": "pawn", "a3": "rook"}
        queen_board = {"d4": "queen", "d8": "rook", "h4": "bishop", "a1": "pawn"}
        king_board = {"e4": "king", "e5": "pawn", "f5": "rook", "g6": "queen"}
        pawn_board = {"e4": "pawn", "d5": "bishop", "f5": "knight", "e5": "rook"}

        self.assertEqual(
            sorted(chess.get_capturable_pieces(bishop_board, "bishop", "c1")),
            ["a3", "f4"],
        )
        self.assertEqual(
            sorted(chess.get_capturable_pieces(queen_board, "queen", "d4")),
            ["a1", "d8", "h4"],
        )
        self.assertEqual(
            sorted(chess.get_capturable_pieces(king_board, "king", "e4")),
            ["e5", "f5"],
        )
        self.assertEqual(
            sorted(chess.get_capturable_pieces(pawn_board, "pawn", "e4")),
            ["d5", "f5"],
        )


if __name__ == "__main__":
    unittest.main()
