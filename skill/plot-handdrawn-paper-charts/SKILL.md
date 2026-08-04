---
name: plot-handdrawn-paper-charts
description: Create, restyle, and export hand-drawn or handwritten academic charts from verified data, including horizontal bars, grouped bars, training curves, line plots, and multi-panel figures. Use for 手绘风、手写风、漫画式但适合论文的柱状图或折线图, paper Figure redesigns, error distributions, correct-vs-incorrect comparisons, ablation or scaling curves, palette switching, or Matplotlib chart code that needs curated publication color aesthetics. Provides 12 semantic palette systems, editable PDF/SVG, 300-dpi PNG, grayscale QA, and a reproducibility manifest.
---

# FigureInk: Plot Hand-drawn Paper Charts

Create quantitative figures with hand-lettered warmth while retaining paper-grade precision, editability, and evidence traceability. Use the bundled renderer rather than image generation so every plotted mark remains tied to declared data.

## Operating contract

- Preserve every supplied number, label, category order, uncertainty value, and series boundary unless the user explicitly requests a transformation.
- Never infer missing results. If only layout testing is possible, mark the entire fixture as illustrative and keep it separate from paper-ready output.
- Keep the hand-drawn effect restrained: hand-lettered type, dark outlines, curated low-saturation color, optional hatch, and only subtle path perturbation.
- Export PDF and SVG for editing, PNG at 300 dpi for inspection, a grayscale PNG, the resolved source JSON, and a portable manifest containing hashes and runtime versions.
- Do not rasterize text into a generated picture and do not use decorative marks that can be mistaken for data semantics.

## Workflow

1. **Inspect the source.** Read the user's data table and any plotting code. Record the exact plot type, dimensions, units, axis ranges, series joins, highlighted checkpoints, and provenance constraints.
2. **Select the layout.** Use `single-column` for one compact panel, `double-column` for a wide row, or `double-column-grid` for a 2×2 composition. Prefer one message per panel and one visual hierarchy for the full figure.
3. **Choose color semantically.** Read `references/color-system.md`. Select a palette from the analytical relationship and map entities to `primary`, `secondary`, `tertiary`, `accent`, `neutral`, or `pale`; do not choose colors independently by decoration.
4. **Build a JSON specification.** Copy `assets/example_showcase.json` and replace all synthetic values and labels. Read `references/chart-spec.md` when using uncertainty bands, guide lines, missing segments, annotations, or custom legends.
5. **Validate before drawing.** Run the renderer with `--validate-only`. Resolve every length mismatch, unknown palette role, or unknown series reference rather than dropping values.
6. **Render reproducibly.** Run `scripts/render_chart.py` with the verified spec and a dedicated output directory. The renderer suppresses PDF/SVG timestamps, stages the full bundle before replacement, and keeps the emitted manifest beside the figure.
7. **Inspect twice.** View the color PNG at intended paper size and the grayscale PNG. Check clipping, collisions, small labels, ambiguous line identity, hatch density, palette balance, and whether the emphasized point has an explained meaning.
8. **Iterate in place.** Update the same spec and overwrite the same output stem. Do not create `_v2`, `_final2`, or similar duplicates.
9. **Deliver the evidence bundle.** Return the PDF, SVG, PNG, source JSON, grayscale QA, and manifest. State which data fields and semantic roles were mapped to each visual encoding.

## Chart selection

- Use `horizontal_bar` for ranked reasons, taxonomies, and long category labels. Put direct values outside the bar when requested. Use `label_mode: "legend"` only when the in-panel legend is easier to scan than y-axis labels.
- Use `grouped_bar` for matched comparisons over the same categories. Distinguish series with both color and hatch when grayscale reproduction matters.
- Use `line` for ordered steps, budgets, time, or scale. Use `null` only for genuinely absent segments; the renderer preserves the gap. Add lower and upper arrays together for uncertainty bands.
- Use a multi-panel grid only when panels share a narrative and visual grammar. Keep colors semantically stable across panels.

## Visual grammar

- Default typeface: bundled open-licensed Comic Neue; system Comic Sans MS and Chalkboard are fallbacks.
- Default ink: `#252A34`; grid: `#D9DEE7`; background: white.
- Default palette: `ocean-blue`. Other single-hue choices are `ink-indigo`, `sage-green`, `forest-green`, `lagoon-teal`, `plum-purple`, `lavender`, `dusty-rose`, `sunset-orange`, `terracotta`, `ochre-gold`, and `graphite`.
- Use `primary` for the focal method, `neutral` for a baseline, `secondary` for a peer comparison, `accent` for one meaningful checkpoint, and `pale` for bands or background context. All six roles stay inside the selected hue family.
- Keep no more than two highly salient series in one panel; avoid rainbow ordering and unrelated colors with equal visual weight.
- Use `sketch: "subtle"` by default. Use `none` for camera-ready venues with very small figures. Reserve `rough` for posters or explicitly playful drafts.
- Use dark edges, white-centered line markers, and one endpoint star only when the endpoint is substantively special.
- Keep titles short, axes explicit, legends frameless, and grids lighter than every data mark.

## Commands

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/plot-handdrawn-paper-charts"

python3 "$SKILL_DIR/scripts/render_chart.py" \
  --spec /absolute/path/to/figure.json \
  --validate-only

python3 "$SKILL_DIR/scripts/render_chart.py" \
  --spec /absolute/path/to/figure.json \
  --output-dir /absolute/path/to/output \
  2>&1 | tee /absolute/path/to/render.log

python3 "$SKILL_DIR/scripts/render_chart.py" --list-palettes
```

The render succeeds only after reopening and checking the source JSON, PDF, SVG, and PNG. Inspect the manifest for relative artifact paths, the resolved font, runtime versions, size, hashes, pixel dimensions, and verification status.

## Quality gates

- Read `references/publication-qa.md` before calling a figure paper-ready.
- Do not abbreviate or omit data points with visual or textual ellipses.
- Keep bar-value labels outside the filled rectangle.
- Ensure color is not the sole encoding for series that must survive grayscale printing.
- Apply one semantic role consistently across panels; changing the palette name must not change the entity meaning.
- Confirm percent values are already expressed in displayed percentage points; the renderer formats but never rescales them.
- Require non-negative error magnitudes and ordered lower/upper uncertainty bounds; validation rejects malformed intervals before creating output.
- Make the PDF/SVG the manuscript source of record and use PNG only for preview or raster-only submission systems.

## Resources

- `scripts/render_chart.py`: schema validation, rendering, multi-format export, reopening, and manifest generation.
- `requirements.txt`: minimal Python runtime dependencies for the deterministic renderer.
- `LICENSE`: MIT terms for the renderer and skill documentation.
- `assets/example_showcase.json`: seeded synthetic three-panel fixture showing both bar types, error bars, an uncertainty band, and line-series emphasis.
- `assets/example_palette_gallery.json`: all 12 curated palettes rendered through the six semantic roles.
- `assets/fonts/`: bundled Comic Neue regular and bold fonts with their OFL license.
- `references/chart-spec.md`: supported JSON fields and advanced examples.
- `references/color-system.md`: palette-selection matrix, role semantics, aesthetic rules, and accessibility guidance.
- `references/publication-qa.md`: numerical, visual, vector, and final-size review checklist.
