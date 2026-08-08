# Research state

Keep one compact state file in the active experiment folder.

## Research spine

| Field | Content |
|---|---|
| Question | What exact uncertainty is the paper resolving? |
| Observed failure | What behavior or result makes the problem concrete? |
| Mechanistic insight | Why should the proposed intervention change that behavior? |
| Decisive comparison | Which measured comparison supports or contradicts the claim? |
| Falsification | Which outcome would make the claim false or materially weaker? |

## Claim ledger

For each claim, record:

- stable claim ID;
- claim text and scope;
- status: `hypothesis`, `planned`, `partial`, `measured`, or `contradicted`;
- experiment ID and metric;
- source artifact path;
- exact supporting value or qualitative observation;
- limitation and unresolved condition.

## Artifact roles

Maintain exactly one current path for each applicable role:

- experiment specification;
- raw result;
- aggregate result;
- main table source;
- claim ledger;
- manuscript section;
- figure source;
- rendered figure;
- round ledger.

When a role changes, update its source and every downstream dependency in the same round.
