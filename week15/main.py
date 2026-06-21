"""Small JSON-lines adapter for the Hex AI.

Input:  {"board": [[...]], "player": 1, "time_limit": 8.5}
Output: {"row": 5, "col": 5, "move": "f6"}
"""

from __future__ import annotations

import json
import sys

from hex_ai import get_best_move, move_to_notation


def main() -> None:
    request = json.load(sys.stdin)
    move = get_best_move(
        request["board"],
        int(request["player"]),
        float(request.get("time_limit", 8.5)),
        request.get("seed"),
        str(request.get("profile", "mohex")),
    )
    json.dump({"row": move[0], "col": move[1], "move": move_to_notation(move)}, sys.stdout)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
