"""Python port of the deterministic level-10 Davies Hex evaluator.

The original MIT implementation is davies-hex-ai 1.2.7 by Davies.  It uses
four potential fields (two borders per colour) and bridge bonuses.  This port
keeps those constants and propagation rules, with a Python-friendly API.
"""

from __future__ import annotations

from hex_board import BLUE, EMPTY, NEIGHBORS, RED, SIZE, HexBoard

INF = 20_000.0
OFF_BOARD = 30_000.0


class Davies10Python:
    name = "davies-10-python"

    def choose_move(self, board: HexBoard, player: int, time_limit: float | None = None) -> tuple[int, int]:
        scores = self.score_moves(board, player)
        if not scores:
            raise ValueError("board is full")
        fld = [[0 if x == EMPTY else -1 if x == RED else 1 for x in row] for row in board.cells]
        return self._far_border_choice(scores, fld, player)

    def _far_border_choice(self, scores, fld, player):
        best = min(scores, key=lambda move: (scores[move], move))
        minimum = scores[best] + 108
        colour = -1 if player == RED else 1
        for (r, c), value in scores.items():
            if value >= minimum:
                continue
            if colour < 0:
                if 3 < r < SIZE - 1 and 0 < c < 3 and fld[r - 1][c + 2] == 1:
                    far = self._can_connect_far_border(fld, r - 1, c + 2, 1)
                    if far < 2:
                        rr = r - (far < -1)
                        far += far < -1
                        best, minimum = (rr, c - far), value
                if 0 < r < SIZE - 1 and c == 0 and fld[r - 1][2] == 1 and all(fld[x][y] == 0 for x, y in ((r-1, 0), (r-1, 1), (r, 1), (r+1, 0))):
                    best, minimum = (r, c), value
                if 0 < r < SIZE - 4 and SIZE - 4 < c < SIZE - 1 and fld[r + 1][c - 2] == 1:
                    far = self._can_connect_far_border(fld, r + 1, c - 2, 1)
                    if far < 2:
                        rr = r + (far < -1)
                        far += far < -1
                        best, minimum = (rr, c + far), value
                if 0 < r < SIZE - 1 and c == SIZE - 1 and fld[r + 1][c - 2] == 1 and all(fld[x][y] == 0 for x, y in ((r+1, c), (r+1, c-1), (r, c-1), (r-1, c))):
                    best, minimum = (r, c), value
            else:
                if 3 < c < SIZE - 1 and 0 < r < 3 and fld[r + 2][c - 1] == -1:
                    far = self._can_connect_far_border(fld, r + 2, c - 1, -1)
                    if far < 2:
                        cc = c - (far < -1)
                        far += far < -1
                        best, minimum = (r - far, cc), value
                if 0 < c < SIZE - 1 and r == 0 and fld[2][c - 1] == -1 and all(fld[x][y] == 0 for x, y in ((0, c-1), (1, c-1), (1, c), (0, c+1))):
                    best, minimum = (r, c), value
                if 0 < c < SIZE - 4 and SIZE - 4 < r < SIZE - 1 and fld[r - 2][c + 1] == -1:
                    far = self._can_connect_far_border(fld, r - 2, c + 1, -1)
                    if far < 2:
                        cc = c + (far < -1)
                        far += far < -1
                        best, minimum = (r + far, cc), value
                if 0 < c < SIZE - 1 and r == SIZE - 1 and fld[r - 2][c + 1] == -1 and all(fld[x][y] == 0 for x, y in ((r, c+1), (r-1, c+1), (r-1, c), (r, c-1))):
                    best, minimum = (r, c), value
        return best

    @staticmethod
    def _get_fld(fld, r, c):
        if r < 0 or r >= SIZE:
            return -1
        if c < 0 or c >= SIZE:
            return 1
        return fld[r][c]

    def _can_connect_far_border(self, fld, r, c, colour):
        if colour > 0:
            if 2 * c < SIZE - 1:
                if any(fld[i][j] != 0 for i in range(SIZE) for j in range(c) if j-i < c-r and i+j <= r+c): return 2
                if fld[r-1][c] == -colour: return 0
                if fld[r-1][c-1] == -colour:
                    return 0 if self._get_fld(fld, r+2, c-1) == -colour else -1
                if self._get_fld(fld, r+2, c-1) == -colour: return -2
            else:
                if any(fld[i][j] != 0 for i in range(SIZE) for j in range(SIZE-1, c, -1) if j-i > c-r and i+j >= r+c): return 2
                if fld[r+1][c] == -colour: return 0
                if fld[r+1][c+1] == -colour:
                    return 0 if self._get_fld(fld, r-2, c+1) == -colour else -1
                if self._get_fld(fld, r-2, c+1) == -colour: return -2
        else:
            if 2 * r < SIZE - 1:
                if any(fld[i][j] != 0 for j in range(SIZE) for i in range(r) if i-j < r-c and i+j <= r+c): return 2
                if fld[r][c-1] == -colour: return 0
                if fld[r-1][c-1] == -colour:
                    return 0 if self._get_fld(fld, r-1, c+2) == -colour else -1
                if self._get_fld(fld, r-1, c+2) == -colour: return -2
            else:
                if any(fld[i][j] != 0 for j in range(SIZE) for i in range(SIZE-1, r, -1) if i-j > r-c and i+j >= r+c): return 2
                if fld[r][c+1] == -colour: return 0
                if fld[r+1][c+1] == -colour:
                    return 0 if self._get_fld(fld, r+1, c-2) == -colour else -1
                if self._get_fld(fld, r+1, c-2) == -colour: return -2
        return 1

    def score_moves(self, board: HexBoard, player: int) -> dict[tuple[int, int], float]:
        # Original storage: red=-1, blue=+1.
        fld = [[0 if x == EMPTY else -1 if x == RED else 1 for x in row] for row in board.cells]
        pot = [[[INF] * 4 for _ in range(SIZE)] for _ in range(SIZE)]
        bridge = [[[0.0] * 4 for _ in range(SIZE)] for _ in range(SIZE)]
        self._potentials(fld, pot, bridge)

        count = len(board.history) or sum(x != EMPTY for row in board.cells for x in row)
        spread = 190.0 / (count * count) if count else 0.0
        row_bias = self._sign(sum(2 * r + 1 - SIZE for r in range(SIZE) for c in range(SIZE) if fld[r][c]))
        col_bias = self._sign(sum(2 * c + 1 - SIZE for r in range(SIZE) for c in range(SIZE) if fld[r][c]))
        result: dict[tuple[int, int], float] = {}
        for r in range(SIZE):
            for c in range(SIZE):
                if fld[r][c] != 0:
                    continue
                value = (abs(r - 5) + abs(c - 5)) * spread
                value += 8.0 * (row_bias * (r - 5) + col_bias * (c - 5)) / (count + 1)
                value -= sum(bridge[r][c])
                own_pair = pot[r][c][2] + pot[r][c][3] if player == RED else pot[r][c][0] + pot[r][c][1]
                enemy_pair = pot[r][c][0] + pot[r][c][1] if player == RED else pot[r][c][2] + pot[r][c][3]
                value += own_pair + enemy_pair
                if own_pair <= 268 or enemy_pair <= 268:
                    value -= 400
                result[(r, c)] = value
        return result

    @staticmethod
    def _sign(value: int) -> int:
        return (value > 0) - (value < 0)

    def _potentials(self, fld, pot, bridge) -> None:
        for r in range(SIZE):
            if fld[r][0] == 0:
                pot[r][0][0] = 128
            elif fld[r][0] > 0:
                pot[r][0][0] = 0
            if fld[r][SIZE - 1] == 0:
                pot[r][SIZE - 1][1] = 128
            elif fld[r][SIZE - 1] > 0:
                pot[r][SIZE - 1][1] = 0
        for c in range(SIZE):
            if fld[0][c] == 0:
                pot[0][c][2] = 128
            elif fld[0][c] < 0:
                pot[0][c][2] = 0
            if fld[SIZE - 1][c] == 0:
                pot[SIZE - 1][c][3] = 128
            elif fld[SIZE - 1][c] < 0:
                pot[SIZE - 1][c][3] = 0

        # In davies-hex-ai 1.2.7 currentMove is left at its initialized RED
        # value when a custom/history position is evaluated.
        active_colour = -1
        for direction, colour in ((0, 1), (1, 1), (2, -1), (3, -1)):
            for _ in range(12):
                changes = 0
                for r in range(SIZE):
                    for c in range(SIZE):
                        changes += self._relax(fld, pot, bridge, r, c, direction, colour, active_colour)
                for r in range(SIZE - 1, -1, -1):
                    for c in range(SIZE - 1, -1, -1):
                        changes += self._relax(fld, pot, bridge, r, c, direction, colour, active_colour)
                if changes == 0:
                    break

    def _relax(self, fld, pot, bridge, r, c, direction, colour, active_colour) -> int:
        bridge[r][c][direction] = 0.0
        if fld[r][c] == -colour:
            return 0
        values = [self._pot_value(fld, pot, r + dr, c + dc, direction, colour) for dr, dc in NEIGHBORS]
        blocked_bonus = 0
        for i in range(6):
            if values[i] >= OFF_BOARD and values[(i + 2) % 6] >= OFF_BOARD:
                if values[(i + 1) % 6] < 0:
                    blocked_bonus += 32
                else:
                    values[(i + 1) % 6] += 128
        for i in range(6):
            if values[i] >= OFF_BOARD and values[(i + 3) % 6] >= OFF_BOARD:
                blocked_bonus += 30
        weights = [10 if value < 0 else 1 for value in values]
        values = [value + OFF_BOARD if value < 0 else value for value in values]
        minimum = min(values)
        ties = sum(weight for value, weight in zip(values, weights) if value == minimum)
        bridge_base = 66 if colour == active_colour else 52
        bonus = ties / 5
        if 2 <= ties < 10:
            bonus = bridge_base + ties - 2
            minimum -= 32
        elif ties < 2:
            second = min((v for v in values if v > minimum), default=OFF_BOARD)
            if second <= minimum + 104:
                bonus = bridge_base - (second - minimum) / 4
                minimum -= 64
            minimum = (minimum + second) / 2
        bonus += blocked_bonus if 0 < r < SIZE - 1 and 0 < c < SIZE - 1 else -2
        if r in (0, SIZE - 1) and c in (0, SIZE - 1):
            bonus /= 2
        bridge[r][c][direction] = min(68, bonus)
        new_value = minimum if fld[r][c] == colour else minimum + 140
        if new_value < pot[r][c][direction]:
            pot[r][c][direction] = new_value
            return 1
        return 0

    @staticmethod
    def _pot_value(fld, pot, r, c, direction, colour):
        if not (0 <= r < SIZE and 0 <= c < SIZE):
            return OFF_BOARD
        if fld[r][c] == 0:
            return pot[r][c][direction]
        if fld[r][c] == -colour:
            return OFF_BOARD
        return pot[r][c][direction] - OFF_BOARD
