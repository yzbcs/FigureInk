# Prose quality

Use this reference during drafting, polishing, compression, and the final readback. The goal is not decorative language; every sentence should strengthen the scientific argument.

## Direct scientific voice

Prefer subjects inside the research:

- `We study ...`, `We propose ...`, and `The results show ...`;
- `This bottleneck arises because ...`;
- `[MODULE] transforms [INPUT] into [OUTPUT] ...`.

Avoid detached narration about the manuscript, its authors, or an imagined reviewer. Keep reviewer-facing reasoning in the internal plan and persuade through mechanism and evidence.

## Cohesion

Each paragraph needs one retained message. A sentence should state, explain, support, contrast, or transition. Remove a sentence that performs none of these jobs.

Maintain continuity through subject inheritance:

```text
method family -> its mechanism -> the mechanism's assumption -> failure under that assumption -> required capability -> matching design
```

Transitions must name real relations. `However` introduces a conflict, `therefore` a consequence, `building on` a dependency, and `moreover` a genuinely complementary step.

## Terminology discipline

- Define one canonical name for each task, module, representation, dataset, metric, assumption, and claim.
- Do not alternate synonyms merely to avoid repetition.
- Expand acronyms at first use and preserve capitalization thereafter.
- Match names across Abstract, Introduction, Method, equations, captions, tables, and code-facing artifacts.

## Sentence rhythm

Mix short signpost sentences with longer explanatory sentences. Do not let every sentence use the same cue, length, or grammatical shape. Split a sentence when it carries multiple unrelated claims, mechanisms, and evidence items.

## High-risk patterns

Remove or rewrite:

- label-heavy prose such as repeated `Key:`, `Challenge:`, `C1`, or `Q1` scaffolding;
- formula-first paragraphs that introduce notation before scientific purpose;
- number-led abstracts that substitute gains for task, gap, insight, and scope;
- citation dumps without a shared claim;
- repeated generic openings such as `Recently` or `In recent years`;
- repeated motivation in every section;
- empty intensifiers such as `novel`, `significant`, `powerful`, or `clearly` without evidence;
- punctuation chains, arrows, brackets, or slash stacks used instead of sentence logic;
- visible process narration such as audit status, internal confidence, or what a reviewer is expected to think;
- defensive phrasing that weakens the contribution instead of stating its scientific boundary.

## Section checks

### Abstract

- A reader can recover task, gap, method insight, progressive contributions, evidence, and scope in one pass.
- Decisive numbers support the story rather than dominate it.
- No sentence contains several unrelated modules.

### Introduction

- Prior work is organized by mechanism and solved capability, not as an author catalogue.
- The root reason appears before the proposed design.
- Limitations, required capabilities, modules, and evidence use the same order.
- Figure 1 is interpreted as part of the argument rather than cited ceremonially.

### Method

- Explain why a component exists before its computation.
- Introduce what an equation represents before displaying it and explain how its output is used afterward.
- Keep empirical gains in Experiments.

## Final readback

Check for a paragraph without one retained message, a sentence that repeats rather than advances, inconsistent names, unsupported modifiers, vague referents, template repetition, or a conclusion stronger than the evidence. Revise the prose itself rather than appending a generic warning.
