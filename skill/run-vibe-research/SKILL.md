---
name: run-vibe-research
description: Orchestrate an agent-native, evidence-backed research loop across experiments, paper writing, and scientific figures. Use when a researcher asks for vibe research, end-to-end paper iteration, turning a codebase or idea into a research package, coordinating main-table enrichment with abstract/introduction/method writing, creating intro/method/experiment figures, or maintaining a round-by-round research handoff. Route focused subtasks to design-paper-experiments, write-paper-sections, design-paper-figures, and plot-handdrawn-paper-charts.
---

# Run Vibe Research

Turn the current workspace into a visible loop of question -> evidence -> claim -> prose -> figure. Keep the researcher in control at every round and prefer inspectable artifacts over one-shot paper generation.

## Operating contract

- Bind the active repository, manuscript, result files, and figure sources before proposing work.
- Treat measured artifacts as authoritative. Keep planned, synthetic, partial, and measured values visibly distinct.
- Preserve the user's research idea and source wording. Improve structure and support rather than inventing a different paper.
- Run code after editing it, preserve existing checkpoints, and record exact result paths and unfinished coverage.
- Do not let figures or prose outrun the evidence ledger. Every headline claim must resolve to a measured result, a cited source, or an explicit hypothesis.
- Keep one current artifact per role. Iterate in place rather than creating `_v2`, `_final2`, or similar copies.

## Core loop

1. **Inventory current state.** Read the repository instructions, manuscript sources, result tables, plotting code, logs, and active outputs. Classify each artifact as measured, partial, planned, illustrative, or stale.
2. **Write the research spine.** State the research question, concrete failure of prior practice, proposed mechanism, decisive comparison, and falsification condition in five short fields.
3. **Build the evidence map.** Use `references/research-state.md`. Link each planned claim to the experiment, metric, slice, and artifact that could support or contradict it.
4. **Design the next experiment round.** Invoke `design-paper-experiments`. Prioritize the smallest experiment that reduces the largest claim uncertainty, not the largest possible sweep.
5. **Execute and read back.** Run the edited code, reopen the output, and record the exact input, command, result, failure, and next decision in the round ledger.
6. **Freeze the evidence snapshot.** Once the main comparison is complete, freeze the rows, columns, metric definitions, denominators, and uncertainty convention used by writing and figures.
7. **Draft the paper story.** Invoke `write-paper-sections` in the order introduction spine -> method contract -> abstract. Draft the abstract last even when it appears first.
8. **Compose the visual story.** Invoke `design-paper-figures` for intro and method diagrams. Invoke `plot-handdrawn-paper-charts` for exact quantitative plots.
9. **Run the consistency pass.** Confirm that names, numbers, method stages, baselines, dataset splits, and caveats agree across source results, tables, prose, captions, and figures.
10. **Choose the next round.** Continue only from observed evidence. Record what changed, why, the result, the interpretation, and the next decision.

## Routing

- **Main table, baselines, metrics, ablations, robustness, efficiency:** `design-paper-experiments`
- **Abstract, introduction, method, claim-evidence alignment:** `write-paper-sections`
- **Intro figure, method overview, figure story, panel plan:** `design-paper-figures`
- **Bars, curves, exact values, uncertainty, grayscale QA:** `plot-handdrawn-paper-charts`

Use several skills in one round when the artifacts depend on each other. Do not collapse their quality gates into a generic checklist.

## Round gate

A round is complete only when all five fields exist:

1. design motivation;
2. concrete change and key parameters;
3. literal result data and artifact path;
4. interpretation or failure cause;
5. next insight derived from that result.

Use `assets/round-ledger-template.md` for the durable record.

## Completion gate

Before calling a research package ready, verify:

- the main claim has a decisive comparison and a stated falsification condition;
- the main table has complete denominators and no mixed metric semantics;
- every reported number resolves to the frozen result snapshot;
- the method figure and method section use the same component names and order;
- the introduction figure visualizes the paper's real gap, not a generic workflow;
- limitations describe unresolved evidence rather than generic caution;
- all generated code and artifact paths reopen successfully.

## Resources

- `references/research-state.md`: compact research-spine and claim-evidence schema.
- `references/github-patterns.md`: design decisions distilled from related GitHub projects.
- `assets/round-ledger-template.md`: reusable round-by-round handoff template.
