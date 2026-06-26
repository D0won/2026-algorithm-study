"""Board rules for the 11x11 Hex term project."""

from __future__ import annotations

from collections import deque

EMPTY, RED, BLUE = 0, 1, 2
SIZE = 11
DIRECTIONS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))


class HexBoard:
    def __init__(self, cells=None, history=None):
        self.cells = [row[:] for row in cells] if cells else [[EMPTY] * SIZE for _ in range(SIZE)]
        self.history = list(history) if history else []

    def copy(self):
        return HexBoard(self.cells, self.history)

    def legal_moves(self):
        return [(r, c) for r in range(SIZE) for c in range(SIZE) if self.cells[r][c] == EMPTY]

    def play(self, move, player):
        r, c = move
        if player not in (RED, BLUE):
            raise ValueError("invalid player")
        if not (0 <= r < SIZE and 0 <= c < SIZE) or self.cells[r][c] != EMPTY:
            raise ValueError("illegal move")
        self.cells[r][c] = player
        self.history.append((r, c, player))

    def undo(self):
        r, c, _ = self.history.pop()
        self.cells[r][c] = EMPTY

    def has_won(self, player):
        queue = deque()
        visited = set()
        starts = ((0, c) for c in range(SIZE)) if player == RED else ((r, 0) for r in range(SIZE))
        for cell in starts:
            r, c = cell
            if self.cells[r][c] == player:
                queue.append(cell)
                visited.add(cell)
        while queue:
            r, c = queue.popleft()
            if (player == RED and r == SIZE - 1) or (player == BLUE and c == SIZE - 1):
                return True
            for dr, dc in DIRECTIONS:
                nxt = r + dr, c + dc
                nr, nc = nxt
                if 0 <= nr < SIZE and 0 <= nc < SIZE and nxt not in visited and self.cells[nr][nc] == player:
                    visited.add(nxt)
                    queue.append(nxt)
        return False

    def render(self):
        lines = ["   " + " ".join(chr(65 + c) for c in range(SIZE))]
        for r, row in enumerate(self.cells):
            stones = " ".join("." if v == EMPTY else "R" if v == RED else "B" for v in row)
            lines.append(f"{r + 1:2} " + " " * r + stones)
        return "\n".join(lines)


def other(player):
    return BLUE if player == RED else RED


def parse_move(text):
    text = text.strip().lower()
    if len(text) < 2 or text[0] < "a" or text[0] > "k" or not text[1:].isdigit():
        raise ValueError("enter a coordinate such as f6")
    move = int(text[1:]) - 1, ord(text[0]) - ord("a")
    if not (0 <= move[0] < SIZE and 0 <= move[1] < SIZE):
        raise ValueError("coordinate is outside the board")
    return move


def move_text(move):
    r, c = move
    return f"{chr(ord('a') + c)}{r + 1}"
