#!/usr/bin/env python3
"""Fit generic move-ordering weights to positions analyzed by MoHex."""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from hex_ai import EMPTY, HEURISTIC_WEIGHTS, _connection_cost, _forced_bridge_responses, _heuristic_features


def dot(weights: list[float], features: tuple[float, ...]) -> float:
    return sum(a * b for a, b in zip(weights, features))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book", type=Path, default=Path("mohex_book.json"))
    parser.add_argument("--epochs", type=int, default=18)
    args = parser.parse_args()
    rng = random.Random(20260621)
    raw = json.loads(args.book.read_text(encoding="utf-8"))
    examples: list[tuple[tuple[float, ...], list[tuple[float, ...]]]] = []
    for number, (key, chosen_rc) in enumerate(raw.items(), 1):
        player_text, encoded = key.split(":", 1)
        player = int(player_text)
        size = math.isqrt(len(encoded))
        cells = [int(value) for value in encoded]
        chosen = chosen_rc[0] * size + chosen_rc[1]
        if cells[chosen] != EMPTY:
            continue
        own = _connection_cost(cells, size, player)
        enemy = _connection_cost(cells, size, 3 - player)
        bridges = _forced_bridge_responses(cells, size, player)
        good = _heuristic_features(cells, size, chosen, player, own, enemy, bridges)
        candidates = []
        for move, value in enumerate(cells):
            if value == EMPTY and move != chosen:
                feat = _heuristic_features(cells, size, move, player, own, enemy, bridges)
                candidates.append((dot(list(HEURISTIC_WEIGHTS), feat), feat))
        candidates.sort(reverse=True)
        negatives = [feat for _, feat in candidates[:16]]
        if len(candidates) > 16:
            negatives += [feat for _, feat in rng.sample(candidates[16:], min(8, len(candidates) - 16))]
        examples.append((good, negatives))
        if number % 100 == 0:
            print(f"features {number}/{len(raw)}", flush=True)

    weights = list(HEURISTIC_WEIGHTS)
    def accuracy() -> float:
        return sum(dot(weights, good) > max(dot(weights, bad) for bad in negatives)
                   for good, negatives in examples) / len(examples)
    before = accuracy()
    for epoch in range(args.epochs):
        rng.shuffle(examples)
        mistakes = 0
        rate = 0.30 / math.sqrt(epoch + 1)
        for good, negatives in examples:
            bad = max(negatives, key=lambda feat: dot(weights, feat))
            if dot(weights, good) - dot(weights, bad) < 0.5:
                difference = [a - b for a, b in zip(good, bad)]
                norm = math.sqrt(sum(value * value for value in difference)) or 1.0
                weights = [weight + rate * value / norm for weight, value in zip(weights, difference)]
                mistakes += 1
        print(f"epoch={epoch + 1} mistakes={mistakes}", flush=True)
    print(json.dumps({"examples": len(examples), "top1_before": before,
                      "top1_after": accuracy(), "weights": weights}, indent=2))


if __name__ == "__main__":
    main()
