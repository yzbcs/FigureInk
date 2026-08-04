# Curated color system

## Contents

1. [Design standard](#design-standard)
2. [Semantic roles](#semantic-roles)
3. [Palette selection matrix](#palette-selection-matrix)
4. [Chart-specific rules](#chart-specific-rules)
5. [Accessibility and grayscale](#accessibility-and-grayscale)
6. [Switching palettes](#switching-palettes)
7. [Custom-color review](#custom-color-review)

## Design standard

Choose color from the analytical relationship, not from decoration alone.

1. Use one dominant hue family for the entire figure; derive every semantic role from that hue.
2. Keep no more than two highly salient series in one panel. Relegate baselines and context to `neutral` or `pale`.
3. Keep the same semantic role and color for a method across every panel.
4. Use lightness and saturation for visual hierarchy, then add hatch, marker, or line-style differences for categories.
5. Reserve `accent` for one checkpoint, intervention, warning, or focal annotation.
6. Use `pale` for uncertainty bands, reference regions, backgrounds, or secondary bars; do not use it for a thin primary line.
7. Retain dark ink outlines and light grids so the hand-drawn style stays precise rather than childish.
8. Avoid rainbow ordering, neon saturation, cross-family accent colors, and unrelated colors with equal visual weight.

Every curated preset is a single-hue family with dark, medium, muted, and pale steps. Presets use softened chroma, a white background, `#252A34` ink, and `#D9DEE7` grids. This keeps color subordinate to the quantitative structure and makes multi-panel figures feel like one composition.

The renderer also applies four catalog guardrails before drawing: primary-secondary normalized RGB distance must be at least `0.25`, maximum circular hue distance from `primary` must not exceed `0.04`, the `pale` role must have relative luminance of at least `0.65`, and `neutral` HSV saturation must not exceed `0.32`. These checks prevent near-duplicate focal colors, cross-family drift, muddy uncertainty fills, and colorful baselines. They supplement rather than replace color and grayscale inspection.

## Semantic roles

Every palette exposes the same six roles:

| Role | Intended use |
|---|---|
| `primary` | Proposed method, main result, or most important category |
| `secondary` | Direct peer comparison or second focal series |
| `tertiary` | Third meaningful category without stealing focus |
| `accent` | One special checkpoint, phase, warning, or callout |
| `neutral` | Baseline, reference, context, or non-focal series |
| `pale` | Confidence band, background region, low-priority bar, or fill |

Use roles rather than hard-coded hex values when the same figure may be recolored later. A single palette-name change then preserves the semantic mapping.

## Palette selection matrix

| Palette | Tone | Prefer for |
|---|---|---|
| `ocean-blue` | Calm, familiar, technical | Default general paper figures and two-method comparisons |
| `ink-indigo` | Formal, focused, premium | Headline results and compact method-versus-baseline figures |
| `sage-green` | Gentle, editorial, human-centered | Human evaluation, qualitative analysis, behavioral studies |
| `forest-green` | Grounded, robust, natural | Efficiency, robustness, sustainability, systems studies |
| `lagoon-teal` | Fresh, contemporary, balanced | General comparisons, interfaces, systems diagrams |
| `plum-purple` | Distinctive, mature, creative | Multimodal, cross-domain, concept-oriented figures |
| `lavender` | Soft, exploratory, elegant | Supporting analyses, education, qualitative studies |
| `dusty-rose` | Warm, restrained, narrative | Error taxonomies, preferences, human-centered comparisons |
| `sunset-orange` | Warm, expressive | Motivation figures, distributions, visual storytelling |
| `terracotta` | Hand-crafted, explanatory | Failure analysis and warm reference-style panels |
| `ochre-gold` | Classic, warm, understated | Efficiency results, highlights, historical comparisons |
| `graphite` | Understated, print-first | Grayscale submission, baselines, secondary evidence |

Default to `ocean-blue` when the task supplies no mood or domain signal. Prefer `graphite` plus redundant markers or hatches when print or color-vision robustness matters more than an editorial tone.

## Chart-specific rules

### Two-series comparison

- Proposed versus baseline: `primary` versus `neutral`.
- Two equally important methods: `primary` versus `secondary`.
- Add hatch or marker differences even when colors are distinct.

### Three-to-six categorical series

- Assign `primary`, `secondary`, `tertiary`, `accent`, `neutral`, then `pale` only if a pale fill remains legible.
- Prefer `ocean-blue`, `ink-indigo`, `plum-purple`, or `graphite`.
- Because the presets intentionally share one hue, add distinct hatches, markers, or direct labels for unordered categories.
- Do not imply ordering through lightness unless the categories are ordered; when categories are unordered, make the redundant encoding prominent.

### Ordered bars or sequential curves

- Use one hue family with lightness progression or one primary line plus pale uncertainty.
- Prefer `ocean-blue`, `forest-green`, or `graphite`.
- Keep the hue fixed and encode magnitude through position first, then lightness only when useful.

### Error and failure analysis

- Use warm palettes such as `terracotta`, `dusty-rose`, or `sunset-orange`.
- Keep benign/reference categories neutral or pale.
- Use the strongest warm color for the category emphasized in the manuscript claim, not automatically for the largest value.

### Multi-panel figures

- Keep one figure-level palette throughout the composition.
- Use a panel-level override only when the user explicitly asks for a semantic boundary between panels; never vary palettes merely for decoration.
- If an override is required, keep shared entities on an identical hex color or semantic role.
- Record all panel selections in the generated manifest.

## Accessibility and grayscale

- Never rely on color as the sole series identifier.
- Pair colors with line style, marker shape, hatch, direct label, or ordering.
- Inspect the generated `.gray.png` at final paper width.
- Use dark outlines for pale bars and filled regions.
- Avoid assigning `pale` and `neutral` to two thin neighboring lines.
- For color-vision-safe categorical distinction, use `ocean-blue` or `graphite` and make redundant encodings mandatory.
- Very pale colors require a dark border and sufficient area; reserve them for bars, patches, or uncertainty regions rather than thin lines.

## Switching palettes

Set a figure-wide palette:

```json
{
  "figure": {"palette": "ink-indigo"}
}
```

Assign semantic roles to series:

```json
{
  "series": [
    {"name": "Baseline", "values": [62.1, 63.0, 63.5], "color_role": "neutral"},
    {"name": "Proposed", "values": [64.4, 66.1, 68.8], "color_role": "primary"}
  ]
}
```

Assign roles to horizontal-bar categories:

```json
{
  "color_roles": ["primary", "secondary", "tertiary", "neutral"]
}
```

Override a single panel only when necessary:

```json
{
  "palette": "sage-green"
}
```

List the machine-readable catalog, including the four aesthetic-audit metrics:

```bash
python3 scripts/render_chart.py --list-palettes
```

View `assets/example_palette_gallery.json` and its rendered gallery before selecting a palette by visual tone alone.

## Custom-color review

When the user supplies brand or project colors:

1. Map each supplied color to a semantic role.
2. Reduce excessive saturation rather than mixing neon colors with the curated system.
3. Derive secondary, tertiary, accent, neutral, and pale roles from the same dominant hue.
4. Check that adjacent categorical colors differ in lightness and have a redundant marker, line style, hatch, or label.
5. Check the figure in grayscale.
6. Keep explicit colors in the JSON only when brand fidelity is more important than palette switching.
7. Record custom colors in the source JSON and manifest through the normal reproducibility bundle.
