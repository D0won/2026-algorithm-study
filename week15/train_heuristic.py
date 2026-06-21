"""Fit linear move-ordering weights to Davies-10 self-play choices."""

from __future__ import annotations

import json
import math
import random

from hex_ai import (EMPTY, HEURISTIC_WEIGHTS, _connection_cost,
                    _forced_bridge_responses, _heuristic_features)


def dot(weights, features):
    return sum(a * b for a, b in zip(weights, features))


def main() -> None:
    rng = random.Random(20260621)
    with open("training/davies_positions.jsonl", encoding="utf-8") as stream:
        rows = [json.loads(line) for index, line in enumerate(stream) if index % 4 == 0]
    examples = []
    for number, row in enumerate(rows, 1):
        board, player = row["board"], row["player"]
        size = len(board)
        cells = [value for values in board for value in values]
        chosen = row["move"][0] * size + row["move"][1]
        empties = [i for i, value in enumerate(cells) if value == EMPTY]
        own = _connection_cost(cells, size, player)
        enemy = _connection_cost(cells, size, 3 - player)
        bridges = _forced_bridge_responses(cells, size, player)
        good = _heuristic_features(cells, size, chosen, player, own, enemy, bridges)
        candidates = []
        for move in empties:
            if move != chosen:
                features = _heuristic_features(cells, size, move, player, own, enemy, bridges)
                candidates.append((dot(HEURISTIC_WEIGHTS, features), features))
        candidates.sort(reverse=True)
        selected = [features for _, features in candidates[:12]]
        if len(candidates) > 12:
            selected += [features for _, features in rng.sample(candidates[12:], min(8, len(candidates) - 12))]
        examples.append((good, selected))
        if number % 100 == 0:
            print(f"features {number}/{len(rows)}")

    weights = list(HEURISTIC_WEIGHTS)
    accuracy = lambda: sum(dot(weights, good) > max(map(lambda bad: dot(weights, bad), negatives))
                           for good, negatives in examples) / len(examples)
    before = accuracy()
    for epoch in range(12):
        rng.shuffle(examples)
        mistakes, rate = 0, 0.18 / math.sqrt(epoch + 1)
        for good, negatives in examples:
            bad = max(negatives, key=lambda features: dot(weights, features))
            if dot(weights, good) - dot(weights, bad) < 1.0:
                difference = [a - b for a, b in zip(good, bad)]
                norm = math.sqrt(sum(value * value for value in difference)) or 1.0
                weights = [weight + rate * value / norm for weight, value in zip(weights, difference)]
                mistakes += 1
        print(f"epoch={epoch + 1} mistakes={mistakes} weights={[round(x, 4) for x in weights]}")
    print(json.dumps({"examples": len(examples), "top1_before": before,
                      "top1_after": accuracy(), "weights": weights}, indent=2))


if __name__ == "__main__":
    main()
