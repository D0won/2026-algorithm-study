"""Davies 10 기반 Python 파생·재구현 Hex AI.

[베이스 코드 및 출처]
- Davies, ``davies-hex-ai`` version 1.2.7 (MIT License)
- Original: https://github.com/DaviesGit/hex_board_game
- Adapted package: https://github.com/alcalyn/hex_board_game
- PlayHex integration: https://github.com/playhex/playhex

[베이스에서 참고·재구현한 부분]
- Davies AI의 4방향 potential field와 bridge 평가 개념
- 레드/블루 목표 변으로부터 potential을 반복 전파하는 평가 절차
- 가장자리 연결 보정과 level-10 결정적 후보 선택 방식
- 위 로직은 JavaScript 구현을 Python의 ``HexBoard`` 인터페이스에 맞게
  ``Davies10Python`` 클래스로 포팅·재구성하였다.

[새로 추가하거나 변경한 부분]
- 보드 상태와 AI를 분리하고 ``choose_move(board, player)`` 인터페이스 적용
- 즉시 승리 수 탐색 및 상대의 즉시 승리 차단
- 위험한 후보 제거와 2수 포크 검사
- Davies 평가 기반 후보 정렬에 인접도·거리 휴리스틱 추가
- Dijkstra 최소 연결 비용, 연결 span 및 인접 연결 평가 추가
- iterative-deepening negamax와 alpha-beta pruning 추가
- Davies 정책 rollout과 보드 상태별 counter-plan 캐시 추가
- ``time.monotonic`` 기반 9.5초 상한 및 탐색 중 보드 복구 보장

[구현 도구]
- Python 구현, 테스트, 리팩터링 및 문서화 과정에서 OpenAI Codex를 사용하였다.

이 파일은 Davies 원본의 완전한 독자 구현이라고 주장하지 않으며, 공개 구현을
베이스로 Python에서 포팅한 뒤 위 전술·탐색 요소를 추가한 파생 구현이다.
"""

from __future__ import annotations

import heapq
import math
import time

from hex_board import BLUE, EMPTY, NEIGHBORS, RED, SIZE, HexBoard, opponent

INF = 20_000.0
OFF_BOARD = 30_000.0


# ---------------------------------------------------------------------------
# Davies 공개 구현을 Python 보드 구조에 맞게 포팅·재구성한 베이스 평가 영역
# ---------------------------------------------------------------------------
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
# ---------------------------------------------------------------------------
# 프로젝트에서 새로 추가한 전술, 탐색, 시간 제어 및 counter-plan 영역
# ---------------------------------------------------------------------------
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
