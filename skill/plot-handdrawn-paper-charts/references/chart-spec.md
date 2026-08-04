# Chart specification

## Contents

1. [Top-level structure](#top-level-structure)
2. [Figure fields](#figure-fields)
3. [Shared panel fields](#shared-panel-fields)
4. [Palette roles](#palette-roles)
5. [Horizontal bar](#horizontal-bar)
6. [Grouped bar](#grouped-bar)
7. [Line chart](#line-chart)
8. [Legends and annotations](#legends-and-annotations)
9. [Data-unit rules](#data-unit-rules)
10. [Output bundle](#output-bundle)

## Top-level structure

The renderer accepts one UTF-8 JSON object:

```json
{
  "data_status": "verified measurement",
  "figure": {
    "stem": "result_figure",
    "size": "double-column",
    "rows": 1,
    "cols": 2
  },
  "panels": [
    {
      "type": "horizontal_bar",
      "title": "Failure Reasons",
      "labels": ["Reason A", "Reason B", "Reason C"],
      "values": [42, 35, 23]
    },
    {
      "type": "line",
      "title": "Accuracy by Budget",
      "x": [0, 5, 10, 20],
      "series": [
        {"name": "Method", "values": [24.5, 27.6, 30.2, 34.1]}
      ]
    }
  ]
}
```

`panels` are placed row-major. The number of panels must not exceed `rows × cols`; unused cells are hidden.

## Figure fields

| Field | Type | Default | Meaning |
|---|---|---|---|
| `stem` | string | `handdrawn_chart` | Output filename stem; letters, digits, dot, dash, underscore only |
| `size` | string | `single-column` | `single-column`, `double-column`, or `double-column-grid` |
| `width_in`, `height_in` | number pair | unset | Explicit size; provide both to override `size` |
| `rows`, `cols` | integer | `1`, `1` | Panel grid |
| `palette` | string | `ocean-blue` | One of the 12 single-hue palettes in `references/color-system.md` |
| `sketch` | string | `subtle` | `none`, `subtle`, or `rough` |
| `font_family` | string | bundled font | Requested family; bundled Comic Neue is portable |
| `font_size` | number | `8.0` | Base point size |
| `title_size` | number | base + 3 | Panel title size |
| `label_size` | number | base + 0.2 | Axis-title size |
| `tick_size` | number | base - 0.3 | Tick-label size |
| `legend_size` | number | base - 0.5 | Legend-label size |
| `dpi` | positive integer | `300` | PNG resolution |
| `wspace`, `hspace` | number | `0.08`, `0.10` | Constrained-layout panel spacing |
| `w_pad`, `h_pad` | number | `0.055`, `0.055` | Outer layout padding in inches |
| `title` | string | unset | Optional figure-level title |
| `transparent` | boolean | `false` | Transparent export background |
| `sharex`, `sharey` | boolean | `false` | Shared axes across panels |

Presets use 3.45 inches for single-column width and 7.10 inches for double-column width. Override these only when the target template requires a different measure.

## Shared panel fields

All panels accept:

- `title`, `title_loc`, `title_pad`, `title_weight`
- `x_label`, `y_label`, `x_label_pad`, `y_label_pad`
- `x_lim: [min, max]`, `y_lim: [min, max]`
- `x_ticks`, `y_ticks`, `x_tick_labels`, `y_tick_labels`
- `x_tick_format`, `y_tick_format`: `number`, `percent`, `integer`, `one_decimal`, or `k`
- `x_tick_rotation`
- `grid`: `x`, `y`, `both`, `none`, `true`, or `false`; `true` uses the chart-type default axis
- `spines`: `box`, `open`, or `none`
- `panel_label`: such as `(a)`
- `palette`: optional per-panel palette override
- `legend`: object or `false`

Tick formatters add presentation suffixes but do not transform values. A value of `34.7` with `percent` displays as `34.7%`. A value of `0.347` displays as `0.347%`.

## Palette roles

Each curated palette exposes `primary`, `secondary`, `tertiary`, `accent`, `neutral`, and `pale`. Prefer semantic roles to explicit hex values when a figure should support palette switching.

```json
{
  "figure": {"palette": "ink-indigo"},
  "panels": [
    {
      "type": "line",
      "x": [0, 10, 20],
      "series": [
        {"name": "Baseline", "values": [61.2, 62.4, 63.1], "color_role": "neutral"},
        {"name": "Proposed", "values": [62.0, 65.1, 68.2], "color_role": "primary"}
      ]
    }
  ]
}
```

Set `palette` at figure level for a consistent composition. Override it on one panel only when that panel has a genuinely different semantic domain. The renderer records figure and panel palette selections in the manifest.

Use either `color` or `color_role` for a series, not both. Use either `colors` or `color_roles` for horizontal-bar categories, not both.

## Horizontal bar

Required fields:

```json
{
  "type": "horizontal_bar",
  "labels": ["Reason A", "Reason B", "Reason C"],
  "values": [48, 31, 21]
}
```

Optional fields:

- `sort`: `none`, `ascending`, or `descending`
- `label_mode`: `axis` or `legend`
- `colors`: one valid Matplotlib color per category; exact length must match `values`
- `color_roles`: one semantic role per category; exact length must match `values`
- `hatches`: one hatch per category; exact length must match `values`
- `bar_height`, `bar_linewidth`
- `value_labels`: boolean
- `value_format`: `number`, `percent`, `integer`, `one_decimal`, or a string such as `{value:.2f}`

When `value_labels` is true, the renderer places labels beyond the bar edge. Reserve x-axis headroom with `x_lim` when labels are long.

Example with legend labels:

```json
{
  "type": "horizontal_bar",
  "title": "Why Flights Ended Early",
  "labels": ["Wonky Wing", "Loose Fold", "Lamp Encounter", "Snack Break"],
  "values": [31, 32, 25, 12],
  "color_roles": ["primary", "tertiary", "secondary", "pale"],
  "hatches": ["///", "", "xx", ""],
  "label_mode": "legend",
  "x_lim": [0, 50],
  "x_tick_format": "percent",
  "legend": {"loc": "lower right"}
}
```

## Grouped bar

Required fields:

```json
{
  "type": "grouped_bar",
  "categories": ["Small", "Medium", "Large"],
  "series": [
    {"name": "Correct", "values": [12, 24, 18]},
    {"name": "Incorrect", "values": [4, 8, 11]}
  ]
}
```

Series fields:

- `name`, `values`
- `color` or `color_role`, plus `edgecolor`, `hatch`, `linewidth`
- `errors`: non-negative symmetric error magnitude for each bar

Panel fields:

- `group_width`: total width occupied by one category group
- `bar_width_fraction`: spacing inside the group
- `error_capsize`
- `colors`, `hatches`: defaults for series that omit local values; exact length must match `series`
- `value_labels`, `value_format`

Use the same category order for every series. The validator rejects a length mismatch.

## Line chart

Required fields:

```json
{
  "type": "line",
  "x": [0, 10, 20, 40],
  "series": [
    {"name": "Baseline", "values": [34.7, 35.2, 35.6, 37.2]},
    {"name": "Proposed", "values": [34.7, 35.4, 36.8, 39.1]}
  ]
}
```

Series fields:

- `name`, `values`
- `color` or `color_role`, plus `linewidth`, `linestyle`
- `marker`, `markersize`, `marker_facecolor`, `marker_edgecolor`, `marker_edgewidth`; omitted markers cycle through distinct print-safe shapes
- `markevery`: Matplotlib-compatible marker selection
- `lower`, `upper`: paired uncertainty bounds; both are required together, share null positions, satisfy `lower <= upper`, and contain the finite estimate
- `band_alpha`
- `zorder`

Use JSON `null` for a genuinely unobserved series position. It creates a visible gap rather than connecting unrelated points:

```json
{
  "name": "Late-stage Method",
  "values": [null, null, 36.8, 38.4]
}
```

Semantic guides:

```json
{
  "vertical_guides": [
    {"x": 20, "label": "Phase 2", "color": "#B87945"}
  ],
  "horizontal_guides": [
    {"y": 37.2, "label": "Baseline", "color": "#667085"}
  ]
}
```

Endpoint or checkpoint emphasis:

```json
{
  "highlights": [
    {
      "series": "Proposed",
      "index": -1,
      "marker": "*",
      "size": 160,
      "facecolor": "#E7894C"
    }
  ]
}
```

A highlight must reference an existing, non-null series value. Explain its meaning in the caption or nearby annotation.

## Legends and annotations

Supported legend fields:

- `loc`
- `bbox_to_anchor: [x, y]`
- `ncol`
- `fontsize`
- `frameon`
- `handlelength`, `handletextpad`
- `labelspacing`, `columnspacing`, `borderaxespad`
- `title`

Disable a legend with `"legend": false`.

Annotations are explicit data-coordinate objects and work on all supported panel types:

```json
{
  "annotations": [
    {
      "text": "Best checkpoint",
      "x": 40,
      "y": 39.1,
      "text_x": 32,
      "text_y": 40.0,
      "arrow": true
    }
  ]
}
```

## Data-unit rules

1. Supply the display unit you want on the axis. The renderer never multiplies fractions by 100.
2. Keep counts as counts and percentages as percentage points. Do not mix the two in one axis without an explicit secondary-axis design outside this renderer.
3. Keep complete arrays. Do not replace middle values with an ellipsis token.
4. Use `null` only when the absence itself is true and should break a line.
5. Keep simulated, measured, inferred, and table-anchored values labeled in the source data or a sibling provenance file.
6. Use uncertainty bounds from the same estimator and confidence convention for all compared series.

## Output bundle

For stem `result_figure`, the renderer creates:

- `result_figure.pdf`
- `result_figure.svg`
- `result_figure.png`
- `result_figure.gray.png`
- `result_figure.source.json`
- `result_figure.manifest.json`

The renderer writes the complete bundle to a staging directory, verifies every artifact, and then replaces the prior bundle. A failed validation or export therefore leaves no partial new bundle. PDF/SVG timestamps are suppressed so repeated renders are byte-stable on the same runtime stack.

The manifest records the input filename and hash, renderer hash, Python and library versions, resolved font, figure and panel palette profiles, palette-aesthetic audit metrics, figure size, DPI, panel count, artifact hashes, byte sizes, PNG pixel dimensions, and verification status. Artifact paths are relative to the manifest, so moving or publishing the directory does not leak workstation paths.
