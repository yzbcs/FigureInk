# Abstract writing

Use a four-part abstract: **background convention -> motivation -> formal method introduction -> performance close**. The usual length is 7–10 sentences, but logical completeness outranks a mechanical sentence count.

## Freeze the inputs first

Record these slots before drafting:

- `[TASK]`, `[FUNCTION_OR_SIGNIFICANCE]`, and `[TARGET_SETTING]`;
- the nearest `[METHOD_FAMILY]` and what it already solves;
- one to three observable gaps, each phrased as a missing capability;
- `[METHOD]` and three progressive contributions;
- `[DATASETS_OR_SCOPE]`, `[COMPARATOR]`, `[METRIC]`, `[RESULT]`, and `[BOUNDARY]`.

Do not fill an empirical slot from expectation, a planned run, or a different protocol.

## Part 1 — Background convention (1 sentence)

Define the task and immediately attach its significance. Choose one stem and replace every slot:

```text
[TASK] is a crucial task that [FUNCTION_OR_SIGNIFICANCE].
```

```text
[MODEL_OR_METHOD_FAMILY] demonstrates strong capabilities in [CAPABILITIES], making it a promising foundation for [TARGET_SETTING].
```

Prefer the first stem for task-centered papers and the second for capability-transfer papers. Do not spend a second sentence on generic field growth unless it is needed to understand the gap.

## Part 2 — Motivation (1–2 sentences)

First state what current approaches do; then identify what remains underexplored or operationally unresolved.

```text
Existing methods mainly [CATEGORY_A_ACTION] or [CATEGORY_B_ACTION], enabling [SOLVED_CAPABILITY].
```

```text
However, they still [OBSERVABLE_FAILURE], because [ROOT_CAUSE_OR_MISSING_CAPABILITY]; few studies have examined [UNDEREXPLORED_QUESTION].
```

`Few studies have ...` is useful only when the literature packet supports it. Otherwise use a direct, verifiable gap such as `These methods do not explicitly model ...` or `Their gains diminish when ...`.

## Part 3 — Formal method introduction (4–5 sentences)

The method must be a consequence of Part 2. Use the following default four-sentence sequence:

```text
In this paper, we propose [METHOD], which [CORE_IDEA] to address [GAP_SUMMARY].
Specifically, we [CONTRIBUTION_1], thereby providing [CAPABILITY_1].
To further [UNRESOLVED_NEED_AFTER_1], we [CONTRIBUTION_2], which [RELATION_TO_CONTRIBUTION_1].
Moreover, we [CONTRIBUTION_3] to [COMPLEMENT_OR_OPERATIONALIZE_THE_PREVIOUS_STEPS].
```

The three contributions must be progressive rather than adjacent features:

| Order | Narrative role | Required backward link |
|---|---|---|
| Contribution 1 | establish the base representation, signal, or mechanism | solves the first and most fundamental gap |
| Contribution 2 | extend the base mechanism to the next unresolved condition | begins with what Contribution 1 still lacks |
| Contribution 3 | complement, control, scale, or operationalize the first two | explains why the complete method is necessary |

If the paper has only two genuine method contributions, do not invent a third module. Use the fourth sentence for the training objective, inference policy, or verified design consequence that completes the same chain.

## Part 4 — Performance close (1–2 sentences)

State the evaluated scope before the result and keep the conclusion within that scope:

```text
Extensive experimental results on [DATASETS_OR_SCOPE] demonstrate that [METHOD] [MEASURED_RESULT] compared with [COMPARATOR] under [PROTOCOL].
```

```text
Further [ABLATION_OR_ANALYSIS] shows that [MECHANISM_FINDING], while [BOUNDARY_OR_EXCEPTION].
```

Use one decisive number only when its denominator, metric direction, comparator, and evaluation protocol are fixed. `Extensive experimental results` is a closing convention, not a substitute for naming the tested scope.

## Default eight-sentence template

1. Task or capability significance.
2. Existing method categories and what they solve.
3. Concrete gap plus underexplored question.
4. `In this paper, we propose ...`
5. `Specifically, we ...`
6. `To further ..., we ...`
7. `Moreover, we ...`
8. Evaluated scope, decisive result, and bounded conclusion.

## Choose one story variant

- **Method-family taxonomy:** categories expose complementary missing capabilities, which become three mapped modules.
- **Representation shift:** the central limitation lies in the supervision or representation unit; lead from the old unit to the new one, then add construction and learning mechanisms.
- **Domain-transfer mismatch:** a promising general method transfers poorly; diagnose a small number of mismatches and map data, training, or inference interventions to them.
- **Diagnostic bottleneck:** a measured residual failure is stronger than a generic literature gap; explain the learning-signal mechanism, derive the data insight, then introduce the staged design.

Do not combine all four variants in one abstract.

## Continuity audit

For every sentence after the first, underline the phrase inherited from the previous sentence. A valid chain usually follows:

```text
[TASK] -> existing solutions to [TASK] -> unresolved capability -> [METHOD] -> first capability -> remaining need -> complementary mechanism -> evidence for the complete chain
```

Revise if a sentence introduces an unrelated module, if `Moreover` could be replaced by a bullet without losing logic, or if the result sentence tests a different claim from the motivation.

## Final checks

- Keep the abstract citation-free unless the venue or task explicitly requires citations.
- Expand an acronym at first use and use one stable method name thereafter.
- Remove generic adjectives such as `novel`, `comprehensive`, and `significant` when mechanism or numbers can carry the claim.
- Ensure every gap maps to a method contribution and every headline contribution maps to evidence.
- Compress repeated module descriptions; the abstract should expose roles, not implementation details.
