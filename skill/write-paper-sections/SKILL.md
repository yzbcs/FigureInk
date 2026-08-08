---
name: write-paper-sections
description: Draft, revise, polish, compress, and audit evidence-grounded research paper abstracts, introductions, and method sections. Use for paper story construction, contribution framing, paragraph flow, citation integration, sentence-level academic revision, source-preserving rewrites, claim-evidence alignment, or before-after writing comparison. Preserve the author's idea, source format, terminology, citations, and measured scope; use the bundled claim-ledger audit before strengthening claims.
---

# Write Paper Sections

Write the requested paper text, not a process report. Keep planning controls internal unless the user asks for an outline, diagnosis, or rationale.

## Operating contract

- Read the existing section, nearby manuscript context, figures, tables, captions, bibliography, and result artifacts before drafting.
- Preserve the research question, contribution boundaries, source format, terminology, citations, labels, equations, and measured evidence.
- Do not invent numbers, baselines, citations, dataset properties, implementation details, or evaluation outcomes. Use a typed `TBD` slot when required input is missing.
- Distinguish prior-work evidence, hypotheses, planned evidence, and measured findings.
- Return the requested artifact first. Keep status notes brief and outside manuscript prose.
- Prefer direct scientific voice, concrete mechanisms, stable terms, and evidence-bounded claims.

## Select mode and output

- **draft:** create the requested section from the supplied brief and evidence.
- **revise:** improve structure or argument while preserving authorized claims and source format.
- **polish:** improve local clarity, cohesion, terminology, and rhythm without restructuring the scientific story.
- **compress:** meet a word or page budget without dropping necessary logic, citations, or claim scope.
- **diagnose:** expose paragraph roles, story breaks, unsupported claims, or citation gaps only when requested.

For source-preserving revision, keep LaTeX commands and document structure intact. If the user asks to retain the original, place it in comments or a paired before block and revise sentence by sentence. Read `references/writing-workflow.md` for the detailed output contract.

## Workflow

1. **Freeze the writing brief.** Record mode, output format, section role, target length, immutable content, paper spine, evidence, terminology, and citation slots. Copy `assets/section-brief-template.md` when useful.
2. **Build the paper spine.** Connect `task -> gap -> root reason -> insight -> mechanism -> evidence -> bounded claim`. Unknown links remain typed slots rather than invented transitions.
3. **Prepare citations.** Mark the exact claim each citation must support. Verify source metadata and bibliography keys before inserting citations. Read `references/citation-workflow.md`.
4. **Choose the section contract.** Load only the matching abstract, introduction, or method reference.
5. **Assign paragraph roles internally.** Give each paragraph one retained message and an explicit handoff to the next paragraph.
6. **Draft the artifact first.** Make each sentence state, explain, support, contrast, or transition; remove sentences with no scientific job.
7. **Audit the claim ledger.** Run `scripts/audit_claim_ledger.py`. Resolve unsupported, weak, contradictory, or numerically unanchored claims.
8. **Revise in three passes.** First repair story logic, then evidence and citation scope, then prose quality. Apply `references/prose-quality.md` during the final pass.
9. **Read back in paper order.** Confirm that Abstract, Introduction, Method, figures, tables, and experiments use the same terms and promise only what the evidence delivers.

## Section contracts

### Abstract

Use four parts: **background convention (1 sentence) -> motivation (1–2 sentences) -> formal method introduction (4–5 sentences) -> performance close (1–2 sentences)**. Make the `Specifically -> To further -> Moreover` contributions progressive and map each to a stated gap. Read `references/abstract-writing.md`, then copy `assets/abstract-template.md` when a fillable draft is useful.

### Introduction

Use four or five paragraphs: **topic and Figure 1 -> classified prior work -> additional category and synthesis -> optional standalone limitations -> mapped method response, evidence preview, and three contributions**. Keep a one-to-one `limitation -> required capability -> module -> evidence` map and preserve subject continuity between sentences. Read `references/introduction-writing.md`, then copy `assets/introduction-template.md` when drafting.

### Method

Use: **problem setup -> overview -> components in execution order -> training/inference or optimization -> complexity and reproducibility details**. Explain why each component exists before describing its implementation. Read `references/method-writing.md`.

## Commands

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/write-paper-sections"

python3 "$SKILL_DIR/scripts/audit_claim_ledger.py" \
  --packet /absolute/path/to/section-packet.json \
  --report /absolute/path/to/claim-audit.json
```

Use `--strict` when every headline claim must be supported by measured evidence before delivery.

## Quality gates

- The visible output begins with the requested section or revised source, not an internal checklist.
- Every paragraph has one retained message; every sentence advances that message or the next transition.
- The section follows one paper spine rather than a list of unrelated modules, facts, or numbers.
- Every headline claim resolves to measured evidence, a verified external source, or an explicit hypothesis.
- Citation keys come from verified bibliography entries and support the exact adjacent claim.
- Numbers, metric names, directions, denominators, and comparison scopes agree with the frozen result snapshot.
- The introduction's gaps map to method mechanisms and decisive evidence in the same order.
- Method prose explains scientific roles before equations or implementation detail and does not leak result claims.
- Terminology remains stable across sections, figures, tables, equations, and code-facing names.
- The prose contains no process narration, unsupported hype, repetitive templates, or punctuation standing in for logic.

## Resources

- `scripts/audit_claim_ledger.py`: validate claim-evidence status and numeric anchors.
- `assets/example_section_packet.json`: complete synthetic audit fixture.
- `assets/section-brief-template.md`: freeze mode, format, story, evidence, citations, and paragraph roles.
- `assets/abstract-template.md`: copyable four-part abstract with evidence slots.
- `assets/introduction-template.md`: copyable four/five-paragraph introduction with gap mapping.
- `references/writing-workflow.md`: modes, paper spine, paragraph planning, revision passes, and output contract.
- `references/prose-quality.md`: cohesion, direct voice, terminology, rhythm, and anti-template checks.
- `references/citation-workflow.md`: citation-slot preparation, source verification, insertion, and readback.
- `references/abstract-writing.md`: abstract moves and compression checks.
- `references/introduction-writing.md`: paragraph logic and contribution design.
- `references/method-writing.md`: execution-aligned method exposition.
- `references/evidence-grounding.md`: claim status and evidence vocabulary.
