# Writing workflow

Use this reference to decide how to transform the user's material before loading a section-specific template.

## Mode contract

| Mode | What may change | What stays fixed | Visible output |
|---|---|---|---|
| Draft | wording, paragraph plan, section structure | supplied idea, evidence, terminology, constraints | the requested section |
| Revise | argument order and paragraph logic within the authorized scope | claims, numbers, citations, labels, source format unless restructuring was requested | revised source, then concise change notes if useful |
| Polish | wording, cohesion, syntax, rhythm | paragraph purpose, scientific meaning, claim strength, format | polished text first |
| Compress | redundancy, local phrasing, low-value detail | causal chain, decisive evidence, citations, equations, scope | compressed text and a cut note only for material deletions |
| Diagnose | no manuscript changes unless requested | source file | paragraph roles, breaks, and exact repair actions |

User-requested output form has priority. Preserve LaTeX commands, comments, labels, citation keys, equations, environments, headings, lists, tables, and Markdown structure when editing an existing artifact.

## Freeze the brief

Record only facts that influence the writing:

- requested mode and output format;
- section role and target length;
- immutable claims, terminology, citations, equations, and numbers;
- task, gap, root reason, insight, method mechanism, evidence, and boundary;
- paragraph roles and contribution order;
- unresolved evidence or citation slots.

Use `TBD_RESULT`, `TBD_CITATION`, `TBD_SCOPE`, or another typed slot for unknown information. Do not hide an unknown behind fluent but unsupported prose.

## Build one paper spine

Use this causal sequence:

```text
task and significance
-> observable gap
-> root technical reason
-> core insight
-> method mechanism
-> evidence ladder
-> bounded claim
```

The spine is not necessarily the visible section order. It is an internal consistency check. A strong section lets the reader recover the chain without seeing labels.

Reject or repair a spine when:

- the method appears before the gap is understandable;
- the gap is only that prior work has not tried a technique;
- the insight is merely a module name;
- several unrelated claims compete as the paper's main point;
- experiments validate the full system but not the contribution being emphasized;
- the final claim extends beyond the tested setting.

## Plan paragraphs backward, write them forward

Before drafting, work backward from the evidence:

1. What claim can the supplied evidence support?
2. Which method mechanism produces the tested behavior?
3. Which insight motivates that mechanism?
4. Which root reason makes the insight necessary?
5. Which concrete gap exposes that root reason?

Then write forward from task to evidence. This prevents the introduction from promising a story that the experiments do not support.

Give each paragraph one retained message. Each sentence must perform at least one job:

1. state or narrow the message;
2. explain a reason or mechanism;
3. provide evidence, a citation, or an example;
4. contrast a relevant alternative;
5. hand off to the next required idea.

## Three-pass revision

### Pass 1 — Story logic

- Verify the task-to-claim spine.
- Remove duplicated motivation and detached modules.
- Make paragraph endings create the need answered next.
- Match limitation order to contribution order.

### Pass 2 — Evidence and citations

- Resolve every major claim to measured, theoretical, qualitative, or external support.
- Verify all numbers and comparison scopes.
- Ensure citations support the adjacent claim and bibliography keys exist.
- Narrow or mark claims whose evidence is incomplete.

### Pass 3 — Prose quality

- Apply `prose-quality.md`.
- Stabilize terminology and grammatical subjects.
- Split compound sentences carrying unrelated claims.
- Vary sentence rhythm without replacing technical terms with decorative synonyms.
- Remove visible checklist language and internal process narration.

## Cross-section readback

After revision, compare the section against the rest of the paper:

| Check | Required match |
|---|---|
| Abstract ↔ Introduction | same gap, insight, contribution order, and result scope |
| Introduction ↔ Method | every promised capability has a visible mechanism |
| Method ↔ Figure | same component names, order, inputs, and outputs |
| Introduction ↔ Experiments | each contribution has decisive evidence |
| Text ↔ Tables | metric, direction, comparator, denominator, and displayed value agree |
| Conclusion ↔ Evidence | no new or broader claim appears at the end |

Keep this table internal unless the user asks for an audit report.

## Delivery rule

Return useful paper text first. Add a short note only when meaning changed, a citation remains unresolved, evidence is missing, or the user asked for rationale. Never make the reader excavate the revised section from a long process summary.
