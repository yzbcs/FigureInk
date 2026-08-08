---
name: design-paper-figures
description: Design and produce editable scientific paper figures for introduction motivation, method overviews, and experiment narratives. Use when a user asks how to draw an intro figure, teaser, motivation diagram, method main figure, architecture or pipeline figure, experiment figure, multi-panel paper visual, figure brief, visual redesign, or before-after figure comparison. Separate conceptual diagrams from exact quantitative plots; use the bundled story renderer for editable concept diagrams and route measured charts to plot-handdrawn-paper-charts.
---

# Design Paper Figures

Convert the paper's argument into a visual hierarchy before choosing decoration. Produce editable SVG/PDF plus a PNG preview for conceptual figures; keep exact experimental values in a deterministic plotting workflow.

## Operating contract

- Start from the paper's research question, failure mode, mechanism, and decisive evidence.
- Keep conceptual graphics and quantitative plots separate. Never place invented measurements in a conceptual diagram.
- Preserve exact method component names and execution order from the implementation or manuscript.
- Use one visual sentence per figure and one reading direction per panel.
- Keep text short enough to read at final paper size; move explanation into the caption.
- Reopen the SVG/PDF and PNG after rendering. Iterate on the same source specification and stem.

## Figure selection

### Introduction figure

Use a four-beat story: **setting -> failure -> insight -> payoff**. Show a concrete contrast that makes the gap visible. Prefer paired outcomes or a single cause-and-effect chain over a generic architecture.

Read `references/intro-figure.md` when the figure is a teaser, motivation panel, or Figure 1.

### Method main figure

Use a stable pipeline: **inputs -> novel mechanism -> intermediate state -> outputs/objective**. Give the novel block the strongest visual weight. Match the method section's terminology and order exactly.

Read `references/method-figure.md` for architecture, training/inference, feedback loops, and multi-stage methods.

### Experiment figure

Start from one question such as “where does the gain come from?” or “how does performance change with budget?” Use exact results, uncertainty, and denominators. Route bars, curves, and quantitative panels to `plot-handdrawn-paper-charts`.

Read `references/experiment-figure.md` before designing the panel map.

## Workflow

1. **Extract a story card.** Record audience, figure role, one-sentence takeaway, evidence status, required entities, forbidden implications, and final size.
2. **Choose the figure grammar.** Select intro, method, or experiment. Do not start from a preferred visual style.
3. **Storyboard in text.** Write each panel as `subject + action + consequence`. Remove any panel that does not advance the takeaway.
4. **Map semantics to marks.** Assign stable roles to focal method, baseline, data, process, output, warning, and evidence. Keep those roles consistent across panels.
5. **Build a JSON story specification.** Copy `assets/example_intro_figure.json` or `assets/example_method_figure.json`. Use normalized coordinates so the layout remains editable.
6. **Render conceptual figures.** Run `scripts/render_story_figure.py`. For measured plots, use `plot-handdrawn-paper-charts` instead.
7. **Critique in three passes.** Check semantic correctness, reading order, then aesthetics. Do not use aesthetics to hide a missing causal link.
8. **Inspect at final size.** Check text, arrow routing, alignment, color meaning, grayscale differentiation, and caption independence.
9. **Deliver the bundle.** Return source JSON, SVG, PDF, PNG, and a short mapping from claim beats to visual elements.

## Commands

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/design-paper-figures"

python3 "$SKILL_DIR/scripts/render_story_figure.py" \
  --spec /absolute/path/to/figure-story.json \
  --validate-only

python3 "$SKILL_DIR/scripts/render_story_figure.py" \
  --spec /absolute/path/to/figure-story.json \
  --output-dir /absolute/path/to/output \
  2>&1 | tee /absolute/path/to/render.log
```

## Quality gates

- A reader should recover the intended takeaway in five seconds without reading the body text.
- The focal method should be visually dominant for a reason, not merely because it is colorful.
- Every arrow must express a named relation such as data flow, control, feedback, contrast, or supervision.
- Intro figures must show the real failure and insight; method figures must expose the real computation; experiment figures must encode real values.
- Do not use screenshots or generated raster text when native vector shapes are sufficient.
- Do not repeat the title inside every panel.
- Captions must state what is shown, how to read encodings, and what conclusion is supported.

## Resources

- `scripts/render_story_figure.py`: validate and render editable conceptual diagrams.
- `assets/example_intro_figure.json`: setting-failure-insight-payoff example.
- `assets/example_method_figure.json`: input-mechanism-state-output example.
- `references/figure-grammar.md`: shared visual semantics and critique rubric.
- `references/intro-figure.md`: intro/teaser patterns.
- `references/method-figure.md`: method overview patterns.
- `references/experiment-figure.md`: measured panel planning.
