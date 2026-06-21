"""Compress generated Davies positions into a runtime strategy book."""

from __future__ import annotations

import json


def main() -> None:
    book = {}
    with open("training/davies_positions.jsonl", encoding="utf-8") as source:
        for line in source:
            row = json.loads(line)
            key = f'{row["player"]}:' + "".join(str(value) for values in row["board"] for value in values)
            book[key] = {"move": row["move"], "winner": row["winner"]}
    with open("davies_book.json", "w", encoding="utf-8") as target:
        json.dump(book, target, separators=(",", ":"))
    print(f"wrote {len(book)} strategy-book positions")


if __name__ == "__main__":
    main()
