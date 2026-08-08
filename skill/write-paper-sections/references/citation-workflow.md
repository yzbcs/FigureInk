# Citation workflow

Use this reference whenever the requested section discusses prior work, datasets, metrics, borrowed components, empirical premises, or external facts.

## Core rule

Use this sequence:

```text
identify the claim -> mark the citation need -> verify the source -> obtain the bibliography entry -> insert the citation -> read back the supported sentence
```

Never invent a paper, author, year, venue, title, identifier, bibliography key, or result. Existing project bibliography files and verified source records are the source of truth.

## Citation slots

Before drafting, create one slot for each external claim:

| Slot | Claim to support | Source type | Search or supplied source | Bibliography key | Status |
|---|---|---|---|---|---|
| `[CITE_1]` | `[EXACT_CLAIM]` | field premise / method family / closest work / borrowed component / dataset / metric | `[SOURCE]` | `[BIB_KEY]` | verified / unfilled |

Do not use fixed citation counts as a quality substitute. Citation coverage is complete when every external claim has an appropriate source, the closest relevant work is represented, and irrelevant citations have been removed.

## Source verification

For every new citation:

1. verify the paper title, full author list, venue or archive, and year from a reliable record;
2. prefer the final venue version when it is the version being discussed;
3. obtain a complete bibliography entry rather than guessing a key from memory;
4. add it to the project's existing bibliography file and deduplicate equivalent records;
5. leave `[TBD_CITATION: claim]` when the source is still unresolved.

## Natural insertion

Put the scientific claim before the citation. Use the method, finding, or paradigm as the grammatical subject rather than turning the paragraph into an author list.

Prefer:

```text
[METHOD_FAMILY] improves [CAPABILITY] by [MECHANISM] [CITATIONS], but its reliance on [ASSUMPTION] leaves [LIMITATION].
```

Avoid:

```text
[AUTHOR_1] proposed [METHOD_1]. [AUTHOR_2] proposed [METHOD_2]. Many works study this problem [LONG_CITATION_LIST].
```

Group citations only when the sources support the same sentence-level claim. Do not attach a citation cluster to several unrelated assertions.

## Section placement

- **Abstract:** normally citation-free unless one external definition is essential and the venue permits it.
- **Introduction:** cite task premises, method-family summaries, observed limitations, and closest competitors.
- **Method:** cite borrowed algorithms, architectures, objectives, datasets, or formal results at first use.
- **Experiments:** cite datasets, metrics, baselines, and evaluation protocols.

## Readback

After drafting:

1. verify every citation key exists in the bibliography;
2. verify every cited source supports the adjacent claim;
3. remove citations that are famous but irrelevant to the sentence;
4. ensure no external factual claim remains uncited;
5. compile or run the project's bibliography checker when available;
6. keep unresolved slots visible as typed placeholders rather than silently deleting them.

A citation establishes an external premise or prior result. It does not turn a planned or proxy result from the current paper into measured evidence.
