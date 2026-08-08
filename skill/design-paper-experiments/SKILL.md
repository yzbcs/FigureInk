---
name: design-paper-experiments
description: Design, enrich, and audit research experiment packages and main result tables. Use when a user asks how to make a main table richer, add meaningful baselines or metrics, plan ablations, robustness, efficiency, scaling, error analysis, human evaluation, statistical reporting, evidence matrices, reviewer-question coverage, or before-after experiment comparisons. Expand evidence only where it tests a claim; preserve measured values and use the bundled matrix auditor to expose missing cells and unsupported table structure.
---

# Design Paper Experiments

Turn a sparse result table into a compact evidence argument. Richness means reviewer-question coverage, not maximum width.

## Operating contract

- Start from the paper's main claim and falsification condition, not from available table space.
- Preserve every measured value, denominator, split, seed, and metric definition.
- Keep measured, partial, planned, proxy, synthetic, and theoretical values visibly separate.
- Never relabel one rollout, one seed, or one subset as a stronger aggregate metric.
- Add a row or column only when it answers a named reviewer question.
- Execute planned experiments before reporting them as results.

## Main-table workflow

1. **State the decisive claim.** Write the exact comparison that would support or contradict it.
2. **Map reviewer questions.** Cover effectiveness, fairness of comparison, generality, reliability, cost, and mechanism only when relevant.
3. **Choose method rows.** Include a lower bound, a strong comparable baseline, the closest method family, the proposed system, and an upper bound only when it is well-defined.
4. **Choose evidence columns.** Use primary quality metrics first; add task or dataset slices that test generality; add cost or latency when the method claims efficiency.
5. **Separate evidence families.** Keep the main table focused. Put ablations, scaling, robustness, and error analysis in supporting tables or figures unless they are decisive.
6. **Specify repetition.** Record seeds or rollouts, aggregation, uncertainty, significance test, and missing-value policy before running.
7. **Build the evidence matrix.** Copy `assets/example_experiment_matrix.json` and replace synthetic values with measured artifacts.
8. **Audit coverage.** Run `scripts/audit_evidence_matrix.py`; resolve missing required roles, incomplete primary cells, duplicate results, and absent evidence families.
9. **Run and read back.** Execute missing cells, reopen outputs, and update the same matrix.
10. **Freeze the table contract.** Lock row order, column order, metric direction, denominators, and best/second-best marking before writing prose.

## Evidence ladder

Use the smallest set that tests the paper's claims:

1. **Effectiveness:** main comparison on primary metrics.
2. **Generality:** multiple tasks, domains, model sizes, or distributions.
3. **Mechanism:** ablations and controlled substitutions.
4. **Reliability:** seeds, rollouts, uncertainty, significance, sensitivity.
5. **Robustness:** noise, shift, missing inputs, adversarial or stress conditions.
6. **Efficiency:** latency, memory, tokens, FLOPs, cost, data, or wall time.
7. **Understanding:** error taxonomy, qualitative cases, subgroup or failure analysis.
8. **Replication:** independent rerun or held-out implementation when the claim needs it.

Read `references/experiment-ladder.md` to select only relevant levels.

## Commands

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/design-paper-experiments"

python3 "$SKILL_DIR/scripts/audit_evidence_matrix.py" \
  --matrix /absolute/path/to/experiment-matrix.json \
  --report /absolute/path/to/evidence-audit.json \
  --markdown /absolute/path/to/main-table.md
```

Use `--strict` after all required cells have been executed.

## Quality gates

- Every required method has every primary metric on every required benchmark or an explicit missing-value reason.
- Baselines are comparable in data, backbone, tool access, budget, and evaluation protocol, or the mismatch is disclosed.
- Metric names include direction, unit, aggregation, and denominator.
- Best and second-best formatting is recomputed after every changed value.
- Uncertainty describes the actual sampling unit: seed, rollout, subject, task, or example.
- Ablations remove or replace one mechanism at a time.
- Robustness conditions are tied to a plausible failure mode.
- Main-text claims do not generalize beyond tested tasks, datasets, models, or budgets.

## Resources

- `scripts/audit_evidence_matrix.py`: validate table schema, coverage, and evidence-family presence.
- `assets/example_experiment_matrix.json`: complete synthetic evidence matrix.
- `references/main-table-design.md`: row/column selection and marking rules.
- `references/experiment-ladder.md`: evidence-family selection guide.
- `references/statistical-reporting.md`: repetition, uncertainty, and denominator guidance.
