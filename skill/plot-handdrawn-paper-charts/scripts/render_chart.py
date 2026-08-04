#!/usr/bin/env python3
"""Render reproducible hand-drawn academic bar and line charts from JSON.

The renderer keeps data, visual choices, and exports together. It supports
horizontal bars, grouped bars, line plots, and multi-panel compositions; emits
editable PDF/SVG plus 300-dpi PNG; and writes a manifest with artifact hashes.
"""

from __future__ import annotations

import argparse
import colorsys
import hashlib
import json
import math
import platform
import re
import shutil
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Mapping, Sequence

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import is_color_like
from matplotlib import font_manager
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
import numpy as np


VERSION = "1.3.0"
SKILL_ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = SKILL_ROOT / "assets/fonts"

INK = "#252A34"
GRID = "#D9DEE7"
MUTED = "#667085"
PALETTE_SPECS: dict[str, dict[str, Any]] = {
    "ocean-blue": {
        "colors": ["#2B6188", "#90B5D0", "#4A8EBF", "#194666", "#8596A3", "#DEE7ED"],
        "roles": {
            "primary": "#2B6188", "secondary": "#90B5D0", "tertiary": "#4A8EBF",
            "accent": "#194666", "neutral": "#8596A3", "pale": "#DEE7ED",
        },
        "tone": "calm, familiar, technical",
        "best_for": "default general paper figures and two-method comparisons",
    },
    "ink-indigo": {
        "colors": ["#323C81", "#979DC9", "#5461B6", "#1F2761", "#8589A3", "#E0E1EB"],
        "roles": {
            "primary": "#323C81", "secondary": "#979DC9", "tertiary": "#5461B6",
            "accent": "#1F2761", "neutral": "#8589A3", "pale": "#E0E1EB",
        },
        "tone": "formal, focused, premium",
        "best_for": "headline results, method versus baseline, and compact figures",
    },
    "sage-green": {
        "colors": ["#4C743E", "#A9BEA2", "#75A465", "#345828", "#8CA385", "#E4E8E3"],
        "roles": {
            "primary": "#4C743E", "secondary": "#A9BEA2", "tertiary": "#75A465",
            "accent": "#345828", "neutral": "#8CA385", "pale": "#E4E8E3",
        },
        "tone": "gentle, editorial, human-centered",
        "best_for": "human evaluation, qualitative analysis, and behavioral studies",
    },
    "forest-green": {
        "colors": ["#2E8459", "#93CCB0", "#4FBA85", "#1C6340", "#85A394", "#DFECE6"],
        "roles": {
            "primary": "#2E8459", "secondary": "#93CCB0", "tertiary": "#4FBA85",
            "accent": "#1C6340", "neutral": "#85A394", "pale": "#DFECE6",
        },
        "tone": "grounded, robust, natural",
        "best_for": "efficiency, sustainability, robustness, and systems studies",
    },
    "lagoon-teal": {
        "colors": ["#2E847D", "#93CCC8", "#4FBAB1", "#1C635E", "#85A3A0", "#DFECEB"],
        "roles": {
            "primary": "#2E847D", "secondary": "#93CCC8", "tertiary": "#4FBAB1",
            "accent": "#1C635E", "neutral": "#85A3A0", "pale": "#DFECEB",
        },
        "tone": "fresh, contemporary, balanced",
        "best_for": "general comparisons, interfaces, and systems diagrams",
    },
    "plum-purple": {
        "colors": ["#783B73", "#C19FBE", "#A960A3", "#5B2556", "#A385A0", "#E9E2E8"],
        "roles": {
            "primary": "#783B73", "secondary": "#C19FBE", "tertiary": "#A960A3",
            "accent": "#5B2556", "neutral": "#A385A0", "pale": "#E9E2E8",
        },
        "tone": "distinctive, mature, creative",
        "best_for": "multimodal, cross-domain, and concept-oriented figures",
    },
    "lavender": {
        "colors": ["#593B78", "#B09FC1", "#8560A9", "#40255B", "#9485A3", "#E6E2E9"],
        "roles": {
            "primary": "#593B78", "secondary": "#B09FC1", "tertiary": "#8560A9",
            "accent": "#40255B", "neutral": "#9485A3", "pale": "#E6E2E9",
        },
        "tone": "soft, exploratory, elegant",
        "best_for": "qualitative studies, educational figures, and supporting analyses",
    },
    "dusty-rose": {
        "colors": ["#7F3440", "#C898A0", "#B35666", "#60202B", "#A3858A", "#EBE0E2"],
        "roles": {
            "primary": "#7F3440", "secondary": "#C898A0", "tertiary": "#B35666",
            "accent": "#60202B", "neutral": "#A3858A", "pale": "#EBE0E2",
        },
        "tone": "warm, restrained, narrative",
        "best_for": "preferences, error taxonomies, and human-centered comparisons",
    },
    "sunset-orange": {
        "colors": ["#8D5125", "#D4AA8C", "#C77A43", "#6A3916", "#A39185", "#EFE4DC"],
        "roles": {
            "primary": "#8D5125", "secondary": "#D4AA8C", "tertiary": "#C77A43",
            "accent": "#6A3916", "neutral": "#A39185", "pale": "#EFE4DC",
        },
        "tone": "warm, expressive, presentation-friendly",
        "best_for": "motivation figures, distributions, and visual storytelling",
    },
    "terracotta": {
        "colors": ["#84402E", "#CC9F93", "#BA644F", "#632A1C", "#A38B85", "#ECE2DF"],
        "roles": {
            "primary": "#84402E", "secondary": "#CC9F93", "tertiary": "#BA644F",
            "accent": "#632A1C", "neutral": "#A38B85", "pale": "#ECE2DF",
        },
        "tone": "warm, explanatory, hand-crafted",
        "best_for": "failure analysis, distributions, and reference-style panels",
    },
    "ochre-gold": {
        "colors": ["#896E29", "#D1BE8F", "#C29F47", "#675118", "#A39A85", "#EEE9DD"],
        "roles": {
            "primary": "#896E29", "secondary": "#D1BE8F", "tertiary": "#C29F47",
            "accent": "#675118", "neutral": "#A39A85", "pale": "#EEE9DD",
        },
        "tone": "classic, warm, understated",
        "best_for": "efficiency results, highlights, and historical comparisons",
    },
    "graphite": {
        "colors": ["#3F4650", "#9AA1AA", "#69717C", "#252A34", "#C3C9D0", "#E8EBEE"],
        "roles": {
            "primary": "#3F4650", "secondary": "#9AA1AA", "tertiary": "#69717C",
            "accent": "#252A34", "neutral": "#C3C9D0", "pale": "#E8EBEE",
        },
        "tone": "monochrome, print-first, understated",
        "best_for": "grayscale submissions, baselines, and secondary evidence",
    },
}
PALETTES: dict[str, list[str]] = {
    name: list(spec["colors"]) for name, spec in PALETTE_SPECS.items()
}
HATCHES = ["", "///", "xx", "..", "\\\\", "++"]
MARKERS = ["o", "s", "^", "D", "v", "P"]
SIZE_PRESETS: dict[str, tuple[float, float]] = {
    "single-column": (3.45, 2.35),
    "double-column": (7.10, 3.10),
    "double-column-grid": (7.10, 6.00),
}


def parse_args() -> argparse.Namespace:
    """Parse the chart specification, export location, and validation mode."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, help="JSON chart specification")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--stem", help="Override figure.stem from the specification")
    parser.add_argument(
        "--list-palettes",
        action="store_true",
        help="Print the curated palette catalog as JSON and exit",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate the specification without rendering artifacts",
    )
    parser.add_argument(
        "--no-grayscale",
        action="store_true",
        help="Skip the grayscale QA image",
    )
    return parser.parse_args()


def read_spec(path: Path) -> dict[str, Any]:
    """Read one UTF-8 JSON object and retain strict failures for malformed input."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError("the chart specification must be a JSON object")
    return payload


def require_mapping(value: Any, label: str) -> Mapping[str, Any]:
    """Return a mapping or raise a field-specific schema error."""
    if not isinstance(value, Mapping):
        raise TypeError(f"{label} must be an object")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    """Return a non-empty list or raise a field-specific schema error."""
    if not isinstance(value, list) or not value:
        raise TypeError(f"{label} must be a non-empty list")
    return value


def finite_number(
    value: Any,
    label: str,
    *,
    minimum: float | None = None,
    strict_minimum: bool = False,
) -> float:
    """Return one finite real number and enforce an optional lower bound."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be numeric")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    if minimum is not None:
        invalid = number <= minimum if strict_minimum else number < minimum
        if invalid:
            relation = "greater than" if strict_minimum else "at least"
            raise ValueError(f"{label} must be {relation} {minimum:g}")
    return number


def positive_integer(value: Any, label: str) -> int:
    """Return a positive integer without silently truncating floats or booleans."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{label} must be an integer")
    if value < 1:
        raise ValueError(f"{label} must be positive")
    return value


def integer_value(value: Any, label: str) -> int:
    """Return one integer without silently truncating floats or booleans."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{label} must be an integer")
    return value


def validate_color(value: Any, label: str) -> None:
    """Reject malformed Matplotlib color values during schema validation."""
    if not is_color_like(value):
        raise ValueError(f"{label} is not a valid color: {value!r}")


def optional_list(value: Any, label: str) -> list[Any]:
    """Return an explicitly supplied list, allowing an empty collection."""
    if not isinstance(value, list):
        raise TypeError(f"{label} must be a list")
    return value


def exact_list(value: Any, label: str, expected: int) -> list[Any]:
    """Return a non-empty list whose length matches its associated data."""
    items = require_list(value, label)
    if len(items) != expected:
        raise ValueError(f"{label} must contain exactly {expected} items")
    return items


def validate_stem(value: Any, label: str = "figure.stem") -> str:
    """Validate one filename stem without permitting path separators."""
    stem = str(value)
    if not re.fullmatch(r"[A-Za-z0-9._-]+", stem):
        raise ValueError(
            f"{label} may contain only letters, digits, dot, dash, and underscore"
        )
    return stem


def numeric_sequence(
    values: Sequence[Any], label: str, *, allow_none: bool = False
) -> np.ndarray:
    """Convert a sequence to floats while rejecting booleans and non-finite data."""
    converted: list[float] = []
    for index, value in enumerate(values):
        if value is None and allow_none:
            converted.append(np.nan)
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{label}[{index}] must be numeric")
        number = float(value)
        if not math.isfinite(number):
            raise ValueError(f"{label}[{index}] must be finite")
        converted.append(number)
    return np.asarray(converted, dtype=float)


def hex_rgb(color: str) -> tuple[float, float, float]:
    """Convert a six-digit hex color to normalized RGB."""
    return tuple(int(color[index : index + 2], 16) / 255.0 for index in (1, 3, 5))


def relative_luminance(color: str) -> float:
    """Compute WCAG relative luminance for a hex color."""
    converted = [
        channel / 12.92
        if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in hex_rgb(color)
    ]
    return 0.2126 * converted[0] + 0.7152 * converted[1] + 0.0722 * converted[2]


def palette_aesthetic_metrics(palette: Mapping[str, Any]) -> dict[str, float]:
    """Measure role separation, hue cohesion, pale lightness, and neutral restraint."""
    roles = require_mapping(palette["roles"], "palette roles")
    primary = hex_rgb(str(roles["primary"]))
    secondary = hex_rgb(str(roles["secondary"]))
    distance = math.sqrt(
        sum((left - right) ** 2 for left, right in zip(primary, secondary))
    )
    neutral_saturation = colorsys.rgb_to_hsv(*hex_rgb(str(roles["neutral"])))[1]
    primary_hue = colorsys.rgb_to_hsv(*primary)[0]
    hue_distances = []
    for color in roles.values():
        hue, saturation, _ = colorsys.rgb_to_hsv(*hex_rgb(str(color)))
        if saturation >= 0.05:
            raw_distance = abs(hue - primary_hue)
            hue_distances.append(min(raw_distance, 1.0 - raw_distance))
    return {
        "primary_secondary_rgb_distance": round(distance, 4),
        "max_role_hue_distance": round(max(hue_distances, default=0.0), 4),
        "pale_relative_luminance": round(relative_luminance(str(roles["pale"])), 4),
        "neutral_saturation": round(neutral_saturation, 4),
    }


def validate_palette_catalog() -> None:
    """Check that every curated palette has complete semantic roles and valid colors."""
    required_roles = {"primary", "secondary", "tertiary", "accent", "neutral", "pale"}
    color_pattern = re.compile(r"#[0-9A-Fa-f]{6}")
    for name, palette in PALETTE_SPECS.items():
        colors = palette.get("colors")
        roles = palette.get("roles")
        if not isinstance(colors, list) or len(colors) < 6 or len(colors) != len(set(colors)):
            raise ValueError(f"palette {name!r} needs at least six unique colors")
        if not isinstance(roles, Mapping) or set(roles) != required_roles:
            raise ValueError(f"palette {name!r} has incomplete semantic roles")
        for color in [*colors, *roles.values()]:
            if not isinstance(color, str) or not color_pattern.fullmatch(color):
                raise ValueError(f"palette {name!r} contains an invalid hex color")
        metrics = palette_aesthetic_metrics(palette)
        if metrics["primary_secondary_rgb_distance"] < 0.25:
            raise ValueError(f"palette {name!r} lacks primary-secondary separation")
        if metrics["max_role_hue_distance"] > 0.04:
            raise ValueError(f"palette {name!r} mixes unrelated hue families")
        if metrics["pale_relative_luminance"] < 0.65:
            raise ValueError(f"palette {name!r} has an overly dark pale role")
        if metrics["neutral_saturation"] > 0.32:
            raise ValueError(f"palette {name!r} has an overly saturated neutral role")


def validate_color_choice(
    item: Mapping[str, Any], palette_roles: Mapping[str, str], label: str
) -> None:
    """Validate one explicit color or semantic palette-role selection."""
    if "color" in item and "color_role" in item:
        raise ValueError(f"{label} must choose color or color_role, not both")
    if "color_role" in item and str(item["color_role"]) not in palette_roles:
        raise ValueError(
            f"{label}.color_role must be one of {', '.join(sorted(palette_roles))}"
        )
    for field in ("color", "edgecolor", "marker_facecolor", "marker_edgecolor"):
        if field in item:
            validate_color(item[field], f"{label}.{field}")


def validate_value_format(value: Any, label: str) -> None:
    """Check named or custom direct-label formats before rendering begins."""
    if not isinstance(value, str):
        raise TypeError(f"{label} must be a string")
    try:
        format_value(1.25, value)
    except (KeyError, ValueError, IndexError) as exc:
        raise ValueError(f"invalid {label}: {value!r}") from exc


def validate_common_panel(panel: Mapping[str, Any], panel_index: int) -> None:
    """Validate shared axes, legends, guides, annotations, and style enums.

    These checks intentionally run before Matplotlib creates a figure. They
    cover every shared field documented in ``references/chart-spec.md`` so
    ``--validate-only`` and a real render agree on the accepted schema.
    """
    label = f"panels[{panel_index}]"
    if panel.get("grid", None) not in {None, False, True, "none", "x", "y", "both"}:
        raise ValueError(f"{label}.grid must be x, y, both, none, true, or false")
    if str(panel.get("spines", "box")) not in {"box", "open", "none"}:
        raise ValueError(f"{label}.spines must be box, open, or none")

    for axis_name in ("x", "y"):
        limit_field = f"{axis_name}_lim"
        tick_field = f"{axis_name}_ticks"
        label_field = f"{axis_name}_tick_labels"
        format_field = f"{axis_name}_tick_format"
        if limit_field in panel:
            limits = exact_list(panel[limit_field], f"{label}.{limit_field}", 2)
            numbers = numeric_sequence(limits, f"{label}.{limit_field}")
            if numbers[0] == numbers[1]:
                raise ValueError(f"{label}.{limit_field} endpoints must differ")
        if tick_field in panel:
            ticks = optional_list(panel[tick_field], f"{label}.{tick_field}")
            numeric_sequence(ticks, f"{label}.{tick_field}")
        if label_field in panel:
            if tick_field not in panel:
                raise ValueError(f"{label}.{label_field} requires {tick_field}")
            tick_labels = optional_list(panel[label_field], f"{label}.{label_field}")
            if len(tick_labels) != len(panel[tick_field]):
                raise ValueError(
                    f"{label}.{label_field} must match {label}.{tick_field} length"
                )
        if format_field in panel:
            formatter(str(panel[format_field]))

    for field in ("ink", "grid_color"):
        if field in panel:
            validate_color(panel[field], f"{label}.{field}")

    if "legend" in panel and panel["legend"] is not False:
        legend = require_mapping(panel["legend"], f"{label}.legend")
        if "bbox_to_anchor" in legend:
            anchor = exact_list(
                legend["bbox_to_anchor"], f"{label}.legend.bbox_to_anchor", 2
            )
            numeric_sequence(anchor, f"{label}.legend.bbox_to_anchor")
        if "ncol" in legend:
            positive_integer(legend["ncol"], f"{label}.legend.ncol")

    guide_specs = (("vertical_guides", "x"), ("horizontal_guides", "y"))
    for collection_name, coordinate in guide_specs:
        guides = optional_list(panel.get(collection_name, []), f"{label}.{collection_name}")
        for guide_index, raw_guide in enumerate(guides):
            guide_label = f"{label}.{collection_name}[{guide_index}]"
            guide = require_mapping(raw_guide, guide_label)
            if coordinate not in guide:
                raise ValueError(f"{guide_label}.{coordinate} is required")
            finite_number(guide[coordinate], f"{guide_label}.{coordinate}")
            if "color" in guide:
                validate_color(guide["color"], f"{guide_label}.color")

    annotations = optional_list(panel.get("annotations", []), f"{label}.annotations")
    for annotation_index, raw_annotation in enumerate(annotations):
        annotation_label = f"{label}.annotations[{annotation_index}]"
        annotation = require_mapping(raw_annotation, annotation_label)
        for field in ("text", "x", "y"):
            if field not in annotation:
                raise ValueError(f"{annotation_label}.{field} is required")
        for field in ("x", "y", "text_x", "text_y"):
            if field in annotation:
                finite_number(annotation[field], f"{annotation_label}.{field}")
        if "color" in annotation:
            validate_color(annotation["color"], f"{annotation_label}.color")


def validate_spec(spec: Mapping[str, Any]) -> None:
    """Validate the complete figure before any output is created.

    The validation is intentionally structural rather than inferential: chart
    values are never guessed, normalized, or silently dropped. Every category,
    x position, series value, uncertainty bound, and highlight index must agree
    with the declared panel dimensions.
    """
    validate_palette_catalog()
    figure = require_mapping(spec.get("figure", {}), "figure")
    if "stem" in figure:
        validate_stem(figure["stem"])
    figure_palette_name = str(figure.get("palette", "ocean-blue"))
    if figure_palette_name not in PALETTE_SPECS:
        raise ValueError(f"unknown figure.palette: {figure_palette_name}")
    rows = positive_integer(figure.get("rows", 1), "figure.rows")
    cols = positive_integer(figure.get("cols", 1), "figure.cols")
    if str(figure.get("sketch", "subtle")) not in {"none", "subtle", "rough"}:
        raise ValueError("figure.sketch must be none, subtle, or rough")
    if ("width_in" in figure) != ("height_in" in figure):
        raise ValueError("figure.width_in and figure.height_in must be provided together")
    if "width_in" in figure:
        finite_number(figure["width_in"], "figure.width_in", minimum=0, strict_minimum=True)
        finite_number(
            figure["height_in"], "figure.height_in", minimum=0, strict_minimum=True
        )
    elif str(figure.get("size", "single-column")) not in SIZE_PRESETS:
        raise ValueError(f"unknown figure.size preset: {figure.get('size')}")
    if "dpi" in figure:
        positive_integer(figure["dpi"], "figure.dpi")
    for field in ("font_size", "title_size", "label_size", "tick_size", "legend_size"):
        if field in figure:
            finite_number(figure[field], f"figure.{field}", minimum=0, strict_minimum=True)
    for field in ("wspace", "hspace", "w_pad", "h_pad"):
        if field in figure:
            finite_number(figure[field], f"figure.{field}", minimum=0)
    for field in ("ink", "background"):
        if field in figure:
            validate_color(figure[field], f"figure.{field}")

    panels = require_list(spec.get("panels"), "panels")
    if len(panels) > rows * cols:
        raise ValueError("the panel count exceeds figure.rows × figure.cols")

    for panel_index, raw_panel in enumerate(panels):
        panel = require_mapping(raw_panel, f"panels[{panel_index}]")
        panel_palette_name = str(panel.get("palette", figure_palette_name))
        if panel_palette_name not in PALETTE_SPECS:
            raise ValueError(f"unknown panels[{panel_index}].palette: {panel_palette_name}")
        palette_roles = require_mapping(
            PALETTE_SPECS[panel_palette_name]["roles"], f"palette {panel_palette_name} roles"
        )
        validate_common_panel(panel, panel_index)
        chart_type = panel.get("type")
        if chart_type not in {"horizontal_bar", "grouped_bar", "line"}:
            raise ValueError(
                f"panels[{panel_index}].type must be horizontal_bar, grouped_bar, or line"
            )

        if chart_type == "horizontal_bar":
            labels = require_list(panel.get("labels"), f"panels[{panel_index}].labels")
            values = require_list(panel.get("values"), f"panels[{panel_index}].values")
            numeric_sequence(values, f"panels[{panel_index}].values")
            if len(labels) != len(values):
                raise ValueError(f"panels[{panel_index}] labels and values differ in length")
            if len({str(label) for label in labels}) != len(labels):
                raise ValueError(f"panels[{panel_index}] labels must be unique")
            for field in ("colors", "hatches"):
                if field in panel:
                    items = exact_list(
                        panel[field], f"panels[{panel_index}].{field}", len(values)
                    )
                    if field == "colors":
                        for item_index, color in enumerate(items):
                            validate_color(
                                color, f"panels[{panel_index}].colors[{item_index}]"
                            )
            if "color_roles" in panel:
                if "colors" in panel:
                    raise ValueError(
                        f"panels[{panel_index}] must choose colors or color_roles, not both"
                    )
                color_roles = require_list(
                    panel["color_roles"], f"panels[{panel_index}].color_roles"
                )
                if len(color_roles) != len(values):
                    raise ValueError(
                        f"panels[{panel_index}] color_roles and values differ in length"
                    )
                for role in color_roles:
                    if str(role) not in palette_roles:
                        raise ValueError(
                            f"panels[{panel_index}] unknown color role: {role}"
                        )
            if str(panel.get("sort", "none")) not in {"none", "ascending", "descending"}:
                raise ValueError(
                    f"panels[{panel_index}].sort must be none, ascending, or descending"
                )
            if str(panel.get("label_mode", "axis")) not in {"axis", "legend"}:
                raise ValueError(f"panels[{panel_index}].label_mode must be axis or legend")
            if "value_format" in panel:
                validate_value_format(
                    panel["value_format"], f"panels[{panel_index}].value_format"
                )

        if chart_type == "grouped_bar":
            categories = require_list(
                panel.get("categories"), f"panels[{panel_index}].categories"
            )
            series = require_list(panel.get("series"), f"panels[{panel_index}].series")
            if len({str(category) for category in categories}) != len(categories):
                raise ValueError(f"panels[{panel_index}] categories must be unique")
            for field in ("colors", "hatches"):
                if field in panel:
                    items = exact_list(
                        panel[field], f"panels[{panel_index}].{field}", len(series)
                    )
                    if field == "colors":
                        for item_index, color in enumerate(items):
                            validate_color(
                                color, f"panels[{panel_index}].colors[{item_index}]"
                            )
            names: list[str] = []
            for series_index, raw_series in enumerate(series):
                item = require_mapping(
                    raw_series, f"panels[{panel_index}].series[{series_index}]"
                )
                name = str(item.get("name", "")).strip()
                if not name:
                    raise ValueError(
                        f"panels[{panel_index}].series[{series_index}].name is required"
                    )
                names.append(name)
                validate_color_choice(
                    item,
                    palette_roles,
                    f"panels[{panel_index}].series[{series_index}]",
                )
                values = require_list(
                    item.get("values"),
                    f"panels[{panel_index}].series[{series_index}].values",
                )
                numeric_sequence(
                    values, f"panels[{panel_index}].series[{series_index}].values"
                )
                if len(values) != len(categories):
                    raise ValueError(
                        f"panels[{panel_index}] series {name!r} does not match categories"
                    )
                if "errors" in item:
                    errors = require_list(
                        item["errors"],
                        f"panels[{panel_index}].series[{series_index}].errors",
                    )
                    error_values = numeric_sequence(
                        errors, f"panels[{panel_index}].series[{series_index}].errors"
                    )
                    if len(errors) != len(categories):
                        raise ValueError(
                            f"panels[{panel_index}] error bars for {name!r} have wrong length"
                        )
                    if np.any(error_values < 0):
                        raise ValueError(
                            f"panels[{panel_index}] error bars for {name!r} must be non-negative"
                        )
            if len(set(names)) != len(names):
                raise ValueError(f"panels[{panel_index}] series names must be unique")
            if "value_format" in panel:
                validate_value_format(
                    panel["value_format"], f"panels[{panel_index}].value_format"
                )

        if chart_type == "line":
            x = require_list(panel.get("x"), f"panels[{panel_index}].x")
            numeric_sequence(x, f"panels[{panel_index}].x")
            series = require_list(panel.get("series"), f"panels[{panel_index}].series")
            if "colors" in panel:
                colors = exact_list(
                    panel["colors"], f"panels[{panel_index}].colors", len(series)
                )
                for color_index, color in enumerate(colors):
                    validate_color(color, f"panels[{panel_index}].colors[{color_index}]")
            names = []
            values_by_name: dict[str, np.ndarray] = {}
            for series_index, raw_series in enumerate(series):
                item = require_mapping(
                    raw_series, f"panels[{panel_index}].series[{series_index}]"
                )
                name = str(item.get("name", "")).strip()
                if not name:
                    raise ValueError(
                        f"panels[{panel_index}].series[{series_index}].name is required"
                    )
                names.append(name)
                validate_color_choice(
                    item,
                    palette_roles,
                    f"panels[{panel_index}].series[{series_index}]",
                )
                values = require_list(
                    item.get("values"),
                    f"panels[{panel_index}].series[{series_index}].values",
                )
                value_numbers = numeric_sequence(
                    values,
                    f"panels[{panel_index}].series[{series_index}].values",
                    allow_none=True,
                )
                values_by_name[name] = value_numbers
                if len(values) != len(x):
                    raise ValueError(
                        f"panels[{panel_index}] series {name!r} does not match x"
                    )
                bounds: dict[str, np.ndarray] = {}
                for bound_name in ("lower", "upper"):
                    if bound_name in item:
                        bound = require_list(
                            item[bound_name],
                            f"panels[{panel_index}].series[{series_index}].{bound_name}",
                        )
                        bound_numbers = numeric_sequence(
                            bound,
                            f"panels[{panel_index}].series[{series_index}].{bound_name}",
                            allow_none=True,
                        )
                        bounds[bound_name] = bound_numbers
                        if len(bound) != len(x):
                            raise ValueError(
                                f"panels[{panel_index}] {bound_name} for {name!r} has wrong length"
                            )
                if ("lower" in item) != ("upper" in item):
                    raise ValueError(
                        f"panels[{panel_index}] series {name!r} needs both lower and upper"
                    )
                if len(bounds) == 2:
                    lower = bounds["lower"]
                    upper = bounds["upper"]
                    if not np.array_equal(np.isnan(lower), np.isnan(upper)):
                        raise ValueError(
                            f"panels[{panel_index}] bounds for {name!r} "
                            "need matching null positions"
                        )
                    finite_mask = np.isfinite(lower) & np.isfinite(upper)
                    if np.any(lower[finite_mask] > upper[finite_mask]):
                        raise ValueError(
                            f"panels[{panel_index}] lower bound exceeds upper for {name!r}"
                        )
                    estimate_mask = finite_mask & np.isfinite(value_numbers)
                    if np.any(value_numbers[estimate_mask] < lower[estimate_mask]) or np.any(
                        value_numbers[estimate_mask] > upper[estimate_mask]
                    ):
                        raise ValueError(
                            f"panels[{panel_index}] estimate falls outside bounds for {name!r}"
                        )
            if len(set(names)) != len(names):
                raise ValueError(f"panels[{panel_index}] series names must be unique")
            highlights = optional_list(
                panel.get("highlights", []), f"panels[{panel_index}].highlights"
            )
            for highlight_index, raw_highlight in enumerate(highlights):
                highlight = require_mapping(
                    raw_highlight, f"panels[{panel_index}].highlights[{highlight_index}]"
                )
                if str(highlight.get("series")) not in names:
                    raise ValueError(
                        f"panels[{panel_index}] highlight references an unknown series"
                    )
                index = integer_value(
                    highlight.get("index", -1),
                    f"panels[{panel_index}].highlights[{highlight_index}].index",
                )
                if not -len(x) <= index < len(x):
                    raise IndexError(f"panels[{panel_index}] highlight index is out of range")
                series_name = str(highlight.get("series"))
                if np.isnan(values_by_name[series_name][index]):
                    raise ValueError(
                        f"panels[{panel_index}] highlight for {series_name!r} points to null"
                    )
                for color_field in ("facecolor", "edgecolor"):
                    if color_field in highlight:
                        validate_color(
                            highlight[color_field],
                            f"panels[{panel_index}].highlights[{highlight_index}].{color_field}",
                        )


def install_bundled_fonts() -> None:
    """Register bundled open fonts without mutating the operating system."""
    if FONT_DIR.is_dir():
        for font_path in sorted(FONT_DIR.glob("*.ttf")):
            font_manager.fontManager.addfont(str(font_path))


def choose_font(requested: str | None) -> str:
    """Choose the requested or first available hand-lettered font."""
    install_bundled_fonts()
    available = {entry.name for entry in font_manager.fontManager.ttflist}
    candidates = [requested] if requested else []
    candidates.extend(["Comic Neue", "Comic Sans MS", "Chalkboard", "DejaVu Sans"])
    for candidate in candidates:
        if candidate and candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_style(figure_spec: Mapping[str, Any], font_name: str) -> None:
    """Apply a restrained hand-drawn grammar suitable for vector paper figures."""
    sketch = str(figure_spec.get("sketch", "subtle"))
    sketch_value: tuple[float, float, float] | None
    if sketch == "none":
        sketch_value = None
    elif sketch == "subtle":
        sketch_value = (0.55, 120.0, 1.35)
    elif sketch == "rough":
        sketch_value = (1.0, 95.0, 2.1)
    else:
        raise ValueError("figure.sketch must be none, subtle, or rough")

    base_font = float(figure_spec.get("font_size", 8.0))
    plt.rcParams.update(
        {
            "font.family": font_name,
            "font.size": base_font,
            "axes.titlesize": float(figure_spec.get("title_size", base_font + 3.0)),
            "axes.labelsize": float(figure_spec.get("label_size", base_font + 0.2)),
            "xtick.labelsize": float(figure_spec.get("tick_size", base_font - 0.3)),
            "ytick.labelsize": float(figure_spec.get("tick_size", base_font - 0.3)),
            "legend.fontsize": float(figure_spec.get("legend_size", base_font - 0.5)),
            "axes.linewidth": float(figure_spec.get("axes_linewidth", 1.15)),
            "axes.edgecolor": str(figure_spec.get("ink", INK)),
            "hatch.linewidth": float(figure_spec.get("hatch_linewidth", 0.9)),
            "path.sketch": sketch_value,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "plot-handdrawn-paper-charts-v1",
            "savefig.facecolor": str(figure_spec.get("background", "white")),
        }
    )


def formatter(name: str | None) -> FuncFormatter | None:
    """Create stable tick formatting for display-unit numeric values."""
    if not name or name == "number":
        return None
    if name == "percent":
        return FuncFormatter(lambda value, _: f"{value:g}%")
    if name == "integer":
        return FuncFormatter(lambda value, _: f"{value:.0f}")
    if name == "one_decimal":
        return FuncFormatter(lambda value, _: f"{value:.1f}")
    if name == "k":
        return FuncFormatter(lambda value, _: f"{value:g}K")
    raise ValueError(f"unknown tick format: {name}")


def format_value(value: float, format_spec: str | None) -> str:
    """Format a direct value label without changing its numeric scale."""
    if not format_spec or format_spec == "number":
        return f"{value:g}"
    if format_spec == "percent":
        return f"{value:g}%"
    if format_spec == "integer":
        return f"{value:.0f}"
    if format_spec == "one_decimal":
        return f"{value:.1f}"
    if "{" in format_spec:
        return format_spec.format(value=value)
    raise ValueError(f"unknown value format: {format_spec}")


def colors_for(count: int, palette: Sequence[str], explicit: Any = None) -> list[str]:
    """Return exactly one color per visual item, cycling only when necessary."""
    source = explicit if isinstance(explicit, list) and explicit else palette
    return [str(source[index % len(source)]) for index in range(count)]


def role_colors(role_names: Sequence[Any], palette_roles: Mapping[str, str]) -> list[str]:
    """Resolve semantic role names to stable colors within one selected palette."""
    return [str(palette_roles[str(role)]) for role in role_names]


def item_color(
    item: Mapping[str, Any], default: str, palette_roles: Mapping[str, str]
) -> str:
    """Resolve a series color, preferring explicit hex then a semantic role."""
    if "color" in item:
        return str(item["color"])
    if "color_role" in item:
        return str(palette_roles[str(item["color_role"])])
    return default


def hatches_for(count: int, explicit: Any = None) -> list[str]:
    """Return one print-safe hatch per bar or series."""
    source = explicit if isinstance(explicit, list) and explicit else HATCHES
    return [str(source[index % len(source)]) for index in range(count)]


def apply_common_axis(axis: plt.Axes, panel: Mapping[str, Any], grid_axis: str) -> None:
    """Apply titles, scales, ticks, spines, grid, and optional panel lettering."""
    ink = str(panel.get("ink", INK))
    grid_color = str(panel.get("grid_color", GRID))
    axis.set_axisbelow(True)

    if panel.get("title"):
        axis.set_title(
            str(panel["title"]),
            loc=str(panel.get("title_loc", "center")),
            pad=float(panel.get("title_pad", 10.0)),
            fontweight=str(panel.get("title_weight", "bold")),
        )
    if panel.get("x_label"):
        axis.set_xlabel(
            str(panel["x_label"]),
            labelpad=float(panel.get("x_label_pad", 5.0)),
            fontweight=str(panel.get("axis_label_weight", "bold")),
        )
    if panel.get("y_label"):
        axis.set_ylabel(
            str(panel["y_label"]),
            labelpad=float(panel.get("y_label_pad", 5.0)),
            fontweight=str(panel.get("axis_label_weight", "bold")),
        )

    if "x_lim" in panel:
        axis.set_xlim(*numeric_sequence(panel["x_lim"], "x_lim"))
    if "y_lim" in panel:
        axis.set_ylim(*numeric_sequence(panel["y_lim"], "y_lim"))
    if "x_ticks" in panel:
        axis.set_xticks(numeric_sequence(panel["x_ticks"], "x_ticks"))
    if "y_ticks" in panel:
        axis.set_yticks(numeric_sequence(panel["y_ticks"], "y_ticks"))
    if "x_tick_labels" in panel:
        axis.set_xticklabels([str(value) for value in panel["x_tick_labels"]])
    else:
        x_formatter = formatter(panel.get("x_tick_format"))
        if x_formatter:
            axis.xaxis.set_major_formatter(x_formatter)
    if "y_tick_labels" in panel:
        axis.set_yticklabels([str(value) for value in panel["y_tick_labels"]])
    else:
        y_formatter = formatter(panel.get("y_tick_format"))
        if y_formatter:
            axis.yaxis.set_major_formatter(y_formatter)

    grid = panel.get("grid", grid_axis)
    if grid is True:
        grid = grid_axis
    if grid not in {False, "none", None}:
        axis.grid(
            axis=str(grid),
            color=grid_color,
            linewidth=float(panel.get("grid_linewidth", 0.55)),
            alpha=float(panel.get("grid_alpha", 0.72)),
            zorder=0,
        )

    spine_mode = str(panel.get("spines", "box"))
    if spine_mode == "open":
        axis.spines[["top", "right"]].set_visible(False)
    elif spine_mode == "none":
        for spine in axis.spines.values():
            spine.set_visible(False)
    elif spine_mode != "box":
        raise ValueError("panel.spines must be box, open, or none")
    for spine in axis.spines.values():
        spine.set_color(ink)
        spine.set_linewidth(float(panel.get("spine_linewidth", 1.15)))
    axis.tick_params(
        color=ink,
        width=float(panel.get("tick_width", 0.95)),
        length=float(panel.get("tick_length", 3.0)),
        pad=float(panel.get("tick_pad", 2.0)),
    )
    if panel.get("x_tick_rotation") is not None:
        axis.tick_params(axis="x", labelrotation=float(panel["x_tick_rotation"]))
    if panel.get("panel_label"):
        axis.text(
            float(panel.get("panel_label_x", -0.10)),
            float(panel.get("panel_label_y", 1.08)),
            str(panel["panel_label"]),
            transform=axis.transAxes,
            ha="left",
            va="bottom",
            fontweight="bold",
        )


def apply_legend(
    axis: plt.Axes,
    panel: Mapping[str, Any],
    *,
    handles: Sequence[Any] | None = None,
) -> None:
    """Draw one compact, frameless legend from a small supported option set."""
    raw_config = panel.get("legend", {})
    if raw_config is False:
        return
    config = require_mapping(raw_config, "legend") if raw_config else {}
    kwargs: dict[str, Any] = {
        "loc": str(config.get("loc", "best")),
        "frameon": bool(config.get("frameon", False)),
        "ncol": int(config.get("ncol", 1)),
        "handlelength": float(config.get("handlelength", 1.7)),
        "handletextpad": float(config.get("handletextpad", 0.55)),
        "labelspacing": float(config.get("labelspacing", 0.3)),
        "columnspacing": float(config.get("columnspacing", 0.9)),
        "borderaxespad": float(config.get("borderaxespad", 0.2)),
    }
    if "fontsize" in config:
        kwargs["fontsize"] = float(config["fontsize"])
    if "bbox_to_anchor" in config:
        kwargs["bbox_to_anchor"] = tuple(config["bbox_to_anchor"])
    if "title" in config:
        kwargs["title"] = str(config["title"])
    axis.legend(handles=handles, **kwargs)


def draw_horizontal_bar(
    axis: plt.Axes,
    panel: Mapping[str, Any],
    palette: Sequence[str],
    palette_roles: Mapping[str, str],
) -> None:
    """Draw horizontal bars with axis labels or an in-panel category legend."""
    labels = [str(value) for value in panel["labels"]]
    values = numeric_sequence(panel["values"], "values")
    if "color_roles" in panel:
        colors = role_colors(panel["color_roles"], palette_roles)
    else:
        colors = colors_for(len(values), palette, panel.get("colors"))
    hatches = hatches_for(len(values), panel.get("hatches"))

    order = list(range(len(values)))
    sort_mode = str(panel.get("sort", "none"))
    if sort_mode == "descending":
        order.sort(key=lambda index: values[index], reverse=True)
    elif sort_mode == "ascending":
        order.sort(key=lambda index: values[index])
    elif sort_mode != "none":
        raise ValueError("horizontal_bar.sort must be none, ascending, or descending")
    labels = [labels[index] for index in order]
    values = values[order]
    colors = [colors[index] for index in order]
    hatches = [hatches[index] for index in order]

    positions = np.arange(len(labels))
    bars = axis.barh(
        positions,
        values,
        height=float(panel.get("bar_height", 0.62)),
        color=colors,
        edgecolor=str(panel.get("ink", INK)),
        linewidth=float(panel.get("bar_linewidth", 1.05)),
        zorder=3,
    )
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
    axis.invert_yaxis()

    label_mode = str(panel.get("label_mode", "axis"))
    if label_mode == "axis":
        axis.set_yticks(positions, labels)
    elif label_mode == "legend":
        axis.set_yticks([])
    else:
        raise ValueError("horizontal_bar.label_mode must be axis or legend")

    if "x_lim" not in panel:
        minimum = min(0.0, float(np.min(values)))
        maximum = max(0.0, float(np.max(values)))
        raw_span = maximum - minimum
        span = raw_span if raw_span > 0 else max(abs(minimum), abs(maximum), 1.0)
        label_fraction = 0.16 if panel.get("value_labels", False) else 0.06
        left = minimum - label_fraction * span if minimum < 0 else 0.0
        right = maximum + label_fraction * span if maximum > 0 else 0.0
        if left == right:
            right = 1.0
        axis.set_xlim(left, right)
    apply_common_axis(axis, panel, "x")

    if panel.get("value_labels", False):
        span = axis.get_xlim()[1] - axis.get_xlim()[0]
        for bar, value in zip(bars, values):
            positive = value >= 0
            axis.text(
                value + (0.012 * span if positive else -0.012 * span),
                bar.get_y() + bar.get_height() / 2,
                format_value(float(value), panel.get("value_format")),
                ha="left" if positive else "right",
                va="center",
                color=str(panel.get("ink", INK)),
                clip_on=False,
            )

    if label_mode == "legend":
        handles = [
            Patch(
                facecolor=color,
                edgecolor=str(panel.get("ink", INK)),
                linewidth=0.9,
                hatch=hatch,
                label=label,
            )
            for label, color, hatch in zip(labels, colors, hatches)
        ]
        apply_legend(axis, panel, handles=handles)
    draw_annotations(axis, panel)


def draw_grouped_bar(
    axis: plt.Axes,
    panel: Mapping[str, Any],
    palette: Sequence[str],
    palette_roles: Mapping[str, str],
) -> None:
    """Draw grouped bars with optional errors, outside value labels, and hatches."""
    categories = [str(value) for value in panel["categories"]]
    series = [require_mapping(value, "series") for value in panel["series"]]
    colors = colors_for(len(series), palette, panel.get("colors"))
    hatches = hatches_for(len(series), panel.get("hatches"))
    x = np.arange(len(categories), dtype=float)
    group_width = float(panel.get("group_width", 0.76))
    width = group_width / len(series)

    for index, item in enumerate(series):
        values = numeric_sequence(item["values"], f"{item['name']}.values")
        offset = (index - (len(series) - 1) / 2.0) * width
        errors = None
        if "errors" in item:
            errors = numeric_sequence(item["errors"], f"{item['name']}.errors")
        bars = axis.bar(
            x + offset,
            values,
            width * float(panel.get("bar_width_fraction", 0.92)),
            yerr=errors,
            capsize=float(panel.get("error_capsize", 2.2)) if errors is not None else 0,
            color=item_color(item, colors[index], palette_roles),
            edgecolor=str(item.get("edgecolor", panel.get("ink", INK))),
            linewidth=float(item.get("linewidth", panel.get("bar_linewidth", 1.05))),
            hatch=str(item.get("hatch", hatches[index])),
            label=str(item["name"]),
            zorder=3,
        )
        if panel.get("value_labels", False):
            for bar, value in zip(bars, values):
                positive = value >= 0
                axis.text(
                    bar.get_x() + bar.get_width() / 2,
                    value,
                    format_value(float(value), panel.get("value_format")),
                    ha="center",
                    va="bottom" if positive else "top",
                    color=str(panel.get("ink", INK)),
                    clip_on=False,
                )

    axis.set_xticks(x, categories)
    apply_common_axis(axis, panel, "y")
    apply_legend(axis, panel)
    draw_annotations(axis, panel)


def draw_guides(axis: plt.Axes, panel: Mapping[str, Any]) -> None:
    """Draw semantic vertical or horizontal guides without changing data values."""
    for raw_guide in panel.get("vertical_guides", []):
        guide = require_mapping(raw_guide, "vertical_guide")
        x_value = float(guide["x"])
        axis.axvline(
            x_value,
            color=str(guide.get("color", "#B87945")),
            linewidth=float(guide.get("linewidth", 1.0)),
            linestyle=guide.get("linestyle", (0, (3.0, 3.0))),
            alpha=float(guide.get("alpha", 0.9)),
            zorder=1,
        )
        if guide.get("label"):
            axis.text(
                x_value,
                float(guide.get("label_y", 0.98)),
                str(guide["label"]),
                transform=axis.get_xaxis_transform(),
                ha=str(guide.get("ha", "center")),
                va="top",
                color=str(guide.get("color", MUTED)),
            )
    for raw_guide in panel.get("horizontal_guides", []):
        guide = require_mapping(raw_guide, "horizontal_guide")
        y_value = float(guide["y"])
        axis.axhline(
            y_value,
            color=str(guide.get("color", MUTED)),
            linewidth=float(guide.get("linewidth", 1.0)),
            linestyle=guide.get("linestyle", (0, (4.0, 2.4))),
            alpha=float(guide.get("alpha", 0.9)),
            zorder=1,
        )
        if guide.get("label"):
            axis.text(
                float(guide.get("label_x", 0.02)),
                y_value,
                str(guide["label"]),
                transform=axis.get_yaxis_transform(),
                ha="left",
                va=str(guide.get("va", "bottom")),
                color=str(guide.get("color", MUTED)),
            )


def draw_annotations(axis: plt.Axes, panel: Mapping[str, Any]) -> None:
    """Place explicitly anchored annotations supplied by the chart specification."""
    for raw_annotation in panel.get("annotations", []):
        annotation = require_mapping(raw_annotation, "annotation")
        axis.annotate(
            str(annotation["text"]),
            xy=(float(annotation["x"]), float(annotation["y"])),
            xytext=(
                float(annotation.get("text_x", annotation["x"])),
                float(annotation.get("text_y", annotation["y"])),
            ),
            ha=str(annotation.get("ha", "center")),
            va=str(annotation.get("va", "bottom")),
            color=str(annotation.get("color", INK)),
            arrowprops=(
                {
                    "arrowstyle": str(annotation.get("arrowstyle", "->")),
                    "color": str(annotation.get("color", INK)),
                    "linewidth": float(annotation.get("linewidth", 0.9)),
                }
                if annotation.get("arrow", False)
                else None
            ),
        )


def draw_line(
    axis: plt.Axes,
    panel: Mapping[str, Any],
    palette: Sequence[str],
    palette_roles: Mapping[str, str],
) -> None:
    """Draw complete or gapped series, uncertainty bands, guides, and highlights."""
    x = numeric_sequence(panel["x"], "x")
    series = [require_mapping(value, "series") for value in panel["series"]]
    colors = colors_for(len(series), palette, panel.get("colors"))
    values_by_name: dict[str, np.ndarray] = {}
    color_by_name: dict[str, str] = {}

    draw_guides(axis, panel)
    for index, item in enumerate(series):
        name = str(item["name"])
        values = numeric_sequence(item["values"], f"{name}.values", allow_none=True)
        color = item_color(item, colors[index], palette_roles)
        values_by_name[name] = values
        color_by_name[name] = color

        if "lower" in item and "upper" in item:
            lower = numeric_sequence(item["lower"], f"{name}.lower", allow_none=True)
            upper = numeric_sequence(item["upper"], f"{name}.upper", allow_none=True)
            axis.fill_between(
                x,
                lower,
                upper,
                color=color,
                alpha=float(item.get("band_alpha", 0.15)),
                linewidth=0,
                zorder=1,
            )

        marker = str(item.get("marker", MARKERS[index % len(MARKERS)]))
        marker_face = str(item.get("marker_facecolor", "white"))
        axis.plot(
            x,
            values,
            color=color,
            linewidth=float(item.get("linewidth", 1.9)),
            linestyle=item.get("linestyle", "-"),
            marker=marker,
            markersize=float(item.get("markersize", 4.8)),
            markerfacecolor=marker_face,
            markeredgecolor=str(item.get("marker_edgecolor", color)),
            markeredgewidth=float(item.get("marker_edgewidth", 1.0)),
            markevery=item.get("markevery", None),
            label=name,
            zorder=int(item.get("zorder", 3)),
        )

    apply_common_axis(axis, panel, "both")
    for raw_highlight in panel.get("highlights", []):
        highlight = require_mapping(raw_highlight, "highlight")
        name = str(highlight["series"])
        index = int(highlight.get("index", -1))
        value = values_by_name[name][index]
        if np.isnan(value):
            raise ValueError(f"highlight for {name!r} points to a null value")
        axis.scatter(
            [x[index]],
            [value],
            marker=str(highlight.get("marker", "*")),
            s=float(highlight.get("size", 150.0)),
            facecolor=str(highlight.get("facecolor", color_by_name[name])),
            edgecolor=str(highlight.get("edgecolor", panel.get("ink", INK))),
            linewidth=float(highlight.get("linewidth", 1.0)),
            zorder=int(highlight.get("zorder", 7)),
            clip_on=False,
        )
    draw_annotations(axis, panel)
    apply_legend(axis, panel)


def figure_size(figure_spec: Mapping[str, Any]) -> tuple[float, float]:
    """Resolve an explicit size or one of the paper-column presets."""
    if "width_in" in figure_spec or "height_in" in figure_spec:
        if "width_in" not in figure_spec or "height_in" not in figure_spec:
            raise ValueError("figure.width_in and figure.height_in must be provided together")
        return float(figure_spec["width_in"]), float(figure_spec["height_in"])
    preset = str(figure_spec.get("size", "single-column"))
    if preset not in SIZE_PRESETS:
        raise ValueError(f"unknown figure.size preset: {preset}")
    return SIZE_PRESETS[preset]


def render_figure(spec: Mapping[str, Any]) -> tuple[plt.Figure, str, tuple[float, float]]:
    """Create the grid, dispatch each panel renderer, and return resolved metadata."""
    figure_spec = require_mapping(spec.get("figure", {}), "figure")
    font_name = choose_font(
        str(figure_spec["font_family"]) if figure_spec.get("font_family") else None
    )
    configure_style(figure_spec, font_name)
    size = figure_size(figure_spec)
    rows = int(figure_spec.get("rows", 1))
    cols = int(figure_spec.get("cols", 1))
    palette_name = str(figure_spec.get("palette", "ocean-blue"))
    if palette_name not in PALETTES:
        raise ValueError(f"unknown figure.palette: {palette_name}")
    palette = PALETTES[palette_name]

    figure, axes = plt.subplots(
        rows,
        cols,
        figsize=size,
        squeeze=False,
        sharex=bool(figure_spec.get("sharex", False)),
        sharey=bool(figure_spec.get("sharey", False)),
        layout="constrained",
        facecolor=str(figure_spec.get("background", "white")),
    )
    figure.set_constrained_layout_pads(
        w_pad=float(figure_spec.get("w_pad", 0.055)),
        h_pad=float(figure_spec.get("h_pad", 0.055)),
        wspace=float(figure_spec.get("wspace", 0.08)),
        hspace=float(figure_spec.get("hspace", 0.10)),
    )
    if figure_spec.get("title"):
        figure.suptitle(
            str(figure_spec["title"]),
            fontweight="bold",
            fontsize=float(figure_spec.get("suptitle_size", 13.0)),
        )

    panels = list(spec["panels"])
    flat_axes = list(axes.ravel())
    for axis, raw_panel in zip(flat_axes, panels):
        panel = require_mapping(raw_panel, "panel")
        panel_type = str(panel["type"])
        panel_palette_name = str(panel.get("palette", palette_name))
        if panel_palette_name not in PALETTES:
            raise ValueError(f"unknown panel palette: {panel_palette_name}")
        panel_palette = PALETTES[panel_palette_name]
        panel_palette_roles = require_mapping(
            PALETTE_SPECS[panel_palette_name]["roles"],
            f"palette {panel_palette_name} roles",
        )
        if panel_type == "horizontal_bar":
            draw_horizontal_bar(axis, panel, panel_palette, panel_palette_roles)
        elif panel_type == "grouped_bar":
            draw_grouped_bar(axis, panel, panel_palette, panel_palette_roles)
        elif panel_type == "line":
            draw_line(axis, panel, panel_palette, panel_palette_roles)
    for axis in flat_axes[len(panels) :]:
        axis.set_visible(False)
    return figure, font_name, size


def sha256(path: Path) -> str:
    """Hash one file in bounded chunks for the reproducibility manifest."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_pillow() -> tuple[Any, Any]:
    """Load Pillow before export so PNG verification and grayscale are guaranteed."""
    try:
        import PIL
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError(
            "Pillow is required for PNG verification; install "
            "skill/plot-handdrawn-paper-charts/requirements.txt"
        ) from exc
    return PIL, Image


def verify_artifact(
    path: Path, kind: str, *, manifest_path: str | None = None
) -> dict[str, Any]:
    """Reopen one export, validate its structure, and return portable evidence."""
    size = path.stat().st_size
    if size < 1:
        raise ValueError(f"artifact is empty: {path}")
    if kind in {"pdf", "png", "svg"} and size < 256:
        raise ValueError(f"artifact is unexpectedly small: {path}")
    prefix = path.read_bytes()[:256]
    if kind == "pdf" and not prefix.startswith(b"%PDF"):
        raise ValueError(f"invalid PDF signature: {path}")
    if kind == "png" and not prefix.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"invalid PNG signature: {path}")
    if kind == "svg":
        root = ET.parse(path).getroot()
        if root.tag.rsplit("}", 1)[-1] != "svg":
            raise ValueError(f"invalid SVG root: {path}")
    if kind == "source":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError(f"source artifact is not a JSON object: {path}")
    evidence: dict[str, Any] = {
        "path": manifest_path or path.name,
        "bytes": size,
        "sha256": sha256(path),
    }
    if kind == "png":
        _, Image = require_pillow()
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            evidence["pixels"] = [int(image.width), int(image.height)]
    return evidence


def commit_staged_exports(
    staged_paths: Sequence[Path], output_dir: Path, stale_paths: Sequence[Path]
) -> list[Path]:
    """Atomically replace a complete export set and restore prior files on error.

    Every new artifact is rendered and verified in a temporary directory first.
    Existing targets are copied into the same staging area before replacement.
    If a commit operation fails, the function removes newly introduced files and
    restores every previous target, preventing a mixed old/new delivery bundle.
    """
    backup_dir = staged_paths[0].parent / ".previous"
    backup_dir.mkdir()
    final_paths = [output_dir / path.name for path in staged_paths]
    touched_paths = [*final_paths, *stale_paths]
    backups: dict[Path, Path] = {}
    for target in touched_paths:
        if target.exists():
            backup = backup_dir / target.name
            shutil.copy2(target, backup)
            backups[target] = backup

    try:
        for staged, target in zip(staged_paths, final_paths):
            staged.replace(target)
        for stale in stale_paths:
            stale.unlink(missing_ok=True)
    except Exception:
        for target in touched_paths:
            if target.exists():
                target.unlink()
        for target, backup in backups.items():
            shutil.copy2(backup, target)
        raise
    return final_paths


def export(
    figure: plt.Figure,
    spec: Mapping[str, Any],
    source_path: Path,
    output_dir: Path,
    stem: str,
    font_name: str,
    size: tuple[float, float],
    *,
    grayscale: bool,
) -> list[Path]:
    """Stage, verify, and atomically commit a portable publication bundle.

    PDF and SVG timestamps are suppressed so repeated renders on the same
    software stack are byte-stable. The manifest stores relative artifact names
    rather than workstation paths, making a completed bundle safe to move or
    publish. No staged file reaches the output directory until all checks pass.
    """
    PIL, Image = require_pillow()
    figure_spec = require_mapping(spec.get("figure", {}), "figure")
    dpi = int(figure_spec.get("dpi", 300))
    title = str(figure_spec.get("title", stem))
    transparent = bool(figure_spec.get("transparent", False))
    output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f".{stem}.", dir=output_dir) as temp_dir:
        stage_dir = Path(temp_dir)
        source_copy = stage_dir / f"{stem}.source.json"
        pdf_path = stage_dir / f"{stem}.pdf"
        svg_path = stage_dir / f"{stem}.svg"
        png_path = stage_dir / f"{stem}.png"
        gray_path = stage_dir / f"{stem}.gray.png"
        manifest_path = stage_dir / f"{stem}.manifest.json"

        source_copy.write_text(
            json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        figure.savefig(
            pdf_path,
            bbox_inches="tight",
            pad_inches=0.04,
            transparent=transparent,
            metadata={
                "Title": title,
                "Creator": "plot-handdrawn-paper-charts",
                "CreationDate": None,
                "ModDate": None,
            },
        )
        figure.savefig(
            svg_path,
            bbox_inches="tight",
            pad_inches=0.04,
            transparent=transparent,
            metadata={
                "Title": title,
                "Creator": "plot-handdrawn-paper-charts",
                "Date": None,
            },
        )
        figure.savefig(
            png_path,
            dpi=dpi,
            bbox_inches="tight",
            pad_inches=0.04,
            transparent=transparent,
            metadata={"Title": title, "Software": "plot-handdrawn-paper-charts"},
        )

        paths = [source_copy, pdf_path, svg_path, png_path]
        if grayscale:
            with Image.open(png_path) as image:
                image.convert("L").convert("RGB").save(gray_path)
            paths.append(gray_path)

        evidence: dict[str, Any] = {
            "source": verify_artifact(source_copy, "source"),
            "pdf": verify_artifact(pdf_path, "pdf"),
            "svg": verify_artifact(svg_path, "svg"),
            "png": verify_artifact(png_path, "png"),
        }
        if grayscale:
            evidence["grayscale_png"] = verify_artifact(gray_path, "png")

        figure_palette_name = str(figure_spec.get("palette", "ocean-blue"))
        panel_palette_names = [
            str(require_mapping(panel, "panel").get("palette", figure_palette_name))
            for panel in spec["panels"]
        ]
        selected_palette_names = list(
            dict.fromkeys([figure_palette_name, *panel_palette_names])
        )
        manifest = {
            "renderer": "plot-handdrawn-paper-charts",
            "renderer_version": VERSION,
            "renderer_sha256": sha256(Path(__file__)),
            "status": "verified",
            "data_status": str(spec.get("data_status", "unspecified")),
            "input_file": source_path.name,
            "input_sha256": sha256(source_path),
            "resolved_font": font_name,
            "runtime": {
                "python": platform.python_version(),
                "matplotlib": matplotlib.__version__,
                "numpy": np.__version__,
                "pillow": PIL.__version__,
            },
            "palette_selection": {
                "figure": figure_palette_name,
                "panels": panel_palette_names,
                "profiles": {
                    name: {
                        "tone": PALETTE_SPECS[name]["tone"],
                        "best_for": PALETTE_SPECS[name]["best_for"],
                        "roles": PALETTE_SPECS[name]["roles"],
                        "aesthetic_audit": palette_aesthetic_metrics(
                            PALETTE_SPECS[name]
                        ),
                    }
                    for name in selected_palette_names
                },
            },
            "figure_size_inches": [size[0], size[1]],
            "dpi": dpi,
            "panel_count": len(spec["panels"]),
            "grayscale_included": grayscale,
            "artifact_paths": "relative_to_manifest",
            "artifacts": evidence,
        }
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        parsed_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if parsed_manifest.get("status") != "verified":
            raise ValueError("manifest verification status is missing")
        paths.append(manifest_path)
        stale = [] if grayscale else [output_dir / f"{stem}.gray.png"]
        return commit_staged_exports(paths, output_dir, stale)


def main() -> None:
    """Validate, render, verify, and print every absolute artifact path."""
    args = parse_args()
    if args.list_palettes:
        validate_palette_catalog()
        catalog = {
            name: {**palette, "aesthetic_audit": palette_aesthetic_metrics(palette)}
            for name, palette in PALETTE_SPECS.items()
        }
        print(json.dumps(catalog, ensure_ascii=False, indent=2))
        return
    if args.spec is None:
        raise ValueError("--spec is required unless --list-palettes is used")
    spec = read_spec(args.spec)
    validate_spec(spec)
    figure_spec = require_mapping(spec.get("figure", {}), "figure")
    stem = validate_stem(
        args.stem or figure_spec.get("stem", "handdrawn_chart"), "output stem"
    )
    if args.validate_only:
        print(f"VALID: {args.spec.resolve()}")
        return
    if args.output_dir is None:
        raise ValueError("--output-dir is required when rendering")

    require_pillow()
    figure, font_name, size = render_figure(spec)
    try:
        outputs = export(
            figure,
            spec,
            args.spec,
            args.output_dir,
            stem,
            font_name,
            size,
            grayscale=not args.no_grayscale,
        )
    finally:
        plt.close(figure)
    for path in outputs:
        print(path.resolve())


if __name__ == "__main__":
    main()
