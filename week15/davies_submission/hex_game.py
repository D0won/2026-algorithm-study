"""Console game: human vs enhanced Davies AI."""

from __future__ import annotations

import argparse
import random

from hex_ai import EnhancedDaviesAI
from hex_board import BLUE, RED, HexBoard, format_move, opponent, parse_move


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--human", choices=("red", "blue"))
    parser.add_argument("--opening", help="random red opening shown by the tournament, e.g. f6")
    parser.add_argument("--time", type=float, default=9.0)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    human_text = args.human
    while human_text is None:
        answer = input("Choose your side: 1) first/Red  2) second/Blue: ").strip().lower()
        if answer in ("1", "red", "r"):
            human_text = "red"
        elif answer in ("2", "blue", "b"):
            human_text = "blue"
        else:
            print("Enter 1 (Red) or 2 (Blue).")
    human = RED if human_text == "red" else BLUE
    ai = EnhancedDaviesAI(args.time)
    board = HexBoard()
    rng = random.Random(args.seed)
    opening_text = args.opening
    while opening_text is None:
        opening_text = input("Enter the randomly assigned first Red move (e.g. f6, Enter=random practice): ").strip()
        if not opening_text:
            opening = rng.randrange(11), rng.randrange(11)
            break
        try:
            opening = parse_move(opening_text)
        except ValueError as error:
            print(error)
            opening_text = None
    else:
        opening = parse_move(opening_text)
    board.play(opening, RED)
    print(f"Random red opening: {format_move(opening)}")
    player = BLUE
    while True:
        print("\n" + board.render())
        if player == human:
            while True:
                try:
                    move = parse_move(input("Your move (e.g. f6): "))
                    if board.cells[move[0]][move[1]] != 0:
                        raise ValueError("that cell is occupied")
                    break
                except ValueError as error:
                    print(error)
        else:
            move = ai.choose_move(board, player)
            print(f"AI: {format_move(move)} (searched {ai.nodes} nodes)")
        board.play(move, player)
        if board.has_won(player):
            print("\n" + board.render())
            print(("Red" if player == RED else "Blue") + " wins!")
            return
        player = opponent(player)


if __name__ == "__main__":
    main()
