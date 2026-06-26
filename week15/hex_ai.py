"""Independent rule-based Hex AI.

Strategy: forced tactics, shortest connection paths, explicit two-cell bridge
patterns, and time-bounded alpha-beta search.  No external engine, source port,
opening database, learned model, or external package is used.
"""

from __future__ import annotations

import heapq
import math
import time

from hex_board import BLUE, DIRECTIONS, EMPTY, RED, SIZE, HexBoard, other

BRIDGE_OFFSETS = ((2, -1), (1, 1), (-1, 2), (-2, 1), (-1, -1), (1, -2))
WIN_SCORE = 1_000_000


class OutOfTime(Exception):
    pass


class HexAI:
    def __init__(self, time_limit=9.0):
        self.time_limit = min(9.4, max(0.05, float(time_limit)))
        self.deadline = 0.0
        self.nodes = 0
        self.completed_depth = 0

    def choose_move(self, board: HexBoard, player: int):
        legal = board.legal_moves()
        if not legal:
            raise ValueError("board is full")
        self.deadline = time.monotonic() + self.time_limit
        self.nodes = 0
        self.completed_depth = 0

        winning = self._winning_moves(board, player, legal)
        if winning:
            return winning[0]
        enemy_wins = self._winning_moves(board, other(player), legal)
        if len(enemy_wins) == 1:
            return enemy_wins[0]

        ordered = self._ordered_moves(board, player, 20)
        best = enemy_wins[0] if enemy_wins else ordered[0]
        for depth in range(1, 5):
            try:
                _, candidate = self._search_root(board, player, ordered, depth)
                if candidate is not None:
                    best = candidate
                    self.completed_depth = depth
            except OutOfTime:
                break
        return best

    def _search_root(self, board, player, moves, depth):
        alpha, beta = -math.inf, math.inf
        best_move = None
        for move in moves:
            self._check_clock()
            board.play(move, player)
            try:
                value = -self._negamax(board, other(player), depth - 1, -beta, -alpha)
            finally:
                board.undo()
            if value > alpha:
                alpha, best_move = value, move
        return alpha, best_move

    def _negamax(self, board, player, depth, alpha, beta):
        self._check_clock()
        self.nodes += 1
        if board.has_won(other(player)):
            return -WIN_SCORE - depth
        if depth == 0:
            return self._position_value(board, player)

        width = 14 if depth >= 3 else 11 if depth == 2 else 9
        moves = self._ordered_moves(board, player, width)
        if not moves:
            return 0
        best = -math.inf
        for move in moves:
            board.play(move, player)
            try:
                value = -self._negamax(board, other(player), depth - 1, -beta, -alpha)
            finally:
                board.undo()
            best = max(best, value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best

    def _ordered_moves(self, board, player, limit):
        legal = board.legal_moves()
        occupied = [(r, c) for r in range(SIZE) for c in range(SIZE) if board.cells[r][c] != EMPTY]
        if occupied:
            nearby = [m for m in legal if self._distance_to_group(m, occupied) <= 2]
            if len(nearby) >= 6:
                legal = nearby
        ranked = []
        for move in legal:
            self._check_clock()
            board.play(move, player)
            try:
                score = self._position_value(board, player)
                score += 70 * self._carrier_importance(board, move, player)
                score += 45 * self._carrier_importance(board, move, other(player))
            finally:
                board.undo()
            ranked.append((score, -abs(move[0] - 5) - abs(move[1] - 5), move))
        ranked.sort(reverse=True)
        return [move for _, _, move in ranked[:limit]]

    def _position_value(self, board, player):
        own = self._connection_cost(board, player)
        enemy = self._connection_cost(board, other(player))
        if own >= 10_000:
            return -WIN_SCORE // 2
        if enemy >= 10_000:
            return WIN_SCORE // 2
        # Blocking one opponent connection step is slightly more urgent than
        # gaining one step ourselves; this reduces losing races on 11x11.
        value = 1_450 * enemy - 1_000 * own
        value += 35 * (self._bridge_count(board, player) - self._bridge_count(board, other(player)))
        value += 12 * (self._goal_span(board, player) - self._goal_span(board, other(player)))
        return value

    def _connection_cost(self, board, player):
        blocked = other(player)
        infinity = 10_000
        distance = [[infinity] * SIZE for _ in range(SIZE)]
        queue = []
        starts = ((0, c) for c in range(SIZE)) if player == RED else ((r, 0) for r in range(SIZE))
        for r, c in starts:
            if board.cells[r][c] == blocked:
                continue
            cost = 0 if board.cells[r][c] == player else 1
            distance[r][c] = cost
            heapq.heappush(queue, (cost, r, c))
        while queue:
            cost, r, c = heapq.heappop(queue)
            if cost != distance[r][c]:
                continue
            if (player == RED and r == SIZE - 1) or (player == BLUE and c == SIZE - 1):
                return cost
            destinations = [(r + dr, c + dc, False) for dr, dc in DIRECTIONS]
            if board.cells[r][c] == player:
                for partner, carriers in self._bridges_from((r, c)):
                    pr, pc = partner
                    if board.cells[pr][pc] == player and all(board.cells[x][y] != blocked for x, y in carriers):
                        destinations.append((pr, pc, True))
            for nr, nc, virtual in destinations:
                if not (0 <= nr < SIZE and 0 <= nc < SIZE) or board.cells[nr][nc] == blocked:
                    continue
                step = 0 if virtual or board.cells[nr][nc] == player else 1
                new_cost = cost + step
                if new_cost < distance[nr][nc]:
                    distance[nr][nc] = new_cost
                    heapq.heappush(queue, (new_cost, nr, nc))
        return infinity

    def _bridge_count(self, board, player):
        count = 0
        for r in range(SIZE):
            for c in range(SIZE):
                if board.cells[r][c] != player:
                    continue
                for (pr, pc), carriers in self._bridges_from((r, c)):
                    if (pr, pc) > (r, c) and board.cells[pr][pc] == player:
                        empty = sum(board.cells[x][y] == EMPTY for x, y in carriers)
                        count += 2 if empty == 2 else 1 if empty == 1 else 0
        return count

    def _carrier_importance(self, board, move, player):
        r, c = move
        importance = 0
        stones = [(r + dr, c + dc) for dr, dc in BRIDGE_OFFSETS]
        for sr, sc in stones:
            if not (0 <= sr < SIZE and 0 <= sc < SIZE) or board.cells[sr][sc] != player:
                continue
            common = self._common_neighbors((r, c), (sr, sc))
            importance += sum(board.cells[x][y] == player for x, y in common)
        return importance

    def _bridges_from(self, cell):
        r, c = cell
        for dr, dc in BRIDGE_OFFSETS:
            partner = r + dr, c + dc
            if 0 <= partner[0] < SIZE and 0 <= partner[1] < SIZE:
                common = self._common_neighbors(cell, partner)
                if len(common) == 2:
                    yield partner, common

    @staticmethod
    def _common_neighbors(first, second):
        def neighbors(cell):
            r, c = cell
            return {(r + dr, c + dc) for dr, dc in DIRECTIONS if 0 <= r + dr < SIZE and 0 <= c + dc < SIZE}
        return tuple(sorted(neighbors(first) & neighbors(second)))

    @staticmethod
    def _distance_to_group(move, stones):
        r, c = move
        return min(max(abs(r - sr), abs(c - sc), abs((r + c) - (sr + sc))) for sr, sc in stones)

    @staticmethod
    def _goal_span(board, player):
        stones = [(r, c) for r in range(SIZE) for c in range(SIZE) if board.cells[r][c] == player]
        if not stones:
            return 0
        values = [r for r, _ in stones] if player == RED else [c for _, c in stones]
        return max(values) - min(values)

    @staticmethod
    def _winning_moves(board, player, moves):
        result = []
        for move in moves:
            board.play(move, player)
            won = board.has_won(player)
            board.undo()
            if won:
                result.append(move)
        return result

    def _check_clock(self):
        if time.monotonic() >= self.deadline:
            raise OutOfTime
