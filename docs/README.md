# FigureInk / Vibe Research Skills 对接文档

## 当前状态

- 工作分支：`codex/fix-project`
- 原有能力：`plot-handdrawn-paper-charts` 的结构化数据校验、定量图渲染、PDF/SVG/PNG/灰度输出。
- 本轮新增：总编排、概念图、论文写作、实验设计四个 Skills。
- 可视化入口：`showcase/vibe-research/index.html`
- Showcase 状态：`verified`，共登记 61 个源文件、审计报告与渲染产物。
- 数据边界：所有 before-after 方法、任务、数值和结论均为 synthetic instructional fixtures。

## Skill 架构

| Skill | 核心职责 | 确定性工具 |
|---|---|---|
| `run-vibe-research` | 维护 research spine、claim-evidence ledger、Round 状态和跨模态一致性 | Round ledger 与 research-state 模板 |
| `design-paper-experiments` | 主表 rows/columns、baseline roles、metrics、evidence families | `audit_evidence_matrix.py` |
| `write-paper-sections` | story spine、section contract、引用槽位、原格式修订与 claim audit | `audit_claim_ledger.py` |
| `design-paper-figures` | intro、method、experiment figure 的 visual story | `render_story_figure.py` |
| `plot-handdrawn-paper-charts` | 精确 bars、curves、uncertainty 和出版级导出 | `render_chart.py` |

总编排 Skill 不复制专业 Skill 的细节，只负责当前状态、路由、artifact roles 和完成门槛。概念图与定量图明确分开：概念图使用 editable story spec；精确实验图只读取经过核对的数据。

## 关键文件

### Skills

- `skill/run-vibe-research/SKILL.md`
- `skill/design-paper-experiments/SKILL.md`
- `skill/write-paper-sections/SKILL.md`
- `skill/write-paper-sections/assets/section-brief-template.md`
- `skill/write-paper-sections/references/writing-workflow.md`
- `skill/write-paper-sections/references/prose-quality.md`
- `skill/write-paper-sections/references/citation-workflow.md`
- `skill/design-paper-figures/SKILL.md`
- `skill/plot-handdrawn-paper-charts/SKILL.md`

### 可执行脚本

- `skill/design-paper-figures/scripts/render_story_figure.py`
- `skill/write-paper-sections/scripts/audit_claim_ledger.py`
- `skill/design-paper-experiments/scripts/audit_evidence_matrix.py`
- `showcase/generate_vibe_research_showcase.py`
- `showcase/validate_skill_suite.py`

### 展示与审计

- `showcase/vibe-research/index.html`
- `showcase/vibe-research/showcase.manifest.json`
- `showcase/vibe-research/output/figures/`
- `showcase/vibe-research/output/writing/`
- `showcase/vibe-research/output/experiments/`

## 本轮可复现实验

```bash
python3 showcase/validate_skill_suite.py

SKILL_VALIDATOR="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py"

python3 "$SKILL_VALIDATOR" \
  skill/design-paper-figures

python3 "$SKILL_VALIDATOR" \
  skill/write-paper-sections

python3 "$SKILL_VALIDATOR" \
  skill/design-paper-experiments

python3 "$SKILL_VALIDATOR" \
  skill/run-vibe-research

python3 showcase/generate_vibe_research_showcase.py
```

## Before / After 结果

### 图

| Figure role | Before | After |
|---|---|---|
| Intro / Figure 1 | `Data → Agent → Paper`，没有可见 gap | `setting → failure → insight → payoff`，含下一轮 uncertainty 反馈 |
| Method main figure | `Input → Method → Output`，隐藏真实计算 | inputs、experiment manager、executor、claim-evidence ledger、paper-facing outputs |
| Experiment figure | 单一 quality headline | effectiveness、generality、budget behavior 三联图，含 uncertainty 与 task slice |

每个概念图 After 版本均有 source JSON、SVG、PDF、PNG 和 manifest；实验图额外包含灰度 QA。

### 写作

| Section | Before audit | After audit | 主要变化 |
|---|---:|---:|---|
| Abstract | 2 个 evidence issues | 0 | 背景 1 句、动机 2 句、递进方法 4 句、性能与边界 2 句 |
| Introduction | 2 个 evidence issues | 0 | 5 段式 taxonomy、独立 limitations、gap-to-module 映射与三项 contributions |
| Method | 1 个 evidence issue | 0 | 按执行顺序说明输入、状态、选择、执行和输出 |

### 实验与主表

- Before：2 / 8 required cells，coverage 为 25%；缺少 `lower_bound` 与 `closest_method`；五类 evidence family 均未完成。
- After：16 / 16 required cells，coverage 为 100%；四类 baseline/method roles 和 effectiveness、ablation、robustness、efficiency、replication 全部登记。
- 表格中的 best 与 second-best 标记由审计脚本从显示值重新计算。

## GitHub 项目调研与借鉴

| 项目 | 借鉴点 | 本项目中的落实 |
|---|---|---|
| [PaperBanana](https://github.com/dwzhu-pku/PaperBanana) | Retriever、Planner、Stylist、Visualizer、Critic 分工 | 先做 semantic story，再做 style 和 critique；能用向量形状时保持 editable |
| [AI Scientist](https://github.com/SakanaAI/AI-Scientist) | experiment、plot、prompt、paper template 分离 | 明确 artifact roles，并让脚本读取稳定 JSON 输入 |
| [AI Scientist v2](https://github.com/SakanaAI/AI-Scientist-v2) | experiment manager 与 progressive search | 按 claim uncertainty 选择下一轮；明确 template 与 open-ended mode 的选择 |
| [CodeScientist](https://github.com/allenai/codescientist) | paper review 之外加入 code review 与 replication | 完成门槛包含脚本执行、结果 readback 和 replication evidence family |
| [AI-Researcher](https://github.com/HKUDS/AI-Researcher) | 分阶段 refinement 与 hierarchical writing | 为 abstract、Introduction、method 使用不同 section contracts |
| [AutoSci](https://github.com/skyllwt/AutoSci) | persistent research memory | research-state 与 append-only Round ledger 成为下一轮输入 |

## 实验推进历程

### Round 1 — 审计现有 FigureInk 边界

#### 设计动机

先确认仓库现有能力，避免把定量图渲染器误当成完整 research workflow，也避免重写已经稳定的 chart renderer。

#### 具体方案与关键参数

- 检查当前分支、Skill tree、README、showcase 和 CI。
- 运行现有 `quick_validate.py` 入口。
- 把 FigureInk 保留为定量图后端，新能力采用独立 Skills。

#### 结果数据

- 初始 Skill 数：1。
- 初始 figure coverage：bars、lines、multi-panel quantitative charts。
- 初始 writing/experiment orchestration：0 个对应 Skills。

#### 核心发现或失败原因

现有 FigureInk 的数据忠实性、palette roles 和多格式导出可以直接复用，但 intro 图、方法主图、section writing 和 main-table planning 需要不同的 artifact contract。

#### 推导出的下一步洞察

采用“总编排 + 三个专业 Skill + 原有定量图 Skill”的五层结构，而不是把所有说明塞进一个巨大 SKILL.md。

### Round 2 — 借鉴相关 GitHub 工作流并确定架构

#### 设计动机

避免把 vibe research 简化为一键写论文，重点吸收当前项目在 visual planning、experiment management、artifact separation 和 persistent memory 上的成熟模式。

#### 具体方案与关键参数

- 调研 PaperBanana、AI Scientist v1/v2、CodeScientist、AI-Researcher 和 AutoSci。
- 保留本项目的 agent-portable 结构：Markdown + JSON + Python。
- 不引入重型 UI 或特定模型 API 依赖。

#### 结果数据

- 形成 6 组可落实设计模式。
- 新建 4 个 Skill skeletons，并为每个生成 `agents/openai.yaml`。

#### 核心发现或失败原因

相关项目共同强调分阶段 workflow，但开放式 agent search 不一定优于强模板。对明确的 paper-writing 和 figure tasks，应采用 section/figure-specific templates；对实验探索才使用 uncertainty-driven iteration。

#### 推导出的下一步洞察

总编排 Skill 只选择下一步和保持状态，具体生成与审计交给低自由度脚本和专用 references。

### Round 3 — 实现三类专业能力

#### 设计动机

让 Skills 不只是提示词说明，而是具备可执行、可审计和可复现的 artifact pipeline。

#### 具体方案与关键参数

- `render_story_figure.py`：normalized geometry、2 套 semantic palettes、4 类 edge semantics、source JSON + SVG + PDF + PNG + manifest。
- `audit_claim_ledger.py`：claim-evidence references、headline direct-measured gate、numeric anchors、terminology checks。
- `audit_evidence_matrix.py`：required cells、method roles、evidence families、best/second-best ranking 和 Markdown table。
- 所有新 Skill frontmatter 仅包含 `name` 与 `description`。

#### 结果数据

- 4 个新 Skills 通过系统 `quick_validate.py`。
- 3 个新脚本通过 `py_compile`。
- bundled intro、method、writing、experiment fixtures 均通过 strict audit。

#### 核心发现或失败原因

首轮 experiment chart fixture 使用了 renderer 未支持的 `.1f` 名称，校验阶段立即失败。根据现有 schema 改为 `one_decimal` 后，整套生成成功。

#### 推导出的下一步洞察

所有示例必须走实际 parser 和 renderer，不能只靠目视检查 JSON；CI 也应执行同一 showcase generator。

### Round 4 — 生成并视觉检查 Before / After Showcase

#### 设计动机

用户不仅需要 Skill 文件，还需要直观看到加入 Skills 后图、文、实验发生了什么变化。

#### 具体方案与关键参数

- 使用一个完全合成的 EvidenceLoop 案例贯穿三种模态。
- 生成 3 组 figure comparisons、3 组 writing comparisons 和 2 份 experiment matrices。
- HTML 直接覆盖 `showcase/vibe-research/index.html`。
- HTML coverage bar 的数值标签作为 bar-fill 的兄弟元素放在柱外。

#### 结果数据

- Showcase manifest：61 个 artifacts，状态 `verified`。
- Writing audits：Before 为 2、2、1 个 issues；After 均为 0。
- Main-table coverage：25% → 100%。
- 图像视觉检查发现并修正了 feedback label 与方法边缘标签重叠。

#### 核心发现或失败原因

同一案例能清晰展示三个 Skill 之间的依赖：没有 experiment matrix，写作 claim audit 和实验图的 scope 都不稳定；没有 claim ledger，intro 与 method 图容易退化成通用流程图。

#### 推导出的下一步洞察

下一阶段应使用一个真实论文 workspace 做 forward test，重点检查真实 LaTeX terminology、现有表格 schema 和用户当前 figure sources 能否无损接入。

### Round 5 — 全量验证、打包与回滚演练

#### 设计动机

证明新增内容不只是文档草案，而是能够在干净 baseline 上应用、执行、生成展示并完整回滚的项目改动。

#### 具体方案与关键参数

- 使用 `showcase/validate_skill_suite.py` 检查五个 Skill folders、frontmatter 和 `agents/openai.yaml`。
- 使用系统 `quick_validate.py` 分别检查五个 Skills。
- 编译三个新脚本、现有 FigureInk renderer、showcase generator 和 suite validator。
- 重新生成 61 个 showcase artifacts，并检查 README fences、local links、manifest 与 no-ellipsis rule。
- 生成 binary-capable patch，在 baseline 临时目录中执行 apply、suite validation 和 reverse rollback。

#### 结果数据

- Skill validation：5 / 5 通过。
- Bundled strict audits：writing fixture 0 issues；experiment fixture 16 / 16 required cells。
- Showcase：61 artifacts，状态 `verified`。
- Cached diff check：通过。
- Patch apply：通过。
- Rollback readback：只剩原始 `plot-handdrawn-paper-charts` Skill，新增 docs 和 showcase 均已移除。

#### 核心发现或失败原因

第一版 verification script 的 `awk` 正则在 shell 转义后失效，改用 Python `tarfile` 读取 baseline inventory 后，完整验证记录通过。新生成 SVG 被声明为 binary artifact，避免将向量路径内部的格式空格误判为源码 whitespace issue；所有普通文本仍执行严格 cached diff 检查。

#### 推导出的下一步洞察

当前 suite 已具备可移植安装、可执行 fixture、可视化证据和回滚路径。后续重点从“仓库结构是否成立”转向“真实论文案例中是否保持 source、terminology 和 measured evidence 不变”。

### Round 6 — 细化 Abstract 与 Introduction 模板

#### 设计动机

原始 `write-paper-sections` 只给出通用 rhetorical moves，尚未固定摘要句数分配、三项贡献递进关系、引言方法分类、独立 limitation 段和一一对应关系。过于宽泛的模板容易让模型把模块并列罗列，或者在引言最后才突兀地综合出 gap。

#### 具体方案与关键参数

- Abstract 默认采用 7–10 句：背景 1 句、动机 1–2 句、正式方法 4–5 句、性能 1–2 句。
- 正式方法部分使用 `In this paper`、`Specifically`、`To further`、`Moreover` 建立依赖关系；每项贡献必须回指一个 gap。
- Introduction 提供 5 段默认版和 4 段压缩版。默认版依次为主题与 Figure 1、两类 prior work、补充类别与综合、独立 limitations、方法回应与 contributions。
- 新增 `prior family → solved problem → limitation → required capability → module → evidence` 表，先填表再写段落。
- Method 模板保持不变，等待下一轮单独指令。

#### 结果数据

- 新增 2 份可直接复制的 Markdown 模板。
- Abstract 参考文档扩展为 116 行；Introduction 参考文档扩展为 123 行。
- 合成 Abstract 更新为 9 句，分配为 `1 + 2 + 4 + 2`。
- 合成 Introduction 更新为 5 个正文段落和 3 条 contributions。
- 三个 gap 分别对应 comparison selector、artifact readback 和 downstream synchronizer。
- `write-paper-sections` strict claim audit 为 0 issues，5 / 5 Skills 均通过校验。
- Showcase 重新生成 61 个 artifacts，状态为 `verified`，cached diff check 通过。

#### 核心发现或失败原因

- 方法谱系型写法适合从已有路线推导互补模块，mismatch-to-intervention 写法适合领域迁移问题。
- 当论文已经有测量过的残余瓶颈时，诊断链通常比强行套用 prior-work taxonomy 更有说服力。
- `Moreover` 本身不产生递进关系。只有第三项设计明确补充、控制、扩展或落地前两项时，它才不是并列罗列。

#### 推导出的下一步洞察

后续修改 Method 时，应复用同一张 gap-to-contribution map，让方法小节顺序与摘要贡献、引言 limitations 保持一致；真实论文 forward test 则需要补入真实 citation groups、Figure 1 panel 指向和权威结果来源。

### Round 7 — 补全写作模式、故事主线与引用工作流

#### 设计动机

结构模板能够约束 Abstract 和 Introduction 的段落形状，但仅靠句型仍可能产生机械化表达。完整写作流程还需要区分“从零起草、结构修订、局部润色、压缩、诊断”，并在写作前固定源格式、整篇故事、证据边界和引用需求。

#### 具体方案与关键参数

- 增加 `draft / revise / polish / compress / diagnose` 五种模式，明确每种模式允许改动与必须保留的内容。
- 建立 `task → gap → root reason → insight → mechanism → evidence → bounded claim` 故事主线。
- 写作前使用 section brief 固定输出格式、不可变内容、paragraph roles、claim evidence 和 citation slots。
- 引用采用 `identify claim → verify source → obtain bibliography entry → insert → read back` 流程，不用固定引用数量代替覆盖质量。
- 修订分为 story logic、evidence and citations、prose quality 三轮，避免润色掩盖论证或证据问题。
- 可见输出默认先给用户请求的论文文本，内部计划和检查表只在用户要求诊断时展示。

#### 结果数据

- 新增 3 份按需加载的 references：writing workflow、prose quality、citation workflow。
- 新增 1 份可复制的 section brief，覆盖 6 类输出约束、7 个 story links、paragraph roles、claim evidence 和 citation slots。
- 合成 section packet 新增 8 个 writing-brief 字段，同时保持 strict claim audit 兼容。
- Skill 元数据同步更新为“保留格式、证据、引用与科学故事”的默认修订入口。
- `write-paper-sections` 与 5 / 5 suite Skills 均通过校验，strict claim audit 为 0 issues。
- Showcase 重新生成 61 个 artifacts，状态为 `verified`；文档结构与链接检查通过。

#### 核心发现或失败原因

- 句型模板只能保证表面结构；只有先固定 root reason 和 evidence boundary，方法才会从问题自然推导出来。
- 引用质量取决于“每个外部主张是否有准确来源”，而不是机械追求一个固定总数。
- source-preserving 模式必须把格式与科学含义分开控制：允许改善逻辑和语言，但不能顺手改动标签、引用键、公式、数值或主张强度。

#### 推导出的下一步洞察

下一轮 Method 模板应在用户给出详细要求后补充，并直接复用本轮确定的 story spine、component role、equation narration 和 cross-section readback，而不是先扩大方法内容范围。

## 后续可推进方向

1. 选取一个真实实验目录，用 `run-vibe-research` 建立第一份 project-local research-state。
2. 将现有主表导入 experiment matrix，先只审计，不自动新增实验结果。
3. 对真实 Abstract、Introduction 和 Method 做 source-preserving before-after。
4. 将真实 Figure 1 和方法图转换为 story spec，并保留论文中的 active asset path。
5. 在真实 forward test 稳定后再发布 tagged release。
