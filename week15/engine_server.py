"""Persistent JSON-lines process used by the Davies benchmark harness."""

from __future__ import annotations

import json
import sys

from hex_ai import HexAI


def main() -> None:
    for line in sys.stdin:
        try:
            request = json.loads(line)
            ai = HexAI(float(request["time_limit"]), request.get("seed"))
            row, col = ai.choose_move(request["board"], int(request["player"]))
            response = {"row": row, "col": col, "iterations": ai.last_iterations}
        except Exception as error:  # Protocol must always return one line.
            response = {"error": f"{type(error).__name__}: {error}"}
        print(json.dumps(response), flush=True)


if __name__ == "__main__":
    main()

