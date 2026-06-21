"""Round-robin benchmark against the unmodified JavaScript Davies 10."""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from enhanced_ai import EnhancedDaviesAI
from hex_board import BLUE, RED, HexBoard, format_move, opponent


class OriginalDavies10:
    name = "original-davies-10-js"

    def __init__(self):
        runner = Path(__file__).with_name("original_davies_runner.mjs")
        self.process = subprocess.Popen(
            ["node", str(runner)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            text=True, bufsize=1,
        )

    def choose_move(self, board: HexBoard, player: int, time_limit=None):
        history = [format_move((r, c)) for r, c, _ in board.history]
        assert self.process.stdin and self.process.stdout
        self.process.stdin.write(json.dumps({"player": player, "history": history}) + "\n")
        self.process.stdin.flush()
        response = json.loads(self.process.stdout.readline())
        if "error" in response:
            raise RuntimeError(response["error"])
        text = response["move"]
        return int(text[1:]) - 1, ord(text[0]) - 97

    def close(self):
        self.process.terminate()
        self.process.wait(timeout=2)


@dataclass
class Result:
    winner: int
    moves: int
    elapsed: float
    opening: tuple[int, int]
    max_move_time: float


def play_game(red, blue, opening, move_time: float) -> Result:
    board = HexBoard()
    board.play(opening, RED)  # Assignment rule: the first red stone is random.
    player = BLUE
    started = time.monotonic()
    max_move_time = 0.0
    while True:
        ai = red if player == RED else blue
        move_started = time.monotonic()
        move = ai.choose_move(board, player, move_time)
        max_move_time = max(max_move_time, time.monotonic() - move_started)
        board.play(move, player)
        if board.has_won(player):
            return Result(player, len(board.history), time.monotonic() - started, opening, max_move_time)
        player = opponent(player)


def run(games: int, move_time: float, seed: int):
    rng = random.Random(seed)
    original = OriginalDavies10()
    enhanced = EnhancedDaviesAI(move_time)
    wins = {enhanced.name: 0, original.name: 0}
    opening = None
    try:
        for index in range(games):
            if index % 2 == 0 or opening is None:
                opening = rng.randrange(11), rng.randrange(11)
            enhanced_red = index % 2 == 0
            red, blue = (enhanced, original) if enhanced_red else (original, enhanced)
            result = play_game(red, blue, opening, move_time)
            if result.max_move_time >= 10.0:
                raise RuntimeError(f"10-second move limit exceeded: {result.max_move_time:.3f}s")
            winner_ai = red if result.winner == RED else blue
            wins[winner_ai.name] += 1
            colour = "R" if result.winner == RED else "B"
            print(f"{index+1:02}/{games}: {winner_ai.name} ({colour}), {result.moves} moves, {result.elapsed:.2f}s, max-move={result.max_move_time:.2f}s, opening={format_move(opening)}")
    finally:
        original.close()
    print("\nResult")
    for name, count in wins.items():
        print(f"  {name}: {count}/{games} ({count / games:.1%})")
    return wins


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=20)
    parser.add_argument("--time", type=float, default=9.0, help="seconds per enhanced move")
    parser.add_argument("--seed", type=int, default=20260621)
    args = parser.parse_args()
    run(args.games, args.time, args.seed)
