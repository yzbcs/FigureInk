#!/usr/bin/env python3
"""Generate the deterministic, entirely fictional repository showcase."""

from __future__ import annotations

import argparse
import json
import random
import statistics
from pathlib import Path
from typing import Any


DEFAULT_SEED = 20260804
DEFAULT_OUTPUT = (
    Path(__file__).resolve().parents[1]
    / "skill"
    / "plot-handdrawn-paper-charts"
    / "assets"
    / "example_showcase.json"
)


def simulate_landings(
    rng: random.Random, probability: float, batches: int = 6, launches: int = 10
) -> tuple[float, float]:
    """Return the mean and sample deviation from seeded Bernoulli launch batches."""
    batch_counts = [
        sum(rng.random() < probability for _ in range(launches))
        for _ in range(batches)
    ]
    return round(statistics.mean(batch_counts), 1), round(statistics.stdev(batch_counts), 1)


def build_spec(seed: int) -> dict[str, Any]:
    """Build one playful three-panel fixture from a local seeded RNG.

    The routine first samples 100 fictional flight endings, then simulates
    repeated ten-launch landing batches, and finally creates two noisy distance
    trajectories plus an uncertainty ribbon. The seed and procedure are stored
    in the emitted JSON so the showcase is reproducible without suggesting that
    any value came from a real experiment.
    """
    rng = random.Random(seed)

    ending_labels = ["Wonky wing", "Loose fold", "Lamp encounter", "Snack break"]
    ending_weights = [0.34, 0.29, 0.22, 0.15]
    sampled_endings = rng.choices(range(len(ending_labels)), ending_weights, k=100)
    ending_counts = [sampled_endings.count(index) for index in range(len(ending_labels))]

    conditions = ["Still air", "Desk fan", "Hallway gust"]
    dart_probabilities = [0.78, 0.58, 0.39]
    glider_probabilities = [0.88, 0.72, 0.61]
    dart_batches = [simulate_landings(rng, probability) for probability in dart_probabilities]
    glider_batches = [simulate_landings(rng, probability) for probability in glider_probabilities]

    rounds = list(range(1, 8))
    dart_range = [round(3.0 + 0.34 * step + rng.uniform(-0.24, 0.24), 1) for step in rounds]
    glider_range = [
        round(2.9 + 0.57 * step + rng.uniform(-0.20, 0.20), 1) for step in rounds
    ]
    glider_spread = [round(rng.uniform(0.20, 0.38), 1) for _ in rounds]
    glider_lower = [round(value - spread, 1) for value, spread in zip(glider_range, glider_spread)]
    glider_upper = [round(value + spread, 1) for value, spread in zip(glider_range, glider_spread)]

    return {
        "data_status": (
            "synthetic seeded showcase; all values are fictional and are not research measurements"
        ),
        "synthetic_generation": {
            "seed": seed,
            "generator": "showcase/generate_synthetic_showcase.py",
            "recipe": [
                "100 weighted fictional flight endings",
                "6 Bernoulli batches of 10 launches per plane and condition",
                "seeded noisy distance trajectories with a synthetic uncertainty ribbon",
            ],
        },
        "figure": {
            "stem": "paper-plane-lab-showcase",
            "width_in": 12.6,
            "height_in": 4.35,
            "rows": 1,
            "cols": 3,
            "palette": "ocean-blue",
            "sketch": "none",
            "font_family": "Comic Neue",
            "font_size": 9.2,
            "title_size": 13.0,
            "label_size": 9.4,
            "tick_size": 8.5,
            "legend_size": 8.2,
            "dpi": 300,
            "background": "#FFFFFF",
            "ink": "#27313A",
            "title": "The Great Paper-Plane Field Test",
            "suptitle_size": 17.0,
            "wspace": 0.12,
            "w_pad": 0.09,
            "h_pad": 0.08,
        },
        "panels": [
            {
                "type": "horizontal_bar",
                "panel_label": "A",
                "panel_label_x": -0.20,
                "panel_label_y": 1.02,
                "title": "Why flights ended early",
                "labels": ending_labels,
                "values": ending_counts,
                "color_roles": ["primary", "tertiary", "secondary", "pale"],
                "hatches": ["", "///", "xx", ".."],
                "sort": "descending",
                "value_labels": True,
                "value_format": "percent",
                "x_label": "Share of 100 pretend flights",
                "x_lim": [0, max(ending_counts) + 9],
                "x_tick_format": "percent",
                "grid": "x",
                "spines": "open",
            },
            {
                "type": "grouped_bar",
                "panel_label": "B",
                "panel_label_x": -0.13,
                "panel_label_y": 1.02,
                "title": "Soft landings per 10 launches",
                "categories": conditions,
                "series": [
                    {
                        "name": "Dart",
                        "values": [mean for mean, _ in dart_batches],
                        "errors": [deviation for _, deviation in dart_batches],
                        "color_role": "secondary",
                        "hatch": "///",
                    },
                    {
                        "name": "Loopwing",
                        "values": [mean for mean, _ in glider_batches],
                        "errors": [deviation for _, deviation in glider_batches],
                        "color_role": "primary",
                        "hatch": "",
                    },
                ],
                "y_label": "Mean soft landings",
                "y_lim": [0, 11.5],
                "y_ticks": [0, 2, 4, 6, 8, 10],
                "grid": "y",
                "spines": "open",
                "error_capsize": 3.0,
                "legend": {"loc": "upper right", "ncol": 1},
            },
            {
                "type": "line",
                "panel_label": "C",
                "panel_label_x": -0.13,
                "panel_label_y": 1.02,
                "title": "Range after each fold tweak",
                "x": rounds,
                "series": [
                    {
                        "name": "Dart",
                        "values": dart_range,
                        "color_role": "secondary",
                        "marker": "s",
                        "linestyle": "--",
                        "linewidth": 1.8,
                    },
                    {
                        "name": "Loopwing",
                        "values": glider_range,
                        "lower": glider_lower,
                        "upper": glider_upper,
                        "color_role": "primary",
                        "marker": "o",
                        "linewidth": 2.4,
                        "band_alpha": 0.18,
                    },
                ],
                "highlights": [
                    {
                        "series": "Loopwing",
                        "index": -1,
                        "marker": "*",
                        "size": 190,
                        "facecolor": "#4A8EBF",
                    }
                ],
                "annotations": [
                    {
                        "text": "best glide!",
                        "x": rounds[-1],
                        "y": glider_range[-1],
                        "text_x": rounds[-1] - 0.8,
                        "text_y": glider_range[-1] + 0.65,
                        "arrow": True,
                        "ha": "right",
                        "color": "#2B6188",
                    }
                ],
                "x_label": "Fold-tuning round",
                "y_label": "Flight range (m)",
                "x_lim": [0.7, 7.35],
                "x_ticks": rounds,
                "y_lim": [2.8, max(glider_upper) + 1.05],
                "grid": "both",
                "spines": "open",
                "legend": {"loc": "upper left"},
            },
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(build_spec(args.seed), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(args.output.resolve())


if __name__ == "__main__":
    main()
