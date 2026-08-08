#!/usr/bin/env python3
"""Validate the portable skill-suite structure without external YAML packages."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skill"
EXPECTED = {
    "design-paper-experiments",
    "design-paper-figures",
    "plot-handdrawn-paper-charts",
    "run-vibe-research",
    "write-paper-sections",
}
WRITER_REQUIRED = {
    "assets/section-brief-template.md",
    "references/writing-workflow.md",
    "references/prose-quality.md",
    "references/citation-workflow.md",
}
WRITING_BRIEF_FIELDS = {
    "mode",
    "source_format",
    "section_role",
    "target_length",
    "paper_spine",
    "paragraph_roles",
    "citation_slots",
    "delivery_state",
}


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"missing YAML frontmatter: {path}")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line in {path}: {line}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def main() -> int:
    skill_dirs = {path.name: path for path in SKILL_ROOT.iterdir() if path.is_dir()}
    missing = EXPECTED - set(skill_dirs)
    if missing:
        raise ValueError(f"required skill folders are missing: {sorted(missing)}")
    for name, path in sorted(skill_dirs.items()):
        fields = parse_frontmatter(path / "SKILL.md")
        if set(fields) != {"name", "description"}:
            raise ValueError(f"{name} frontmatter must contain only name and description")
        if fields["name"] != name:
            raise ValueError(f"{name} frontmatter name does not match its folder")
        if len(fields["description"]) < 80:
            raise ValueError(f"{name} description is too short for reliable triggering")
        agent = path / "agents" / "openai.yaml"
        if not agent.is_file() or f"${name}" not in agent.read_text(encoding="utf-8"):
            raise ValueError(f"{name} agents/openai.yaml is missing a matching default prompt")
        print(f"valid skill: {name}")

    writer = skill_dirs["write-paper-sections"]
    missing_writer_files = sorted(rel for rel in WRITER_REQUIRED if not (writer / rel).is_file())
    if missing_writer_files:
        raise ValueError(f"write-paper-sections resources are missing: {missing_writer_files}")
    packet = json.loads((writer / "assets/example_section_packet.json").read_text(encoding="utf-8"))
    brief = packet.get("writing_brief")
    if not isinstance(brief, dict) or set(brief) != WRITING_BRIEF_FIELDS:
        raise ValueError("example section packet has an incomplete writing_brief")
    if not isinstance(brief["citation_slots"], list) or not isinstance(brief["paragraph_roles"], list):
        raise ValueError("writing_brief citation_slots and paragraph_roles must be lists")
    print("valid writing workflow resources and example brief")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
