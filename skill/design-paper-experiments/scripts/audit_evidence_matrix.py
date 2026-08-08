#!/usr/bin/env python3
"""Validate experiment coverage and render a compact Markdown main table."""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any


RESULT_STATUSES = {"measured", "synthetic", "partial", "planned", "missing"}
COMPLETE_STATUSES = {"measured", "synthetic"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--markdown", type=Path)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def finite(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be numeric")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    return number


def indexed(items: Any, label: str) -> dict[str, dict[str, Any]]:
    if not isinstance(items, list) or not items:
        raise TypeError(f"{label} must be a non-empty list")
    output: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise TypeError(f"{label}[{index}] must be an object")
        item_id = str(item.get("id", ""))
        if not item_id or item_id in output:
            raise ValueError(f"{label}[{index}].id must be unique")
        output[item_id] = item
    return output


def load_matrix(path: Path) -> dict[str, Any]:
    matrix = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(matrix, dict):
        raise TypeError("the experiment matrix must be an object")
    if not str(matrix.get("data_status", "")).strip():
        raise ValueError("data_status is required")
    return matrix


def audit(matrix: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    methods = indexed(matrix.get("methods"), "methods")
    benchmarks = indexed(matrix.get("benchmarks"), "benchmarks")
    metrics = indexed(matrix.get("metrics"), "metrics")
    for metric_id, metric in metrics.items():
        if str(metric.get("direction")) not in {"higher", "lower"}:
            raise ValueError(f"metrics.{metric_id}.direction must be higher or lower")

    results = matrix.get("results")
    if not isinstance(results, list):
        raise TypeError("results must be a list")
    cells: dict[tuple[str, str, str], dict[str, Any]] = {}
    for index, result in enumerate(results):
        if not isinstance(result, dict):
            raise TypeError(f"results[{index}] must be an object")
        method_id = str(result.get("method", ""))
        benchmark_id = str(result.get("benchmark", ""))
        metric_id = str(result.get("metric", ""))
        if method_id not in methods or benchmark_id not in benchmarks or metric_id not in metrics:
            raise ValueError(f"results[{index}] references an unknown id")
        key = (method_id, benchmark_id, metric_id)
        if key in cells:
            raise ValueError(f"duplicate result cell: {key}")
        status = str(result.get("status", "measured"))
        if status not in RESULT_STATUSES:
            raise ValueError(f"results[{index}].status is invalid")
        if "value" in result and result["value"] is not None:
            finite(result["value"], f"results[{index}].value")
        if "uncertainty" in result and result["uncertainty"] is not None:
            if finite(result["uncertainty"], f"results[{index}].uncertainty") < 0:
                raise ValueError(f"results[{index}].uncertainty must be non-negative")
        cells[key] = result

    requirements = matrix.get("requirements", {})
    if not isinstance(requirements, dict):
        raise TypeError("requirements must be an object")
    required_roles = [str(item) for item in requirements.get("method_roles", [])]
    present_roles = {str(item.get("role", "")) for item in methods.values()}
    missing_roles = [role for role in required_roles if role not in present_roles]

    main_methods = [key for key, item in methods.items() if item.get("include_in_main", True)]
    main_benchmarks = [key for key, item in benchmarks.items() if item.get("required", True)]
    primary_metrics = [key for key, item in metrics.items() if item.get("primary", False)]
    if not primary_metrics:
        raise ValueError("at least one metric must be primary")
    required_cells = [
        (method_id, benchmark_id, metric_id)
        for method_id in main_methods
        for benchmark_id in main_benchmarks
        for metric_id in primary_metrics
    ]
    missing_cells = []
    for key in required_cells:
        result = cells.get(key)
        if result is None or str(result.get("status", "measured")) not in COMPLETE_STATUSES or result.get("value") is None:
            missing_cells.append({"method": key[0], "benchmark": key[1], "metric": key[2]})

    families = matrix.get("evidence_families", {})
    if not isinstance(families, dict):
        raise TypeError("evidence_families must be an object")
    required_families = [str(item) for item in requirements.get("evidence_families", [])]
    missing_families = [
        family
        for family in required_families
        if family not in families or str(families[family].get("status", "")) not in COMPLETE_STATUSES
    ]

    completed = len(required_cells) - len(missing_cells)
    report = {
        "study": str(matrix.get("study", "")),
        "data_status": matrix["data_status"],
        "required_cell_count": len(required_cells),
        "completed_cell_count": completed,
        "coverage_ratio": round(completed / len(required_cells), 4) if required_cells else 1.0,
        "missing_method_roles": missing_roles,
        "missing_cells": missing_cells,
        "missing_evidence_families": missing_families,
    }
    report["status"] = "pass" if not (missing_roles or missing_cells or missing_families) else "review"
    context = {
        "methods": methods,
        "benchmarks": benchmarks,
        "metrics": metrics,
        "cells": cells,
        "main_methods": main_methods,
        "main_benchmarks": main_benchmarks,
        "primary_metrics": primary_metrics,
    }
    return report, context


def format_value(result: dict[str, Any]) -> str:
    if result.get("value") is None:
        return "—"
    digits = int(result.get("digits", 1))
    value = f"{float(result['value']):.{digits}f}"
    if result.get("uncertainty") is not None:
        value += f" ± {float(result['uncertainty']):.{digits}f}"
    return value


def render_markdown(matrix: dict[str, Any], context: dict[str, Any]) -> str:
    methods = context["methods"]
    benchmarks = context["benchmarks"]
    metrics = context["metrics"]
    cells = context["cells"]
    columns = [(benchmark, metric) for benchmark in context["main_benchmarks"] for metric in context["primary_metrics"]]

    ranks: dict[tuple[str, str], dict[str, int]] = {}
    for benchmark_id, metric_id in columns:
        values = []
        for method_id in context["main_methods"]:
            result = cells.get((method_id, benchmark_id, metric_id))
            if result and result.get("value") is not None and str(result.get("status", "measured")) in COMPLETE_STATUSES:
                values.append((method_id, float(result["value"])))
        reverse = str(metrics[metric_id]["direction"]) == "higher"
        ordered = sorted(values, key=lambda item: item[1], reverse=reverse)
        ranks[(benchmark_id, metric_id)] = {method_id: index + 1 for index, (method_id, _) in enumerate(ordered)}

    headers = ["Method"] + [
        f"{benchmarks[benchmark]['name']} · {metrics[metric]['name']} ({'↑' if metrics[metric]['direction'] == 'higher' else '↓'})"
        for benchmark, metric in columns
    ]
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for method_id in context["main_methods"]:
        row = [str(methods[method_id]["name"])]
        for benchmark_id, metric_id in columns:
            result = cells.get((method_id, benchmark_id, metric_id))
            rendered = format_value(result) if result else "—"
            rank = ranks[(benchmark_id, metric_id)].get(method_id)
            if rank == 1:
                rendered = f"**{rendered}**"
            elif rank == 2:
                rendered = f"<u>{rendered}</u>"
            row.append(rendered)
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    lines.append(f"Data status: {matrix['data_status']}.")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    matrix = load_matrix(args.matrix)
    report, context = audit(matrix)
    rendered_report = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered_report, encoding="utf-8")
        json.loads(args.report.read_text(encoding="utf-8"))
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(render_markdown(matrix, context), encoding="utf-8")
        args.markdown.read_text(encoding="utf-8")
    print(rendered_report, end="")
    return 2 if args.strict and report["status"] != "pass" else 0


if __name__ == "__main__":
    raise SystemExit(main())
