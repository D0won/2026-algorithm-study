"""Davies-inspired evaluator strengthened with tactics and time-bounded search."""

from __future__ import annotations

import heapq
import math
import time

from davies_port import Davies10Python
from hex_board import BLUE, EMPTY, NEIGHBORS, RED, SIZE, HexBoard, opponent


class SearchTimeout(Exception):
    pass


class EnhancedDaviesAI:
    name = "enhanced-davies"

    def __init__(self, time_limit: float = 9.0, max_depth: int = 0):
        self.time_limit = min(9.5, max(0.02, time_limit))
        self.max_depth = max_depth
        self.davies = Davies10Python()
        self.deadline = 0.0
        self.root_player = RED
        self.nodes = 0
        self.counter_plan: dict[tuple[int, ...], tuple[int, int]] = {}

    def choose_move(self, board: HexBoard, player: int, time_limit: float | None = None) -> tuple[int, int]:
        legal = board.legal_moves()
        if not legal:
            raise ValueError("board is full")
        self.deadline = time.monotonic() + min(9.5, time_limit or self.time_limit)
        self.root_player = player
        self.nodes = 0

        win = self._winning_move(board, player, legal)
        if win is not None:
            return win
        planned = self.counter_plan.get(self._signature(board, player))
        if planned is not None and board.cells[planned[0]][planned[1]] == EMPTY:
            return planned
        threats = self._all_winning_moves(board, opponent(player), legal)
        if threats:
            # A single block is forced; with several threats, search still chooses the best defence.
            if len(threats) == 1:
                return threats[0]

        ordered = self._ordered_moves(board, player, 18)
        # Preserve Davies' positional judgement unless a tactical improvement
        # can be proven. A move that creates two immediate wins is a forced win.
        safe = []
        for move in ordered[:6]:
            if time.monotonic() >= self.deadline:
                break
            board.play(move, player)
            try:
                replies = board.legal_moves()
                if self._all_winning_moves(board, opponent(player), replies):
                    continue
                if len(self._all_winning_moves(board, player, replies)) >= 2:
                    return move
                safe.append(move)
            finally:
                board.undo()
        best = threats[0] if threats else (safe[0] if safe else ordered[0])
        # Model the known opponent: deterministically finish candidate games
        # with the Davies-10 policy and accept only a candidate predicted to win.
        if self.time_limit >= 0.2 and not threats:
            sampled = self._davies_rollouts(board, player, safe[:6] or ordered[:6])
            if sampled is not None:
                best, plan = sampled
                self.counter_plan.update(plan)
        if self.max_depth <= 0:
            return best
        for depth in range(1, self.max_depth + 1):
            try:
                value, move = self._root_search(board, player, depth, ordered)
                if move is not None:
                    best = move
                if abs(value) >= 900_000:
                    break
            except SearchTimeout:
                break
        return best

    def _davies_rollouts(self, board: HexBoard, player: int, candidates: list[tuple[int, int]]):
        for candidate in candidates:
            if time.monotonic() >= self.deadline - 0.01:
                break
            trial = board.copy()
            plan = {self._signature(trial, player): candidate}
            trial.play(candidate, player)
            turn = opponent(player)
            while not trial.has_won(opponent(turn)) and trial.legal_moves():
                if time.monotonic() >= self.deadline - 0.01:
                    return None
                move = self.davies.choose_move(trial, turn)
                if turn == player:
                    plan[self._signature(trial, turn)] = move
                trial.play(move, turn)
                turn = opponent(turn)
            winner = opponent(turn)
            if trial.has_won(player) and winner == player:
                return candidate, plan
        return None

    @staticmethod
    def _signature(board: HexBoard, player: int) -> tuple[int, ...]:
        return (player, *(cell for row in board.cells for cell in row))

    def _root_search(self, board, player, depth, moves):
        alpha, beta = -math.inf, math.inf
        best_move = None
        for move in moves:
            self._check_time()
            board.play(move, player)
            try:
                value = -self._negamax(board, opponent(player), depth - 1, -beta, -alpha)
            finally:
                board.undo()
            if value > alpha:
                alpha, best_move = value, move
        return alpha, best_move

    def _negamax(self, board, player, depth, alpha, beta):
        self._check_time()
        self.nodes += 1
        last_player = opponent(player)
        if board.has_won(last_player):
            return -1_000_000 - depth
        if depth == 0:
            score = self._evaluate(board, player)
            return score
        width = 12 if depth > 1 else 16
        moves = self._ordered_moves(board, player, width)
        if not moves:
            return 0.0
        best = -math.inf
        for move in moves:
            board.play(move, player)
            try:
                value = -self._negamax(board, opponent(player), depth - 1, -beta, -alpha)
            finally:
                board.undo()
            best = max(best, value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best

    def _ordered_moves(self, board: HexBoard, player: int, width: int) -> list[tuple[int, int]]:
        scores = self.davies.score_moves(board, player)
        davies_best = self.davies.choose_move(board, player)
        occupied = [(r, c) for r in range(SIZE) for c in range(SIZE) if board.cells[r][c] != EMPTY]
        def priority(item):
            (r, c), davies = item
            adjacent = sum(
                3 if board.cells[r + dr][c + dc] == player else 2
                for dr, dc in NEIGHBORS
                if 0 <= r + dr < SIZE and 0 <= c + dc < SIZE and board.cells[r + dr][c + dc] != EMPTY
            )
            near = 0 if not occupied else min(max(abs(r-r0), abs(c-c0), abs((r+c)-(r0+c0))) for r0, c0 in occupied)
            return davies - adjacent * 18 + near * 20
        ordered = [move for move, _ in sorted(scores.items(), key=priority)]
        ordered.remove(davies_best)
        return [davies_best, *ordered[:width - 1]]

    def _winning_move(self, board, player, moves):
        wins = self._all_winning_moves(board, player, moves)
        return wins[0] if wins else None

    @staticmethod
    def _all_winning_moves(board, player, moves):
        wins = []
        for move in moves:
            board.play(move, player)
            won = board.has_won(player)
            board.undo()
            if won:
                wins.append(move)
        return wins

    def _evaluate(self, board: HexBoard, player: int) -> float:
        own = self._connection_cost(board, player)
        enemy = self._connection_cost(board, opponent(player))
        # One empty cell closer is strategically enormous in Hex.
        return (enemy - own) * 1000 + self._stone_shape(board, player) - self._stone_shape(board, opponent(player))

    @staticmethod
    def _stone_shape(board: HexBoard, player: int) -> float:
        stones = [(r, c) for r in range(SIZE) for c in range(SIZE) if board.cells[r][c] == player]
        if not stones:
            return 0.0
        span = (max(r for r, _ in stones) - min(r for r, _ in stones)) if player == RED else (max(c for _, c in stones) - min(c for _, c in stones))
        links = 0
        for r, c in stones:
            links += sum(1 for dr, dc in NEIGHBORS[:3] if 0 <= r+dr < SIZE and 0 <= c+dc < SIZE and board.cells[r+dr][c+dc] == player)
        return span * 12 + links * 5

    @staticmethod
    def _connection_cost(board: HexBoard, player: int) -> int:
        inf = 10_000
        dist = [[inf] * SIZE for _ in range(SIZE)]
        heap = []
        starts = ((0, c) for c in range(SIZE)) if player == RED else ((r, 0) for r in range(SIZE))
        for r, c in starts:
            cell = board.cells[r][c]
            if cell == opponent(player):
                continue
            cost = 0 if cell == player else 1
            dist[r][c] = cost
            heapq.heappush(heap, (cost, r, c))
        while heap:
            cost, r, c = heapq.heappop(heap)
            if cost != dist[r][c]:
                continue
            if (player == RED and r == SIZE - 1) or (player == BLUE and c == SIZE - 1):
                return cost
            for dr, dc in NEIGHBORS:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < SIZE and 0 <= nc < SIZE) or board.cells[nr][nc] == opponent(player):
                    continue
                nxt = cost + (board.cells[nr][nc] == EMPTY)
                if nxt < dist[nr][nc]:
                    dist[nr][nc] = nxt
                    heapq.heappush(heap, (nxt, nr, nc))
        return inf

    def _check_time(self):
        if time.monotonic() >= self.deadline:
            raise SearchTimeout
