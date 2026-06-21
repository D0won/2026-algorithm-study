"""11x11 Hex board and rules (standard library only)."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

EMPTY, RED, BLUE = 0, 1, 2
SIZE = 11
NEIGHBORS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))


@dataclass
class HexBoard:
    cells: list[list[int]] = field(
        default_factory=lambda: [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
    )
    history: list[tuple[int, int, int]] = field(default_factory=list)

    def copy(self) -> "HexBoard":
        return HexBoard([row[:] for row in self.cells], self.history[:])

    def legal_moves(self) -> list[tuple[int, int]]:
        return [(r, c) for r in range(SIZE) for c in range(SIZE) if self.cells[r][c] == EMPTY]

    def play(self, move: tuple[int, int], player: int) -> None:
        r, c = move
        if player not in (RED, BLUE) or not (0 <= r < SIZE and 0 <= c < SIZE):
            raise ValueError("invalid move or player")
        if self.cells[r][c] != EMPTY:
            raise ValueError(f"occupied cell: {format_move(move)}")
        self.cells[r][c] = player
        self.history.append((r, c, player))

    def undo(self) -> None:
        r, c, _ = self.history.pop()
        self.cells[r][c] = EMPTY

    def has_won(self, player: int) -> bool:
        seen: set[tuple[int, int]] = set()
        queue: deque[tuple[int, int]] = deque()
        if player == RED:
            starts = ((0, c) for c in range(SIZE))
            reached = lambda r, c: r == SIZE - 1
        else:
            starts = ((r, 0) for r in range(SIZE))
            reached = lambda r, c: c == SIZE - 1
        for pos in starts:
            r, c = pos
            if self.cells[r][c] == player:
                seen.add(pos)
                queue.append(pos)
        while queue:
            r, c = queue.popleft()
            if reached(r, c):
                return True
            for dr, dc in NEIGHBORS:
                nxt = r + dr, c + dc
                nr, nc = nxt
                if 0 <= nr < SIZE and 0 <= nc < SIZE and nxt not in seen and self.cells[nr][nc] == player:
                    seen.add(nxt)
                    queue.append(nxt)
        return False

    def render(self) -> str:
        out = ["   " + " ".join(chr(65 + c) for c in range(SIZE))]
        for r, row in enumerate(self.cells):
            marks = " ".join("." if x == EMPTY else "R" if x == RED else "B" for x in row)
            out.append(f"{r + 1:2} " + " " * r + marks)
        return "\n".join(out)


def opponent(player: int) -> int:
    return BLUE if player == RED else RED


def format_move(move: tuple[int, int]) -> str:
    r, c = move
    return f"{chr(97 + c)}{r + 1}"


def parse_move(text: str) -> tuple[int, int]:
    text = text.strip().lower()
    if len(text) < 2 or not text[0].isalpha() or not text[1:].isdigit():
        raise ValueError("use a move such as f6")
    move = int(text[1:]) - 1, ord(text[0]) - 97
    if not (0 <= move[0] < SIZE and 0 <= move[1] < SIZE):
        raise ValueError("move outside 11x11 board")
    return move
