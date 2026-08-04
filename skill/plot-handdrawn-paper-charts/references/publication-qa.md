# Publication QA

Use this checklist after the renderer succeeds and before describing the chart as paper-ready.

## Numerical integrity

- Compare every plotted array with the source table or code.
- Confirm category and series order.
- Confirm denominators, units, percent scaling, and rounding.
- Confirm that `null` marks genuine missingness and not an uncollected value being hidden.
- Confirm error bars or bands use the stated estimator and interval.
- Confirm highlighted checkpoints and guide lines are data-backed.
- Keep illustrative or simulated values visibly separated from measured results.

## Visual hierarchy

- The main comparison is identifiable without reading the caption.
- Titles describe the question rather than restating axis labels.
- The grid is lighter than all data marks.
- Baselines are visually quieter than the proposed method.
- One color has one meaning across panels.
- Palette choice follows the analytical relationship and target tone, not decoration alone.
- Focal, comparison, baseline, and uncertainty elements use stable semantic roles.
- No more than two series compete for strongest visual salience in one panel.
- Hatches and markers remain distinct in grayscale.
- A star, bold outline, or annotation has an explicit semantic reason.

## Labels and legends

- No title, tick, category, or legend text is clipped.
- No data label is placed inside a narrow filled bar.
- Long bar labels use a y axis or a compact in-panel legend, whichever scans faster.
- Legends do not cover data, uncertainty bands, or guide labels.
- Multi-line titles use intentional line breaks.
- Acronyms are defined in the caption or manuscript text.
- All text is readable at the final manuscript width, not only when zoomed.

## Paper layout

- Match the actual single- or double-column width.
- Inspect the color PNG at final size.
- Inspect the grayscale PNG at final size.
- Prefer open spines for dense technical panels and boxed spines when matching the reference hand-drawn grammar.
- Remove unnecessary panel whitespace before reducing font size.
- Keep line widths and marker sizes consistent across a multi-panel figure.

## Vector and font checks

- Open the PDF and SVG after export.
- Confirm the PDF begins with a valid PDF signature and the SVG contains an SVG root.
- Confirm the manifest status is `verified`.
- Confirm every manifest artifact path is relative to the manifest and contains no workstation-specific directory.
- When byte reproducibility matters, render twice on the same recorded runtime stack and compare all six SHA-256 values.
- Use `pdffonts figure.pdf` when available and check that fonts are embedded.
- Keep the bundled Comic Neue OFL license with the skill, not with each paper export.
- Use the PDF or SVG as the manuscript source of record.

## Manuscript alignment

- Caption states the panel purpose, data scope, metric semantics, comparison set, and supported takeaway.
- Caption does not promote a layout fixture, interpolated point, or partial run to a measured result.
- Colors and method names match the main tables.
- Figure callouts in the text match panel labels.
- The result remains interpretable when printed in grayscale.
- The manifest records the intended figure palette and every panel override.

## Delivery evidence

Return or retain all six roles:

1. PDF for manuscript inclusion.
2. SVG for editing.
3. Color PNG for visual review.
4. Grayscale PNG for print review.
5. Source JSON for exact regeneration.
6. Manifest for hashes and resolved rendering details.
