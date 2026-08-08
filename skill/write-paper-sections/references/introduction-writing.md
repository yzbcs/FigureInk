# Introduction writing

Use either a four-paragraph compact structure or a five-paragraph structure with a standalone limitation paragraph. Both must maintain the same chain:

```text
task -> prior-method taxonomy -> unresolved requirements -> mapped method design -> evidence and contributions
```

## Build the gap-to-contribution map first

Complete this table before drafting prose. Each row must read as one causal argument.

| Prior family and solved problem | Observable limitation | Required capability | Matching contribution or module | Decisive evidence |
|---|---|---|---|---|
| `[FAMILY_1]` solves `[PROBLEM_1]` | `[LIMITATION_1]` | `[CAPABILITY_1]` | `[MODULE_1]` | `[EVIDENCE_1]` |
| `[FAMILY_2]` solves `[PROBLEM_2]` | `[LIMITATION_2]` | `[CAPABILITY_2]` | `[MODULE_2]` | `[EVIDENCE_2]` |
| `[FAMILY_3]` solves `[PROBLEM_3]` | `[LIMITATION_3]` | `[CAPABILITY_3]` | `[MODULE_3]` | `[EVIDENCE_3]` |

A limitation is useful only if it establishes a necessary capability. Avoid unsupported exclusivity claims such as `only our method can solve this`; show instead why the task requires the capability and how the matching design supplies it.

## Five-paragraph default

### Paragraph 1 — Topic, significance, and Figure 1

Define the topic before naming the method. Move from definition to consequence to a concrete failure or unresolved setting.

```text
[TOPIC] represents/captures [RELATIONS_OR_PROCESS] among [ENTITIES], enabling [FUNCTION] in [SETTING] [CITATION_GROUP].
This [RELATION_OR_PROCESS] matters because [CONSEQUENCE].
However, [OBSERVABLE_FAILURE] remains common when [CONDITION].
As illustrated in Figure 1, [CONCRETE_EXAMPLE_OR_DIAGNOSTIC] exposes the need for [HIGH_LEVEL_CAPABILITY].
```

Figure 1 should show the task, failure, diagnostic, or contrast used by the prose. Do not write `Figure 1 shows our framework` before the reader knows the problem.

### Paragraph 2 — First prior-work categories

Classify approaches by mechanism, not by an author-by-author list. State what each category solves before discussing its boundary.

```text
Various approaches have been proposed to [GOAL] [CITATION_GROUP].
[FAMILY_1] methods [MECHANISM_1], which improves [SOLVED_PROBLEM_1].
This mechanism is effective when [CONDITION_1], but its reliance on [ASSUMPTION_1] leaves [LIMITATION_1].
[FAMILY_2] methods instead [MECHANISM_2], allowing them to [SOLVED_PROBLEM_2].
Although this design relaxes [EARLIER_CONSTRAINT], it still requires [MISSING_CAPABILITY_2].
```

The subject chain is `approaches -> family -> mechanism -> this mechanism -> limitation`, not `dataset -> model -> metric -> therefore gap`.

### Paragraph 3 — Additional category and synthesis

Use `Moreover` or `In addition` only when the new family follows from the unresolved requirement at the end of Paragraph 2.

```text
Moreover, [FAMILY_3] methods attempt to provide [MISSING_CAPABILITY_FROM_P2] by [MECHANISM_3] [CITATION_GROUP].
This strategy addresses [SOLVED_PROBLEM_3], yet [CONDITION_OR_ASSUMPTION] prevents it from [LIMITATION_3].
Taken together, these method families provide [SHARED_PROGRESS] but do not jointly support [SYNTHESIZED_REQUIREMENTS].
```

The three families may correspond to the three contributions in the abstract. If the paper is driven by a measured bottleneck rather than a mature taxonomy, use Paragraphs 2–3 for `observed failure -> mechanism diagnosis -> missing learning signal` instead.

### Paragraph 4 — Standalone limitation paragraph

Use this paragraph when space permits or when the one-to-one mapping is central to the paper. Itemize requirements in prose, then synthesize them.

```text
Despite this progress, three issues remain. First, [LIMITATION_1], so an effective solution must [CAPABILITY_1]. Second, [LIMITATION_2], which requires [CAPABILITY_2] rather than [INSUFFICIENT_SHORTCUT]. Finally, [LIMITATION_3] makes [FAILURE] unavoidable unless the method can [CAPABILITY_3]. These requirements call for a unified design in which [CAPABILITY_2_OR_3] extends or complements [CAPABILITY_1].
```

Each item must have a visible counterpart in the next paragraph. Merge this material into the ends of Paragraphs 2–3 for the compact four-paragraph version.

### Paragraph 5 — Method response, evidence preview, and contributions

Answer the limitations in the same order. Describe the idea and role of each module, not implementation details.

```text
To address these limitations, we propose [METHOD], which [CORE_IDEA].
First, [MODULE_1] [HIGH_LEVEL_ACTION], providing [CAPABILITY_1] for [LIMITATION_1].
Building on this representation/signal, [MODULE_2] [HIGH_LEVEL_ACTION], thereby supplying [CAPABILITY_2] under [CONDITION_2].
Finally, [MODULE_3] complements the preceding modules by [HIGH_LEVEL_ACTION], which resolves [LIMITATION_3].
Experiments on [SCOPE] evaluate [EFFECTIVENESS], [CAUSAL_COMPONENT], and [BOUNDARY_OR_GENERALIZATION].
Our contributions can be summarized as follows:
(1) [CONTRIBUTION_1_WITH_ARTIFACT_AND_SCOPE];
(2) [CONTRIBUTION_2_WITH_ARTIFACT_AND_SCOPE]; and
(3) [CONTRIBUTION_3_WITH_EVIDENCE_OR_BOUNDARY].
```

The module order must match the limitation order. If Module 2 exists to supplement Module 1 rather than solve a separate gap, say so explicitly with `Building on ...`, `To further ...`, or `Because this step still ...`.

## Compact four-paragraph version

Use this structure when the venue is tight:

1. **P1:** define topic, establish significance, and use Figure 1 to expose the concrete problem;
2. **P2:** classify the first prior families, explain what they solve, and end with their limitations;
3. **P3:** introduce the final family, synthesize the numbered missing capabilities, and make the gap-to-contribution mapping explicit;
4. **P4:** begin `To address these limitations, we propose ...`, answer gaps in order, preview evidence, and list three contributions.

Do not delete the limitation logic when compressing; move it to the final sentences of P2 and P3.

## Sentence-continuity test

Apply all four checks paragraph by paragraph:

1. **Subject inheritance:** the next sentence reuses the prior subject or promotes its object to the new subject.
2. **Reasoned transition:** `however`, `therefore`, `building on`, and `moreover` name an actual logical relation.
3. **No delayed synthesis:** do not enumerate unrelated models, datasets, and phenomena and then claim they jointly imply the gap.
4. **Question handoff:** each paragraph ends with the question or missing capability that the next paragraph answers.

A useful chain is:

```text
[FAMILY] -> its mechanism -> the mechanism's assumption -> failure under that assumption -> required capability -> matching module
```

## Citation and contribution checks

- Cite topic definitions, method-family summaries, empirical premises, and borrowed mechanisms.
- Put one claim before each citation group; avoid citation-only sentences and author-name catalogues.
- Keep the novel method preview citation-light except where a component is borrowed.
- Make contribution bullets parallel, non-overlapping, and verifiable.
- Replace `a novel framework` and `extensive experiments` with the artifact, mechanism, evaluated scope, or finding.
- Ensure the introduction promises only claims that the method and experiments later deliver.
