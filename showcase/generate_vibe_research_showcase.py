#!/usr/bin/env python3
"""Generate the complete synthetic before-after showcase for the skill suite.

The script renders intro and method diagrams with the conceptual story renderer,
renders experiment charts with FigureInk, audits three writing sections, audits
sparse and enriched experiment matrices, and composes a self-contained HTML
report. Every example is explicitly synthetic and is regenerated in place.
"""

from __future__ import annotations

import argparse
import html
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SHOWCASE = ROOT / "showcase" / "vibe-research"
SOURCE = SHOWCASE / "source"
OUTPUT = SHOWCASE / "output"
LOG = ROOT / "assets" / "log" / "vibe_research_showcase.log"

STORY_RENDERER = ROOT / "skill" / "design-paper-figures" / "scripts" / "render_story_figure.py"
CHART_RENDERER = ROOT / "skill" / "plot-handdrawn-paper-charts" / "scripts" / "render_chart.py"
CLAIM_AUDITOR = ROOT / "skill" / "write-paper-sections" / "scripts" / "audit_claim_ledger.py"
MATRIX_AUDITOR = ROOT / "skill" / "design-paper-experiments" / "scripts" / "audit_evidence_matrix.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=SHOWCASE / "index.html")
    return parser.parse_args()


def run(command: list[str]) -> None:
    """Execute one generation step and append its literal command and output.

    The function records each argument without shell interpolation, executes the
    process from the repository root, writes stdout and stderr to the shared log,
    and raises immediately on a nonzero exit. This keeps the showcase generation
    reproducible while retaining the exact diagnostics needed to repair a failed
    renderer or audit step.
    """
    rendered_command = " ".join(command)
    process = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(f"$ {rendered_command}\n")
        handle.write(process.stdout)
        handle.write(process.stderr)
        handle.write(f"exit={process.returncode}\n\n")
    if process.returncode:
        raise RuntimeError(
            f"command failed with exit {process.returncode}: {rendered_command}\n{process.stderr}"
        )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    json.loads(path.read_text(encoding="utf-8"))


def prose_html(text: str) -> str:
    return "".join(
        f"<p>{html.escape(paragraph).replace(chr(10), '<br>')}</p>"
        for paragraph in text.split("\n\n")
    )


def inline_markdown(cell: str) -> str:
    escaped = html.escape(cell.strip())
    if escaped.startswith("**") and escaped.endswith("**"):
        return f"<strong>{escaped[2:-2]}</strong>"
    if escaped.startswith("&lt;u&gt;") and escaped.endswith("&lt;/u&gt;"):
        return f"<u>{escaped[9:-10]}</u>"
    return escaped


def markdown_table_html(markdown: str) -> str:
    """Convert the auditor's complete Markdown table into semantic HTML."""
    lines = [line for line in markdown.splitlines() if line.startswith("|")]
    rows = [[cell for cell in line.strip("|").split("|")] for line in lines]
    if len(rows) < 3:
        raise ValueError("the generated Markdown table is incomplete")
    headers = rows[0]
    body = rows[2:]
    header_html = "".join(f"<th>{inline_markdown(cell)}</th>" for cell in headers)
    body_html = "".join(
        "<tr>" + "".join(f"<td>{inline_markdown(cell)}</td>" for cell in row) + "</tr>"
        for row in body
    )
    return f"<div class=\"table-scroll\"><table><thead><tr>{header_html}</tr></thead><tbody>{body_html}</tbody></table></div>"


def compare_figure(title: str, before: str, after: str, before_note: str, after_note: str) -> str:
    return f"""
    <article class="comparison-block">
      <div class="section-kicker">{html.escape(title)}</div>
      <div class="compare-grid">
        <figure class="compare-card before-card">
          <figcaption><span class="state-dot before-dot"></span>Before</figcaption>
          <img src="{html.escape(before)}" alt="{html.escape(title)} before skill" loading="lazy">
          <p>{html.escape(before_note)}</p>
        </figure>
        <figure class="compare-card after-card">
          <figcaption><span class="state-dot after-dot"></span>After skills</figcaption>
          <img src="{html.escape(after)}" alt="{html.escape(title)} after skill" loading="lazy">
          <p>{html.escape(after_note)}</p>
        </figure>
      </div>
    </article>
    """


def generate_artifacts() -> dict[str, Any]:
    """Render every visual and audit artifact used by the HTML comparison.

    Generation is deliberately staged by modality. Conceptual figure specs are
    rendered first, exact experiment charts second, writing packets third, and
    experiment matrices last. The function then reopens every JSON report and
    returns the resolved comparison data to the HTML builder, ensuring the page
    is based on verified outputs rather than on expected values embedded in code.
    """
    OUTPUT.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("Vibe research showcase generation\n\n", encoding="utf-8")

    story_jobs = [
        (SOURCE / "intro-before.json", OUTPUT / "figures" / "intro"),
        (ROOT / "skill" / "design-paper-figures" / "assets" / "example_intro_figure.json", OUTPUT / "figures" / "intro"),
        (SOURCE / "method-before.json", OUTPUT / "figures" / "method"),
        (ROOT / "skill" / "design-paper-figures" / "assets" / "example_method_figure.json", OUTPUT / "figures" / "method"),
    ]
    for spec, destination in story_jobs:
        run(["python3", str(STORY_RENDERER), "--spec", str(spec), "--output-dir", str(destination)])

    chart_jobs = [
        (SOURCE / "experiment-figure-before.json", OUTPUT / "figures" / "experiment"),
        (SOURCE / "experiment-figure-after.json", OUTPUT / "figures" / "experiment"),
    ]
    for spec, destination in chart_jobs:
        run(["python3", str(CHART_RENDERER), "--spec", str(spec), "--output-dir", str(destination)])

    writing = json.loads((SOURCE / "writing-comparison.json").read_text(encoding="utf-8"))
    writing_reports: dict[str, dict[str, Any]] = {}
    for section in writing["sections"]:
        section_id = section["id"]
        section_dir = OUTPUT / "writing" / section_id
        section_dir.mkdir(parents=True, exist_ok=True)
        (section_dir / "before.md").write_text(section["before"] + "\n", encoding="utf-8")
        (section_dir / "after.md").write_text(section["after"] + "\n", encoding="utf-8")
        for state in ("before", "after"):
            packet_path = section_dir / f"{state}-packet.json"
            report_path = section_dir / f"{state}-audit.json"
            write_json(packet_path, section[f"{state}_packet"])
            command = ["python3", str(CLAIM_AUDITOR), "--packet", str(packet_path), "--report", str(report_path)]
            if state == "after":
                command.append("--strict")
            run(command)
        writing_reports[section_id] = {
            "before": json.loads((section_dir / "before-audit.json").read_text(encoding="utf-8")),
            "after": json.loads((section_dir / "after-audit.json").read_text(encoding="utf-8")),
        }

    experiment_dir = OUTPUT / "experiments"
    experiment_dir.mkdir(parents=True, exist_ok=True)
    before_matrix = SOURCE / "experiment-matrix-before.json"
    after_matrix = ROOT / "skill" / "design-paper-experiments" / "assets" / "example_experiment_matrix.json"
    run([
        "python3", str(MATRIX_AUDITOR), "--matrix", str(before_matrix),
        "--report", str(experiment_dir / "before-audit.json"),
        "--markdown", str(experiment_dir / "before-main-table.md"),
    ])
    run([
        "python3", str(MATRIX_AUDITOR), "--matrix", str(after_matrix),
        "--report", str(experiment_dir / "after-audit.json"),
        "--markdown", str(experiment_dir / "after-main-table.md"), "--strict",
    ])

    return {
        "writing": writing,
        "writing_reports": writing_reports,
        "experiment_before": json.loads((experiment_dir / "before-audit.json").read_text(encoding="utf-8")),
        "experiment_after": json.loads((experiment_dir / "after-audit.json").read_text(encoding="utf-8")),
        "table_before": (experiment_dir / "before-main-table.md").read_text(encoding="utf-8"),
        "table_after": (experiment_dir / "after-main-table.md").read_text(encoding="utf-8"),
    }


def build_html(data: dict[str, Any]) -> str:
    writing_blocks = []
    for section in data["writing"]["sections"]:
        reports = data["writing_reports"][section["id"]]
        changes = "".join(f"<li>{html.escape(item)}</li>" for item in section["changes"])
        writing_blocks.append(f"""
        <article class="writing-block">
          <div class="writing-head">
            <h3>{html.escape(section['label'])}</h3>
            <div class="audit-pair">
              <span class="audit-bad bad">Before · {reports['before']['issue_count']} evidence issue</span>
              <span class="audit-bad good">After · {reports['after']['issue_count']} evidence issue</span>
            </div>
          </div>
          <div class="compare-grid prose-grid">
            <section class="prose-card before-card"><h4>Before</h4>{prose_html(section['before'])}</section>
            <section class="prose-card after-card"><h4>After skills</h4>{prose_html(section['after'])}</section>
          </div>
          <div class="change-strip"><strong>关键变化</strong><ul>{changes}</ul></div>
        </article>
        """)

    before = data["experiment_before"]
    after = data["experiment_after"]
    before_percent = round(before["coverage_ratio"] * 100)
    after_percent = round(after["coverage_ratio"] * 100)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Vibe Research Skill Suite · Before / After</title>
  <style>
    :root {{ --ink:#17212b; --muted:#607083; --line:#dce2e9; --paper:#ffffff; --wash:#f6f8fb; --blue:#4057a6; --blue-soft:#e8edff; --green:#2f7b5a; --green-soft:#e5f4ec; --coral:#ad5946; --coral-soft:#fae8e3; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:#eef2f6; color:var(--ink); font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif; line-height:1.65; }}
    a {{ color:var(--blue); }}
    .page {{ width:min(1440px, calc(100% - 36px)); margin:26px auto 70px; }}
    .hero {{ padding:56px; border:1px solid var(--line); border-radius:28px; background:linear-gradient(135deg,#fff 0%,#f3f5ff 56%,#edf8f2 100%); box-shadow:0 18px 50px rgba(38,48,66,.08); }}
    .eyebrow,.section-kicker {{ color:var(--blue); font-size:12px; font-weight:800; letter-spacing:.14em; text-transform:uppercase; }}
    h1 {{ max-width:980px; margin:12px 0 14px; font-size:clamp(36px,5vw,68px); line-height:1.04; letter-spacing:-.04em; }}
    .hero p {{ max-width:920px; margin:0; color:var(--muted); font-size:19px; }}
    .chips {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:24px; }}
    .chip {{ padding:8px 12px; border:1px solid #cdd5e0; border-radius:999px; background:rgba(255,255,255,.72); font-size:13px; font-weight:700; }}
    .section {{ margin-top:26px; padding:34px; border:1px solid var(--line); border-radius:24px; background:var(--paper); box-shadow:0 12px 34px rgba(38,48,66,.05); }}
    .section-title {{ display:flex; align-items:end; justify-content:space-between; gap:20px; margin-bottom:22px; }}
    .section-title h2 {{ margin:4px 0 0; font-size:30px; letter-spacing:-.025em; }}
    .section-title p {{ max-width:680px; margin:0; color:var(--muted); }}
    .comparison-block + .comparison-block,.writing-block + .writing-block {{ margin-top:32px; padding-top:32px; border-top:1px solid var(--line); }}
    .compare-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-top:12px; }}
    .compare-card,.prose-card {{ margin:0; padding:18px; border:1px solid var(--line); border-radius:18px; overflow:hidden; }}
    .before-card {{ background:#fffaf8; }} .after-card {{ background:#f8fbff; border-color:#cfd8f5; }}
    figcaption {{ display:flex; align-items:center; gap:8px; margin-bottom:12px; font-weight:800; }}
    .state-dot {{ width:9px; height:9px; border-radius:50%; }} .before-dot {{ background:var(--coral); }} .after-dot {{ background:var(--green); }}
    figure img {{ display:block; width:100%; min-height:230px; object-fit:contain; background:#fff; border:1px solid #e6e9ee; border-radius:12px; }}
    figure p {{ min-height:52px; margin:12px 2px 0; color:var(--muted); }}
    .writing-head {{ display:flex; justify-content:space-between; align-items:center; gap:16px; }}
    .writing-head h3 {{ margin:0; font-size:23px; }}
    .audit-pair {{ display:flex; flex-wrap:wrap; gap:8px; }}
    .audit-bad {{ padding:5px 9px; border-radius:999px; font-size:12px; font-weight:800; }}
    .bad {{ color:#8f3e2e; background:var(--coral-soft); }} .good {{ color:#236847; background:var(--green-soft); }}
    .prose-card h4 {{ margin:0 0 10px; }} .prose-card p {{ margin:0 0 12px; }}
    .change-strip {{ margin-top:14px; padding:16px 18px; background:var(--wash); border-radius:14px; }}
    .change-strip ul {{ display:grid; grid-template-columns:1fr 1fr; gap:4px 26px; margin:8px 0 0; padding-left:20px; }}
    .coverage-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; margin:14px 0 22px; }}
    .coverage-card {{ padding:18px; border:1px solid var(--line); border-radius:16px; }}
    .coverage-card h3 {{ margin:0 0 10px; }}
    .coverage-row {{ display:grid; grid-template-columns:1fr auto; align-items:center; gap:12px; }}
    .bar-track {{ height:12px; overflow:hidden; border-radius:999px; background:#e4e8ee; }}
    .bar-fill {{ height:100%; border-radius:999px; }}
    .bar-before {{ width:{before_percent}%; background:var(--coral); }} .bar-after {{ width:{after_percent}%; background:var(--green); }}
    .bar-label {{ min-width:44px; text-align:right; font-weight:900; }}
    .coverage-card p {{ margin:10px 0 0; color:var(--muted); }}
    .table-pair {{ display:grid; grid-template-columns:1fr; gap:18px; }}
    .table-card {{ padding:18px; border:1px solid var(--line); border-radius:16px; }}
    .table-card h3 {{ margin:0 0 12px; }}
    .table-scroll {{ overflow-x:auto; }} table {{ width:100%; border-collapse:collapse; font-size:13px; white-space:nowrap; }}
    th,td {{ padding:10px 12px; border-bottom:1px solid var(--line); text-align:center; }} th:first-child,td:first-child {{ text-align:left; position:sticky; left:0; background:#fff; }} th {{ background:#f4f6fa; }}
    .pattern-grid,.skill-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }}
    .pattern,.skill-card {{ padding:17px; border:1px solid var(--line); border-radius:15px; background:var(--wash); }}
    .pattern h3,.skill-card h3 {{ margin:0 0 6px; font-size:16px; }} .pattern p,.skill-card p {{ margin:0; color:var(--muted); font-size:14px; }}
    .footer {{ margin-top:20px; padding:18px 4px; color:var(--muted); text-align:center; }}
    @media (max-width:900px) {{ .hero{{padding:34px 26px}} .section{{padding:24px 18px}} .compare-grid,.coverage-grid,.pattern-grid,.skill-grid{{grid-template-columns:1fr}} .change-strip ul{{grid-template-columns:1fr}} .section-title,.writing-head{{align-items:flex-start;flex-direction:column}} }}
  </style>
</head>
<body>
  <main class="page">
    <header class="hero">
      <div class="eyebrow">Vibe Research Skill Suite</div>
      <h1>让实验、写作和图表从同一份证据状态生长</h1>
      <p>这个页面使用完全合成的 EvidenceLoop 案例，展示加入四个新 Skills 后，intro 图、方法主图、实验图、摘要、Introduction、方法段和主表如何从“看起来像论文”推进到“每一处都回答明确研究问题”。</p>
      <div class="chips"><span class="chip">4 new skills</span><span class="chip">3 figure comparisons</span><span class="chip">3 writing comparisons</span><span class="chip">25% → 100% table coverage</span><span class="chip">Synthetic showcase</span></div>
    </header>

    <section class="section" id="figures">
      <div class="section-title"><div><div class="eyebrow">01 · Figures</div><h2>画图前后对比</h2></div><p>概念图先确定 visual sentence，实验图再绑定精确数据。After 版本同时提供 source JSON、SVG、PDF 和 PNG。</p></div>
      {compare_figure('Intro / Figure 1', 'output/figures/intro/intro-before.png', 'output/figures/intro/intro-story-example.png', '只有 Data → Agent → Paper，读者看不到现有流程为何失败，也看不到论文的核心 insight。', '用 setting → failure → insight → payoff 建立四拍叙事，并把下一轮 uncertainty 作为反馈关系画出来。')}
      {compare_figure('Method main figure', 'output/figures/method/method-before.png', 'output/figures/method/method-story-example.png', 'Input → EvidenceLoop → Output 把所有关键计算藏在一个框里，方法段无法逐模块对应。', '按 inputs、focal mechanism、persistent state、outputs 展开，并显式展示 manager、executor 和 ledger 的反馈循环。')}
      {compare_figure('Experiment figure', 'output/figures/experiment/experiment-before.png', 'output/figures/experiment/experiment-after.png', '单一 headline 数值缺少不确定性、泛化条件和预算行为，无法解释增益范围。', '三联图分别回答 effectiveness、generality 和 budget behavior；误差、任务切片和方法语义保持一致。')}
    </section>

    <section class="section" id="writing">
      <div class="section-title"><div><div class="eyebrow">02 · Writing</div><h2>写作前后对比</h2></div><p>After 文本由同一合成证据包约束，claim audit 从空泛支持推进到 0 个证据问题。</p></div>
      {''.join(writing_blocks)}
    </section>

    <section class="section" id="experiments">
      <div class="section-title"><div><div class="eyebrow">03 · Experiments</div><h2>主表丰富不是单纯加宽</h2></div><p>每个新增行列对应一个 reviewer question。合成示例从两行单指标，推进到 lower bound、strong baseline、closest method、proposed method，以及 effectiveness、ablation、robustness、efficiency、replication 五类证据。</p></div>
      <div class="coverage-grid">
        <article class="coverage-card before-card"><h3>Before · sparse evidence</h3><div class="coverage-row"><div class="bar-track"><div class="bar-fill bar-before"></div></div><span class="bar-label">{before_percent}%</span></div><p>{before['completed_cell_count']} / {before['required_cell_count']} required cells；缺少 {len(before['missing_method_roles'])} 类 baseline role 和 {len(before['missing_evidence_families'])} 个证据族。</p></article>
        <article class="coverage-card after-card"><h3>After · claim-driven matrix</h3><div class="coverage-row"><div class="bar-track"><div class="bar-fill bar-after"></div></div><span class="bar-label">{after_percent}%</span></div><p>{after['completed_cell_count']} / {after['required_cell_count']} required cells；baseline roles 与五类证据族全部显式登记。</p></article>
      </div>
      <div class="table-pair">
        <article class="table-card before-card"><h3>Before main table</h3>{markdown_table_html(data['table_before'])}</article>
        <article class="table-card after-card"><h3>After main table</h3>{markdown_table_html(data['table_after'])}</article>
      </div>
    </section>

    <section class="section" id="skills">
      <div class="section-title"><div><div class="eyebrow">04 · Skill architecture</div><h2>四个新 Skill + 现有 FigureInk</h2></div><p>总编排只维护研究状态和路由；每个专业 Skill 保留自己的 artifact contract 与 quality gate。</p></div>
      <div class="skill-grid">
        <article class="skill-card"><h3>run-vibe-research</h3><p>研究 spine、claim-evidence ledger、Round 记录、跨模态一致性。</p></article>
        <article class="skill-card"><h3>design-paper-figures</h3><p>intro、method、experiment figure 的视觉叙事与 editable vector 输出。</p></article>
        <article class="skill-card"><h3>write-paper-sections</h3><p>abstract、Introduction、method 的故事主线、引用槽位、原格式修订与 claim audit。</p></article>
        <article class="skill-card"><h3>design-paper-experiments</h3><p>主表覆盖、baselines、metrics、ablations、robustness、efficiency、replication。</p></article>
        <article class="skill-card"><h3>plot-handdrawn-paper-charts</h3><p>精确数据的 bars、curves、uncertainty、SVG/PDF/PNG 与 grayscale QA。</p></article>
      </div>
    </section>

    <section class="section" id="patterns">
      <div class="section-title"><div><div class="eyebrow">05 · GitHub patterns</div><h2>借鉴的工作流模式</h2></div><p>只借鉴可复用的架构思想，不复制项目代码或品牌。</p></div>
      <div class="pattern-grid">
        <article class="pattern"><h3><a href="https://github.com/dwzhu-pku/PaperBanana">PaperBanana</a></h3><p>语义规划、风格设计、可视化与 critic 分离。</p></article>
        <article class="pattern"><h3><a href="https://github.com/SakanaAI/AI-Scientist">AI Scientist</a></h3><p>experiment、plot、prompt、paper template 保持独立 artifact role。</p></article>
        <article class="pattern"><h3><a href="https://github.com/SakanaAI/AI-Scientist-v2">AI Scientist v2</a></h3><p>experiment manager 引导探索，并根据问题选择 template 或 open-ended mode。</p></article>
        <article class="pattern"><h3><a href="https://github.com/allenai/codescientist">CodeScientist</a></h3><p>把 code review 与 replication 纳入 research validation。</p></article>
        <article class="pattern"><h3><a href="https://github.com/HKUDS/AI-Researcher">AI-Researcher</a></h3><p>阶段化 refinement 和 hierarchical writing。</p></article>
        <article class="pattern"><h3><a href="https://github.com/skyllwt/AutoSci">AutoSci</a></h3><p>用 persistent research memory 让每轮结果成为下一轮起点。</p></article>
      </div>
    </section>
    <footer class="footer">All values, methods, tasks, and outcomes in this showcase are synthetic instructional fixtures.</footer>
  </main>
</body>
</html>
"""


def main() -> int:
    args = parse_args()
    data = generate_artifacts()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    rendered_html = build_html(data)
    normalized_html = "\n".join(line.rstrip() for line in rendered_html.splitlines()) + "\n"
    args.output.write_text(normalized_html, encoding="utf-8")
    if "..." in args.output.read_text(encoding="utf-8"):
        raise RuntimeError("the showcase contains a textual ellipsis")
    artifacts = sorted(
        str(path.relative_to(SHOWCASE))
        for path in SHOWCASE.rglob("*")
        if path.is_file() and path.name != "showcase.manifest.json"
    )
    manifest = {
        "status": "verified",
        "data_status": "synthetic instructional showcase",
        "entrypoint": str(args.output.relative_to(SHOWCASE)),
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
    }
    write_json(SHOWCASE / "showcase.manifest.json", manifest)
    print(args.output.resolve())
    print(SHOWCASE / "showcase.manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
