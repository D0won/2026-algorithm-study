#!/usr/bin/env python3
"""Play the project Hex AI against the vendored MoHex 2.0 HTP engine.

The assignment's forced random RED opening is supplied explicitly for every
game.  RED maps to HTP black (north-south) and BLUE maps to HTP white
(west-east).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random
import subprocess
import sys
from typing import TextIO

from hex_ai import BLUE, EMPTY, RED, HexAI, has_won, move_to_notation, notation_to_move, opponent


ROOT = Path(__file__).resolve().parent
DEFAULT_MOHEX = ROOT / "vendor/benzene-vanilla-cmake/build/src/mohex/mohex"
COLORS = {RED: "black", BLUE: "white"}


class MoHex:
    def __init__(self, executable: Path, games_per_move: int, seed: int | None = None):
        if not executable.is_file():
            raise FileNotFoundError(f"MoHex executable not found: {executable}")
        command = [str(executable), "--quiet", "--use-logfile=0"]
        if seed is not None:
            command.append(f"--seed={seed}")
        self.process = subprocess.Popen(
            command,
            cwd=executable.parents[3],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )
        assert self.process.stdin is not None and self.process.stdout is not None
        self.stdin: TextIO = self.process.stdin
        self.stdout: TextIO = self.process.stdout
        self.command("boardsize 11 11")
        self.command("param_game allow_swap 0")
        self.command("param_mohex perform_pre_search 0")
        self.command(f"param_mohex max_games {games_per_move}")
        self.command("param_mohex num_threads 1")

    def command(self, text: str) -> str:
        self.stdin.write(text + "\n")
        self.stdin.flush()
        lines: list[str] = []
        while True:
            line = self.stdout.readline()
            if line == "":
                raise RuntimeError(f"MoHex exited while handling {text!r}")
            if line.strip() == "":
                break
            lines.append(line.rstrip())
        first = lines[0] if lines else ""
        if first.startswith("?"):
            raise RuntimeError(f"MoHex rejected {text!r}: {' '.join(lines)}")
        if first.startswith("="):
            lines[0] = first[1:].strip()
        return "\n".join(lines).strip()

    def reset(self) -> None:
        self.command("clear_board")

    def play(self, player: int, move: tuple[int, int]) -> None:
        self.command(f"play {COLORS[player]} {move_to_notation(move)}")

    def genmove(self, player: int) -> tuple[int, int]:
        reply = self.command(f"genmove {COLORS[player]}").splitlines()[0]
        return notation_to_move(reply)

    def close(self) -> None:
        if self.process.poll() is None:
            try:
                self.command("quit")
            except (BrokenPipeError, RuntimeError):
                pass
        self.process.wait(timeout=5)


def play_game(
    mohex: MoHex,
    our_color: int,
    opening: tuple[int, int],
    time_limit: float,
    seed: int,
) -> dict[str, object]:
    board = [[EMPTY] * 11 for _ in range(11)]
    moves: list[tuple[int, tuple[int, int]]] = [(RED, opening)]
    board[opening[0]][opening[1]] = RED
    mohex.reset()
    mohex.play(RED, opening)
    turn = BLUE
    iterations = 0

    while True:
        if turn == our_color:
            ai = HexAI(time_limit=time_limit, seed=seed + len(moves), book_profile="mohex")
            move = ai.choose_move(board, turn)
            iterations += ai.last_iterations
            mohex.play(turn, move)
        else:
            move = mohex.genmove(turn)
        row, col = move
        if not (0 <= row < 11 and 0 <= col < 11) or board[row][col] != EMPTY:
            raise RuntimeError(f"illegal move from {'ours' if turn == our_color else 'MoHex'}: {move}")
        board[row][col] = turn
        moves.append((turn, move))
        flat = [cell for line in board for cell in line]
        if has_won(flat, 11, turn):
            return {
                "winner": turn,
                "our_color": our_color,
                "opening": move_to_notation(opening),
                "plies": len(moves),
                "our_iterations": iterations,
                "moves": [f"{'R' if color == RED else 'B'}:{move_to_notation(pos)}" for color, pos in moves],
            }
        turn = opponent(turn)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mohex", type=Path, default=DEFAULT_MOHEX)
    parser.add_argument("--games", type=int, default=8, help="must be even; colors alternate")
    parser.add_argument("--mohex-playouts", type=int, default=200)
    parser.add_argument("--time-limit", type=float, default=0.08, help="seconds for our AI per move")
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--mohex-seed", type=int, default=20260621)
    parser.add_argument(
        "--fresh-engine", action="store_true",
        help="start MoHex with an independent derived seed for every game",
    )
    parser.add_argument("--output", type=Path, default=ROOT / "training/mohex_games.jsonl")
    args = parser.parse_args()
    if args.games < 2 or args.games % 2:
        parser.error("--games must be a positive even number")

    rng = random.Random(args.seed)
    openings = rng.sample([(row, col) for row in range(11) for col in range(11)], args.games // 2)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    engine = None if args.fresh_engine else MoHex(
        args.mohex.resolve(), args.mohex_playouts, seed=args.mohex_seed
    )
    wins = 0
    try:
        with args.output.open("w", encoding="utf-8") as log:
            game_number = 0
            for opening in openings:
                for our_color in (RED, BLUE):
                    game_number += 1
                    game_engine = engine or MoHex(
                        args.mohex.resolve(), args.mohex_playouts,
                        seed=args.mohex_seed + game_number,
                    )
                    try:
                        result = play_game(
                            game_engine, our_color, opening, args.time_limit,
                            args.seed + game_number * 1000,
                        )
                    finally:
                        if engine is None:
                            game_engine.close()
                    won = result["winner"] == our_color
                    wins += int(won)
                    log.write(json.dumps(result) + "\n")
                    log.flush()
                    print(
                        f"game {game_number:02d}/{args.games}: "
                        f"ours={'RED' if our_color == RED else 'BLUE':4s} "
                        f"opening={result['opening']:>3s} winner="
                        f"{'OURS' if won else 'MOHEX'} plies={result['plies']}"
                    )
    finally:
        if engine is not None:
            engine.close()
    print(f"result: {wins}/{args.games} ({wins / args.games:.1%})")
    print(f"games: {args.output}")


if __name__ == "__main__":
    main()
