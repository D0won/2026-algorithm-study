import unittest

from davies_port import Davies10Python
from enhanced_ai import EnhancedDaviesAI
from hex_board import BLUE, RED, HexBoard


class HexTests(unittest.TestCase):
    def test_red_and_blue_wins(self):
        red = HexBoard()
        for r in range(11):
            red.play((r, 5), RED)
        self.assertTrue(red.has_won(RED))
        blue = HexBoard()
        for c in range(11):
            blue.play((4, c), BLUE)
        self.assertTrue(blue.has_won(BLUE))

    def test_plain_board_header_stays_fixed(self):
        rendered = HexBoard().render().splitlines()
        self.assertEqual(rendered[0], "   A B C D E F G H I J K")
        self.assertNotIn("-", "\n".join(rendered))
        self.assertNotIn("\\", "\n".join(rendered))

    def test_port_returns_legal_move_without_mutation(self):
        board = HexBoard()
        board.play((5, 5), RED)
        before = [row[:] for row in board.cells]
        move = Davies10Python().choose_move(board, BLUE)
        self.assertEqual(board.cells[move[0]][move[1]], 0)
        self.assertEqual(board.cells, before)

    def test_enhanced_takes_win(self):
        board = HexBoard()
        for r in range(10):
            board.play((r, 4), RED)
        move = EnhancedDaviesAI(0.1).choose_move(board, RED)
        board.play(move, RED)
        self.assertTrue(board.has_won(RED))

    def test_enhanced_blocks_loss(self):
        board = HexBoard()
        for c in range(11):
            if c != 5:
                board.play((3, c), BLUE)
        self.assertEqual(EnhancedDaviesAI(0.1).choose_move(board, RED), (3, 5))

    def test_timeout_does_not_mutate_board(self):
        board = HexBoard()
        board.play((5, 5), RED)
        before_cells = [row[:] for row in board.cells]
        before_history = board.history[:]
        EnhancedDaviesAI(0.02, max_depth=5).choose_move(board, BLUE)
        self.assertEqual(board.cells, before_cells)
        self.assertEqual(board.history, before_history)


if __name__ == "__main__":
    unittest.main()
