# Main-table design

## Row selection

Choose rows by reviewer question:

- lower bound or simple heuristic;
- strong comparable baseline;
- closest method family;
- proposed full system;
- upper bound or oracle only when its information advantage is explicit.

Group rows by role and disclose backbone, data, tools, budget, and tuning differences.

## Column selection

Order columns as:

1. primary task metric;
2. generality slices;
3. reliability or uncertainty;
4. efficiency when claimed.

Keep mechanism evidence in an ablation table unless it is central to the headline claim.

## Formatting

- state metric direction and unit in the header;
- state aggregation and sampling unit in the caption or note;
- recompute best and second-best marks from displayed values;
- never compare measured values with theoretical maxima as if both were empirical;
- explain missing values with a reason rather than silently dropping cells.
