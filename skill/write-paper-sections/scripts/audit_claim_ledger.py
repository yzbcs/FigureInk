#!/usr/bin/env python3
"""Audit a paper-section claim ledger against declared evidence artifacts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


STATUSES = {"hypothesis", "planned", "partial", "measured", "contradicted"}
STRENGTHS = {"direct", "proxy", "qualitative", "external", "none"}
NUMBER_PATTERN = re.compile(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?%?")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def load_packet(path: Path) -> dict[str, Any]:
    packet = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(packet, dict):
        raise TypeError("the section packet must be an object")
    if str(packet.get("section_type", "")) not in {"abstract", "introduction", "method"}:
        raise ValueError("section_type must be abstract, introduction, or method")
    if not str(packet.get("text", "")).strip():
        raise ValueError("text is required")
    return packet


def audit(packet: dict[str, Any]) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    evidence_items = packet.get("evidence", [])
    claims = packet.get("claims", [])
    if not isinstance(evidence_items, list) or not isinstance(claims, list):
        raise TypeError("evidence and claims must be lists")

    evidence: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(evidence_items):
        if not isinstance(item, dict):
            raise TypeError(f"evidence[{index}] must be an object")
        evidence_id = str(item.get("id", ""))
        if not evidence_id or evidence_id in evidence:
            raise ValueError(f"evidence[{index}].id must be unique")
        status = str(item.get("status", ""))
        strength = str(item.get("strength", ""))
        if status not in STATUSES:
            raise ValueError(f"evidence[{index}].status is invalid")
        if strength not in STRENGTHS:
            raise ValueError(f"evidence[{index}].strength is invalid")
        evidence[evidence_id] = item

    claim_ids: set[str] = set()
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            raise TypeError(f"claims[{index}] must be an object")
        claim_id = str(claim.get("id", ""))
        if not claim_id or claim_id in claim_ids:
            raise ValueError(f"claims[{index}].id must be unique")
        claim_ids.add(claim_id)
        text = str(claim.get("text", "")).strip()
        if not text:
            raise ValueError(f"claims[{index}].text is required")
        evidence_ids = claim.get("evidence_ids", [])
        if not isinstance(evidence_ids, list):
            raise TypeError(f"claims[{index}].evidence_ids must be a list")
        unknown = [item for item in evidence_ids if str(item) not in evidence]
        if unknown:
            issues.append({"claim": claim_id, "type": "unknown_evidence", "detail": ", ".join(map(str, unknown))})
        resolved = [evidence[str(item)] for item in evidence_ids if str(item) in evidence]
        if not resolved:
            issues.append({"claim": claim_id, "type": "unsupported", "detail": "no evidence is linked"})
        if bool(claim.get("headline", False)):
            direct_measured = any(
                str(item.get("status")) == "measured" and str(item.get("strength")) == "direct"
                for item in resolved
            )
            if not direct_measured:
                issues.append({
                    "claim": claim_id,
                    "type": "headline_not_measured",
                    "detail": "headline claim lacks direct measured evidence",
                })
        declared_numbers = {str(value) for value in claim.get("numeric_anchors", [])}
        text_numbers = set(NUMBER_PATTERN.findall(text))
        undeclared = sorted(text_numbers - declared_numbers)
        if undeclared:
            issues.append({
                "claim": claim_id,
                "type": "undeclared_number",
                "detail": ", ".join(undeclared),
            })

    terminology = packet.get("terminology", [])
    if not isinstance(terminology, list):
        raise TypeError("terminology must be a list")
    missing_terms = [str(term) for term in terminology if str(term) not in str(packet["text"])]
    for term in missing_terms:
        issues.append({"claim": "section", "type": "missing_term", "detail": term})

    return {
        "section_type": packet["section_type"],
        "claim_count": len(claims),
        "evidence_count": len(evidence),
        "issue_count": len(issues),
        "issues": issues,
        "status": "pass" if not issues else "review",
    }


def main() -> int:
    args = parse_args()
    report = audit(load_packet(args.packet))
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
        json.loads(args.report.read_text(encoding="utf-8"))
    print(rendered, end="")
    return 2 if args.strict and report["issue_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
