"""Terminal game for a human playing against the Hex AI."""

from __future__ import annotations

import argparse
import random
import time

from hex_ai import (
    BLUE,
    EMPTY,
    RED,
    HexAI,
    has_won,
    move_to_notation,
    notation_to_move,
    opponent,
)


COLOR_NAME = {RED: "빨강(위-아래)", BLUE: "파랑(왼쪽-오른쪽)"}
STONE = {EMPTY: ".", RED: "R", BLUE: "B"}


def print_board(board: list[list[int]]) -> None:
    size = len(board)
    columns = " ".join(chr(ord("a") + col) for col in range(size))
    print(f"\n    {columns}")
    for row, values in enumerate(board):
        indent = " " * row
        stones = " - ".join(STONE[value] for value in values)
        print(f"{indent}{row + 1:>2}  {stones}  {row + 1}")
    print(f"{' ' * (size + 4)}{columns}\n")


def human_move(board: list[list[int]]) -> tuple[int, int]:
    size = len(board)
    while True:
        text = input("둘 위치 (예: h 10, 종료: q): ").strip().lower()
        if text in {"q", "quit", "exit"}:
            raise KeyboardInterrupt
        try:
            row, col = notation_to_move(text)
        except ValueError:
            print("좌표는 'h 10'처럼 열 문자와 행 번호로 입력하세요.")
            continue
        if not (0 <= row < size and 0 <= col < size):
            print("보드 밖의 좌표입니다.")
        elif board[row][col] != EMPTY:
            print("이미 돌이 놓인 칸입니다.")
        else:
            return row, col


def choose_human_color() -> int:
    while True:
        text = input("내 색을 선택하세요 [1: 레드 / 2: 블루]: ").strip().lower()
        if text in {"1", "r", "red", "레드", "빨강"}:
            return RED
        if text in {"2", "b", "blue", "블루", "파랑"}:
            return BLUE
        print("1(레드) 또는 2(블루)를 입력하세요.")


def main() -> None:
    parser = argparse.ArgumentParser(description="11x11 Hex: 사람 대 AI")
    parser.add_argument(
        "--human",
        choices=("red", "blue"),
        default=None,
        help="사람 색상. 생략하면 실행할 때 직접 선택",
    )
    parser.add_argument("--time", type=float, default=8.5, help="AI 한 수 사고시간, 10초 미만 (기본 8.5초)")
    parser.add_argument("--seed", type=int, default=None, help="첫 수와 AI 난수 재현용 seed")
    parser.add_argument(
        "--profile",
        choices=("mohex", "davies", "none"),
        default="mohex",
        help="오프닝 지식 선택 (기본: 사람/일반 상대에 적합한 mohex)",
    )
    parser.add_argument(
        "--auto-opening",
        action="store_true",
        help="과제의 빨강 첫 돌을 사람이 입력하지 않고 프로그램이 무작위 배치",
    )
    parser.add_argument(
        "--normal-opening",
        action="store_true",
        help="과제 규칙의 랜덤 첫 수 대신 빨강이 첫 수를 직접 둠",
    )
    args = parser.parse_args()

    if args.human is None:
        try:
            human = choose_human_color()
        except (KeyboardInterrupt, EOFError):
            print("\n게임을 종료합니다.")
            return
    else:
        human = RED if args.human == "red" else BLUE
    ai_color = opponent(human)
    board = [[EMPTY] * 11 for _ in range(11)]
    rng = random.Random(args.seed)
    ai = HexAI(time_limit=args.time, seed=args.seed, book_profile=args.profile)
    turn = RED

    print("Hex 11x11 - 사람 대 AI")
    print(f"> 선택한 색: {COLOR_NAME[human]}")
    print(f"> AI 색상: {COLOR_NAME[ai_color]}")
    print(f"> AI 프로필: {args.profile}")
    print("R은 위-아래, B는 왼쪽-오른쪽을 연결하면 승리합니다.")

    # The assignment requires Red's first stone to be random. By default the
    # operator enters the externally drawn coordinate; --auto-opening is handy
    # for casual games.
    if not args.normal_opening:
        if args.auto_opening:
            row, col = divmod(rng.randrange(121), 11)
            print(f"과제 규칙: 빨강 첫 돌을 {move_to_notation((row, col))}로 자동 추첨했습니다.")
        else:
            print("과제에서 무작위로 정해진 빨강 첫 돌의 위치를 입력하세요.")
            try:
                row, col = human_move(board)
            except (KeyboardInterrupt, EOFError):
                print("\n게임을 종료합니다.")
                return
        board[row][col] = RED
        print(f"빨강 첫 돌을 {move_to_notation((row, col))}에 놓았습니다.")
        turn = BLUE

    try:
        while True:
            print_board(board)
            if turn == human:
                move = human_move(board)
            else:
                print(f"AI가 생각 중입니다... (최대 {args.time:g}초)")
                started = time.perf_counter()
                move = ai.choose_move(board, ai_color)
                print(
                    f"AI: {move_to_notation(move)} "
                    f"({time.perf_counter() - started:.2f}초, {ai.last_iterations}회 탐색)"
                )

            row, col = move
            board[row][col] = turn
            flat = [value for values in board for value in values]
            if has_won(flat, 11, turn):
                print_board(board)
                print("사람이 이겼습니다!" if turn == human else "AI가 이겼습니다!")
                return
            turn = opponent(turn)
    except (KeyboardInterrupt, EOFError):
        print("\n게임을 종료합니다.")


if __name__ == "__main__":
    main()
