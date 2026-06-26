"""Console runner for the independently implemented Hex AI."""

from __future__ import annotations

import argparse
import random

from hex_ai import HexAI
from hex_board import BLUE, EMPTY, RED, HexBoard, move_text, other, parse_move


def choose_side(value=None):
    while value is None:
        answer = input("Choose side - 1: Red(first), 2: Blue(second): ").strip().lower()
        if answer in ("1", "r", "red"):
            return RED
        if answer in ("2", "b", "blue"):
            return BLUE
        print("Please enter 1 or 2.")
    return RED if value == "red" else BLUE


def opening_move(value, seed):
    if value:
        return parse_move(value)
    entered = input("Enter the randomly assigned first Red move (Enter=random practice): ").strip()
    if entered:
        return parse_move(entered)
    rng = random.Random(seed)
    return rng.randrange(11), rng.randrange(11)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--human", choices=("red", "blue"))
    parser.add_argument("--opening")
    parser.add_argument("--time", type=float, default=9.0)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()

    human = choose_side(args.human)
    board = HexBoard()
    first = opening_move(args.opening, args.seed)
    board.play(first, RED)
    print("Random Red opening:", move_text(first))
    ai = HexAI(args.time)
    player = BLUE

    while True:
        print("\n" + board.render())
        if player == human:
            while True:
                try:
                    move = parse_move(input("Your move: "))
                    if board.cells[move[0]][move[1]] != EMPTY:
                        raise ValueError("that cell is occupied")
                    break
                except ValueError as error:
                    print(error)
        else:
            move = ai.choose_move(board, player)
            print(f"AI move: {move_text(move)} (depth={ai.completed_depth}, nodes={ai.nodes})")
        board.play(move, player)
        if board.has_won(player):
            print("\n" + board.render())
            print("Red wins!" if player == RED else "Blue wins!")
            return
        player = other(player)


if __name__ == "__main__":
    main()
