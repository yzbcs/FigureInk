<div align="center">

# ✏️ FigureInk

**Straight data. Hand-drawn character.**

Turn verified numbers into warm, hand-lettered academic figures—without turning your data into pixels you can no longer audit.

![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-315F8C?style=flat-square)
![Charts](https://img.shields.io/badge/charts-bars%20%7C%20lines%20%7C%20panels-B85A3A?style=flat-square)
![Palettes](https://img.shields.io/badge/curated%20palettes-12-2F6F73?style=flat-square)
![Exports](https://img.shields.io/badge/exports-PDF%20%7C%20SVG%20%7C%20PNG-D3A33F?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-657C6A?style=flat-square)

![Seeded synthetic paper-plane field test in a playful hand-drawn style](showcase/hero/paper-plane-lab-showcase.png)

</div>

## Why this exists

Most paper plots live at one of two extremes: perfectly precise but visually forgettable, or delightfully hand-drawn but detached from the underlying data. This project keeps the charm **and** the contract.

**FigureInk** is a Codex-compatible skill with a deterministic Matplotlib renderer. It gives charts a restrained hand-made voice while preserving every declared value, category, gap, uncertainty interval, and highlight. Its installable Skill ID remains `plot-handdrawn-paper-charts`, so requests stay descriptive and easy for Codex to route.

> Think “lab notebook with excellent taste,” not “cartoon filter.”

## Meet the paper-plane lab

The hero figure is intentionally a little ridiculous—and entirely synthetic. A local
generator invents **100 pretend flight endings**, repeated soft-landing trials, and two
fold-tuning trajectories using seed `20260804`. One coherent blue palette ties all
three panels together. No manuscript numbers, benchmark results, or real measurements
are hiding in the doodles.

```bash
python3 showcase/generate_synthetic_showcase.py
```

That command rebuilds the exact JSON fixture. Change `--seed` and the tiny paper-plane
lab will have a brand-new (equally fictional) afternoon.

## What you get

| Capability | What it means in practice |
|---|---|
| **Data-bound drawing** | Bars, lines, gaps, error bars, and confidence bands come directly from JSON. |
| **Three chart families** | Horizontal bars, grouped bars, and line charts, composed into publication-sized grids. |
| **12 single-hue palettes** | Semantic roles—`primary`, `secondary`, `tertiary`, `accent`, `neutral`, and `pale`—vary within one color family. |
| **Paper-ready exports** | Editable PDF/SVG, 300-dpi PNG, grayscale preview, resolved source JSON, and a verification manifest. |
| **Strict preflight** | Bad lengths, colors, bounds, error magnitudes, axes, references, and style enums fail before output is created. |
| **Reproducible bundles** | Timestamp-free PDF/SVG, relative manifest paths, runtime provenance, hashes, and staged replacement. |
| **Portable typography** | Comic Neue Regular/Bold are bundled under the SIL Open Font License. |

## The palette shelf

![Twelve curated semantic palettes](showcase/palettes/plot-handdrawn-paper-charts-palettes.png)

Choose by analytical intent, not by spinning a color wheel:

Each row is a self-contained hue family. Roles change in lightness and saturation;
hatches, markers, and line styles carry categorical separation without palette hopping.

| Palette | Personality | Good for |
|---|---|---|
| `ocean-blue` | calm, familiar | default paper figures |
| `ink-indigo` | formal, focused | headline results |
| `sage-green` | gentle, editorial | human evaluation |
| `forest-green` | grounded, robust | systems and efficiency |
| `lagoon-teal` | fresh, balanced | general comparisons |
| `plum-purple` | distinctive, mature | multimodal work |
| `lavender` | soft, exploratory | supporting analyses |
| `dusty-rose` | warm, restrained | preferences and taxonomies |
| `sunset-orange` | expressive | motivation figures |
| `terracotta` | explanatory, crafted | failure analysis |
| `ochre-gold` | classic, understated | highlights and efficiency |
| `graphite` | print-first | monochrome submissions |

## Install the Skill

### The easy way: just ask Codex

Open this repository in Codex—or paste its GitHub URL into a Codex task—and say:

```text
Install the open-source FigureInk Codex Skill from
https://github.com/yzbcs/FigureInk. The skill package is in
skill/plot-handdrawn-paper-charts. Install its dependencies, place it in my
Codex skills directory, validate the bundled examples, and tell me when it is
ready.
```

That is enough. Codex can inspect `SKILL.md`, install the small Python runtime,
copy the skill into your local skills directory, and run a smoke render.

### Manual installation

```bash
git clone https://github.com/yzbcs/FigureInk.git
cd FigureInk

python3 -m pip install -r skill/plot-handdrawn-paper-charts/requirements.txt

SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$SKILLS_DIR"
cp -R skill/plot-handdrawn-paper-charts "$SKILLS_DIR/"
```

### Use it

```text
Use $plot-handdrawn-paper-charts to turn these verified results into a
double-column hand-drawn line chart. Use a print-safe palette and include
a confidence band, a grayscale check, and the reproducibility manifest.
```

### Or run the renderer directly

```bash
SKILL_DIR="$PWD/skill/plot-handdrawn-paper-charts"
SPEC="$SKILL_DIR/assets/example_showcase.json"

# Preflight only: creates no artifacts.
python3 "$SKILL_DIR/scripts/render_chart.py" \
  --spec "$SPEC" \
  --validate-only

# Render the full six-file evidence bundle.
python3 "$SKILL_DIR/scripts/render_chart.py" \
  --spec "$SPEC" \
  --output-dir "$PWD/rendered"

# Browse the palette catalog as JSON.
python3 "$SKILL_DIR/scripts/render_chart.py" --list-palettes
```

## A tiny specification

```json
{
  "data_status": "synthetic tutorial fixture",
  "figure": {
    "stem": "paper_plane_range",
    "size": "single-column",
    "palette": "ink-indigo",
    "sketch": "subtle",
    "dpi": 300
  },
  "panels": [
    {
      "type": "line",
      "x": [1, 2, 3, 4],
      "x_label": "Fold-tuning round",
      "y_label": "Flight range (m)",
      "series": [
        {
          "name": "Dart",
          "values": [3.2, 3.6, 4.1, 4.5],
          "color_role": "neutral"
        },
        {
          "name": "Loopwing",
          "values": [3.1, 3.9, 4.8, 5.6],
          "color_role": "primary"
        }
      ]
    }
  ]
}
```

The renderer never rescales percentages or fills in missing measurements. Use JSON `null` for a genuine line gap; it stays a gap.

## One command, six accountable files

For a stem named `paper_plane_range`, a normal render produces:

```text
paper_plane_range.pdf
paper_plane_range.svg
paper_plane_range.png
paper_plane_range.gray.png
paper_plane_range.source.json
paper_plane_range.manifest.json
```

The manifest records the source and renderer hashes, runtime versions, selected palette roles, resolved font, dimensions, DPI, artifact hashes, byte sizes, and PNG dimensions. Paths are relative, so the bundle can move from a workstation to a repository without publishing a home directory.

## Integrity before decoration

The fun look is deliberately downstream of strict checks:

- every category/series length must match;
- error magnitudes must be non-negative;
- lower and upper bounds must agree and contain finite estimates;
- highlights must reference a real, non-null point;
- explicit colors and palette roles must be valid;
- axis limits, ticks, labels, dimensions, and DPI must be coherent;
- exports are staged, reopened, hashed, and committed as one bundle;
- a failed validation leaves zero new artifacts;
- repeated renders are byte-identical on the same recorded runtime stack.

No numbers were harmed in the making of these doodles.

## Repository map

```text
.
├── README.md
├── LICENSE
├── THIRD_PARTY_NOTICES.md
├── skill/
│   └── plot-handdrawn-paper-charts/
│       ├── SKILL.md
│       ├── LICENSE
│       ├── agents/openai.yaml
│       ├── assets/
│       │   ├── example_showcase.json
│       │   ├── example_palette_gallery.json
│       │   └── fonts/
│       ├── references/
│       ├── requirements.txt
│       └── scripts/render_chart.py
└── showcase/
│   ├── generate_synthetic_showcase.py
│   ├── hero/
│   └── palettes/
```

## Check that it works

```bash
SKILL_DIR="$PWD/skill/plot-handdrawn-paper-charts"

python3 "$SKILL_DIR/scripts/render_chart.py" \
  --spec "$SKILL_DIR/assets/example_showcase.json" \
  --validate-only

OUTPUT_DIR="$(mktemp -d)"
python3 "$SKILL_DIR/scripts/render_chart.py" \
  --spec "$SKILL_DIR/assets/example_showcase.json" \
  --output-dir "$OUTPUT_DIR"
```

You should see `VALID` followed by six artifact paths. GitHub Actions performs the
same compile, validation, and real-render smoke check without keeping test fixtures
in the repository.

## Design notes

- Use `subtle` sketching for papers, `none` for very small camera-ready figures, and `rough` for playful drafts or posters.
- Keep no more than two highly salient series in one panel.
- Pair color with marker shape or hatch when grayscale reproduction matters.
- Put values outside filled bars.
- Treat PDF/SVG as the manuscript source of record; treat PNG as review material.
- The bundled examples are explicitly illustrative; the hero fixture is seeded synthetic data. Replace every example value before using a chart as evidence.

The full schema lives in [`chart-spec.md`](skill/plot-handdrawn-paper-charts/references/chart-spec.md), the palette logic in [`color-system.md`](skill/plot-handdrawn-paper-charts/references/color-system.md), and the paper-readiness checklist in [`publication-qa.md`](skill/plot-handdrawn-paper-charts/references/publication-qa.md).

## License

Project code and documentation are available under the [MIT License](LICENSE). Bundled Comic Neue font files are distributed under the SIL Open Font License 1.1; see [`assets/fonts/OFL.txt`](skill/plot-handdrawn-paper-charts/assets/fonts/OFL.txt) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
