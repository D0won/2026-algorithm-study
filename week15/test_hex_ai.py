import unittest
import time

from hex_ai import BLUE, RED, HexAI, get_best_move, has_won, move_to_notation, notation_to_move


class HexAITest(unittest.TestCase):
    def test_red_and_blue_win_detection(self):
        red = [
            [1, 0, 0],
            [1, 2, 0],
            [1, 2, 0],
        ]
        blue = [
            [2, 2, 2],
            [1, 1, 0],
            [0, 0, 0],
        ]
        self.assertTrue(has_won([x for row in red for x in row], 3, RED))
        self.assertTrue(has_won([x for row in blue for x in row], 3, BLUE))

    def test_takes_immediate_red_win(self):
        board = [
            [1, 0, 0],
            [1, 2, 0],
            [0, 2, 0],
        ]
        self.assertEqual((2, 0), get_best_move(board, RED, time_limit=0.02, seed=1))

    def test_blocks_immediate_blue_win(self):
        board = [
            [2, 2, 0],
            [1, 0, 0],
            [1, 0, 0],
        ]
        self.assertEqual((0, 2), get_best_move(board, RED, time_limit=0.02, seed=1))

    def test_never_returns_occupied_cell(self):
        board = [[0] * 5 for _ in range(5)]
        board[2][2] = RED
        move = HexAI(time_limit=0.05, seed=7).choose_move(board, BLUE)
        self.assertEqual(0, board[move[0]][move[1]])

    def test_notation_round_trip(self):
        self.assertEqual("f6", move_to_notation((5, 5)))
        self.assertEqual((5, 5), notation_to_move("f6"))
        self.assertEqual((9, 7), notation_to_move("h 10"))

    def test_finds_forced_bridge_response(self):
        # Red c3/e2 bridge has common carriers d2 and d3. Blue has just
        # occupied d2, so Red should preserve the bridge at d3.
        board = [[0] * 5 for _ in range(5)]
        board[2][2] = RED  # c3
        board[1][4] = RED  # e2
        board[1][3] = BLUE  # d2
        self.assertEqual((2, 3), get_best_move(board, RED, time_limit=0.02, seed=1))

    def test_blocks_single_gap_in_enemy_route(self):
        board = [
            [0, 0, 0, 0, 0],
            [2, 2, 0, 2, 2],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self.assertEqual((1, 2), get_best_move(board, RED, time_limit=0.02, seed=1))

    def test_time_limit_covers_preprocessing(self):
        board = [[0] * 11 for _ in range(11)]
        board[5][5] = RED
        started = time.perf_counter()
        HexAI(time_limit=0.10, seed=3).choose_move(board, BLUE)
        # Shared CI can be noisy, so allow a modest scheduling margin while
        # still catching the old "preprocessing + time_limit" behavior.
        self.assertLess(time.perf_counter() - started, 0.45)

    def test_davies_counter_book_blue_after_b5(self):
        board = [[0] * 11 for _ in range(11)]
        board[4][1] = RED  # b5 random opening
        self.assertEqual((0, 1), get_best_move(board, BLUE, time_limit=0.01, seed=1))  # b1

    def test_mohex_profile_uses_separate_opening_analysis(self):
        board = [[0] * 11 for _ in range(11)]
        board[4][1] = RED  # b5 random opening
        move = get_best_move(board, BLUE, time_limit=0.01, seed=1, book_profile="mohex")
        self.assertNotEqual((0, 1), move)  # Never leak the Davies-only reply.
        self.assertEqual(0, board[move[0]][move[1]])

    def test_davies_counter_book_red_after_k6_f6(self):
        board = [[0] * 11 for _ in range(11)]
        board[5][10] = RED  # k6 random opening
        board[5][5] = BLUE  # Davies response f6
        self.assertEqual((1, 6), get_best_move(board, RED, time_limit=0.01, seed=1))  # g2


if __name__ == "__main__":
    unittest.main()
