#!/usr/bin/env python3
"""Validate and render editable conceptual paper figures from a JSON story spec.

The renderer keeps semantic roles, node geometry, relations, and exports in one
portable source. It is intended for intro and method diagrams; measured charts
should use a quantitative plotting workflow instead.
"""

from __future__ import annotations

import argparse
import json
import math
import shutil
import tempfile
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


VERSION = "1.0.0"
PALETTES = {
    "indigo-amber": {
        "background": "#FFFFFF",
        "ink": "#263042",
        "muted": "#667085",
        "stage": "#F4F6FA",
        "input": "#E8EEF9",
        "baseline": "#ECEFF3",
        "mechanism": "#D9E2FF",
        "state": "#E7E3F7",
        "output": "#DFF1E7",
        "warning": "#F9E6D4",
        "accent": "#4057A6",
    },
    "sage-coral": {
        "background": "#FFFFFF",
        "ink": "#2C3532",
        "muted": "#66736E",
        "stage": "#F3F6F4",
        "input": "#E7F0EC",
        "baseline": "#ECEFED",
        "mechanism": "#D9EBDD",
        "state": "#E7E8D8",
        "output": "#DDEFEA",
        "warning": "#F6DED6",
        "accent": "#4C743E",
    },
}
ROLES = {"input", "baseline", "mechanism", "state", "output", "warning"}
EDGE_STYLES = {"flow", "supervision", "feedback", "contrast"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    return parser.parse_args()


def finite(value: Any, label: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be numeric")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    if positive and number <= 0:
        raise ValueError(f"{label} must be positive")
    return number


def normalized(value: Any, label: str, *, positive: bool = False) -> float:
    number = finite(value, label, positive=positive)
    if number < 0 or number > 1:
        raise ValueError(f"{label} must be between 0 and 1")
    return number


def validate_box(item: dict[str, Any], label: str) -> None:
    for field in ("x", "y"):
        normalized(item.get(field), f"{label}.{field}")
    for field in ("w", "h"):
        normalized(item.get(field), f"{label}.{field}", positive=True)
    if float(item["x"]) + float(item["w"]) > 1:
        raise ValueError(f"{label} extends beyond the right edge")
    if float(item["y"]) + float(item["h"]) > 1:
        raise ValueError(f"{label} extends beyond the top edge")


def load_and_validate(path: Path) -> dict[str, Any]:
    spec = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(spec, dict):
        raise TypeError("the figure specification must be an object")
    if not str(spec.get("data_status", "")).strip():
        raise ValueError("data_status is required")

    figure = spec.get("figure")
    if not isinstance(figure, dict):
        raise TypeError("figure must be an object")
    stem = str(figure.get("stem", ""))
    if not stem or any(char in stem for char in "/\\"):
        raise ValueError("figure.stem must be a filename stem")
    finite(figure.get("width_in"), "figure.width_in", positive=True)
    finite(figure.get("height_in"), "figure.height_in", positive=True)
    finite(figure.get("dpi", 200), "figure.dpi", positive=True)
    palette = str(figure.get("palette", "indigo-amber"))
    if palette not in PALETTES:
        raise ValueError(f"unknown palette: {palette}")

    stages = spec.get("stages", [])
    if not isinstance(stages, list):
        raise TypeError("stages must be a list")
    stage_ids: set[str] = set()
    for index, stage in enumerate(stages):
        if not isinstance(stage, dict):
            raise TypeError(f"stages[{index}] must be an object")
        stage_id = str(stage.get("id", ""))
        if not stage_id or stage_id in stage_ids:
            raise ValueError(f"stages[{index}].id must be unique")
        stage_ids.add(stage_id)
        validate_box(stage, f"stages[{index}]")

    nodes = spec.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise TypeError("nodes must be a non-empty list")
    node_ids: set[str] = set()
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise TypeError(f"nodes[{index}] must be an object")
        node_id = str(node.get("id", ""))
        if not node_id or node_id in node_ids:
            raise ValueError(f"nodes[{index}].id must be unique")
        node_ids.add(node_id)
        if not str(node.get("label", "")).strip():
            raise ValueError(f"nodes[{index}].label is required")
        if str(node.get("role", "state")) not in ROLES:
            raise ValueError(f"nodes[{index}].role is unknown")
        validate_box(node, f"nodes[{index}]")

    edges = spec.get("edges", [])
    if not isinstance(edges, list):
        raise TypeError("edges must be a list")
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            raise TypeError(f"edges[{index}] must be an object")
        if str(edge.get("from", "")) not in node_ids:
            raise ValueError(f"edges[{index}].from references an unknown node")
        if str(edge.get("to", "")) not in node_ids:
            raise ValueError(f"edges[{index}].to references an unknown node")
        if str(edge.get("style", "flow")) not in EDGE_STYLES:
            raise ValueError(f"edges[{index}].style is unknown")
        if "curve" in edge:
            finite(edge["curve"], f"edges[{index}].curve")
    return spec


def anchor(node: dict[str, Any], target: dict[str, Any]) -> tuple[float, float]:
    """Return a boundary point on node in the direction of target."""
    cx = float(node["x"]) + float(node["w"]) / 2
    cy = float(node["y"]) + float(node["h"]) / 2
    tx = float(target["x"]) + float(target["w"]) / 2
    ty = float(target["y"]) + float(target["h"]) / 2
    dx, dy = tx - cx, ty - cy
    if abs(dx) >= abs(dy):
        return (float(node["x"]) + (float(node["w"]) if dx >= 0 else 0), cy)
    return (cx, float(node["y"]) + (float(node["h"]) if dy >= 0 else 0))


def render(spec: dict[str, Any], output_dir: Path) -> list[Path]:
    """Render a validated story specification and verify every emitted artifact."""
    figure_cfg = spec["figure"]
    palette = PALETTES[str(figure_cfg.get("palette", "indigo-amber"))]
    width = float(figure_cfg["width_in"])
    height = float(figure_cfg["height_in"])
    dpi = int(figure_cfg.get("dpi", 200))
    stem = str(figure_cfg["stem"])

    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
    fig.patch.set_facecolor(palette["background"])
    ax.set_facecolor(palette["background"])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    title = str(figure_cfg.get("title", ""))
    subtitle = str(figure_cfg.get("subtitle", ""))
    if title:
        ax.text(0.03, 0.965, title, ha="left", va="top", fontsize=15, fontweight="bold", color=palette["ink"])
    if subtitle:
        ax.text(0.03, 0.905, subtitle, ha="left", va="top", fontsize=8.8, color=palette["muted"])

    for stage in spec.get("stages", []):
        patch = FancyBboxPatch(
            (float(stage["x"]), float(stage["y"])),
            float(stage["w"]),
            float(stage["h"]),
            boxstyle="round,pad=0.008,rounding_size=0.018",
            linewidth=0.8,
            edgecolor="#D7DCE5",
            facecolor=str(stage.get("color", palette["stage"])),
            zorder=0,
        )
        ax.add_patch(patch)
        ax.text(
            float(stage["x"]) + 0.012,
            float(stage["y"]) + float(stage["h"]) - 0.018,
            str(stage.get("label", "")),
            ha="left",
            va="top",
            fontsize=8,
            fontweight="bold",
            color=palette["muted"],
        )

    nodes = {str(node["id"]): node for node in spec["nodes"]}
    for edge in spec.get("edges", []):
        source = nodes[str(edge["from"])]
        target = nodes[str(edge["to"])]
        start = anchor(source, target)
        end = anchor(target, source)
        style = str(edge.get("style", "flow"))
        linestyle = "--" if style in {"supervision", "contrast"} else "-"
        color = "#B35A45" if style == "contrast" else palette["accent"]
        curve = float(edge.get("curve", -0.22 if style == "feedback" else 0.0))
        arrow = FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=12,
            linewidth=1.5,
            linestyle=linestyle,
            color=color,
            connectionstyle=f"arc3,rad={curve}",
            shrinkA=2,
            shrinkB=2,
            zorder=2,
        )
        ax.add_patch(arrow)
        label = str(edge.get("label", "")).strip()
        if label:
            mx = float(edge.get("label_x", (start[0] + end[0]) / 2))
            my = float(
                edge.get(
                    "label_y",
                    (start[1] + end[1]) / 2 + float(edge.get("label_dy", 0.025)),
                )
            )
            ax.text(mx, my, label, ha="center", va="bottom", fontsize=7.5, color=color, zorder=4)

    for node in spec["nodes"]:
        role = str(node.get("role", "state"))
        emphasized = bool(node.get("emphasis", False))
        patch = FancyBboxPatch(
            (float(node["x"]), float(node["y"])),
            float(node["w"]),
            float(node["h"]),
            boxstyle="round,pad=0.01,rounding_size=0.02",
            linewidth=2.1 if emphasized else 1.15,
            edgecolor=palette["accent"] if emphasized else palette["ink"],
            facecolor=palette[role],
            zorder=3,
        )
        ax.add_patch(patch)
        cx = float(node["x"]) + float(node["w"]) / 2
        cy = float(node["y"]) + float(node["h"]) / 2
        label = textwrap.fill(str(node["label"]), width=int(node.get("wrap", 18)))
        detail = str(node.get("detail", "")).strip()
        ax.text(
            cx,
            cy + (0.022 if detail else 0),
            label,
            ha="center",
            va="center",
            fontsize=float(node.get("font_size", 9.2)),
            fontweight="bold" if emphasized else "semibold",
            color=palette["ink"],
            zorder=4,
        )
        if detail:
            ax.text(
                cx,
                float(node["y"]) + 0.028,
                textwrap.fill(detail, width=int(node.get("detail_wrap", 28))),
                ha="center",
                va="bottom",
                fontsize=6.9,
                color=palette["muted"],
                zorder=4,
            )

    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f"{stem}-", dir=output_dir) as temporary:
        stage_dir = Path(temporary)
        source_path = stage_dir / f"{stem}.source.json"
        source_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        svg_path = stage_dir / f"{stem}.svg"
        pdf_path = stage_dir / f"{stem}.pdf"
        png_path = stage_dir / f"{stem}.png"
        fig.savefig(svg_path, format="svg", facecolor=palette["background"])
        fig.savefig(pdf_path, format="pdf", facecolor=palette["background"], metadata={"CreationDate": None, "ModDate": None})
        fig.savefig(png_path, format="png", facecolor=palette["background"], dpi=dpi)
        plt.close(fig)

        json.loads(source_path.read_text(encoding="utf-8"))
        ET.parse(svg_path)
        if not pdf_path.read_bytes().startswith(b"%PDF"):
            raise RuntimeError("PDF verification failed")
        image = mpimg.imread(png_path)
        if image.ndim not in (2, 3) or min(image.shape[:2]) < 100:
            raise RuntimeError("PNG verification failed")
        manifest = {
            "status": "verified",
            "renderer_version": VERSION,
            "data_status": spec["data_status"],
            "stem": stem,
            "pixel_dimensions": [int(image.shape[1]), int(image.shape[0])],
            "artifacts": [path.name for path in (source_path, svg_path, pdf_path, png_path)],
        }
        manifest_path = stage_dir / f"{stem}.manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

        emitted = []
        for path in (source_path, svg_path, pdf_path, png_path, manifest_path):
            destination = output_dir / path.name
            shutil.copy2(path, destination)
            emitted.append(destination)
    return emitted


def main() -> int:
    args = parse_args()
    spec = load_and_validate(args.spec)
    if args.validate_only:
        print(f"valid: {args.spec.resolve()}")
        return 0
    if args.output_dir is None:
        raise ValueError("--output-dir is required unless --validate-only is used")
    for path in render(spec, args.output_dir):
        print(path.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
