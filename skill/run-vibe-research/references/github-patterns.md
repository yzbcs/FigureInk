# GitHub patterns adopted by this suite

The suite borrows workflow patterns, not project code or branding.

## Reference-driven visual planning

PaperBanana separates retrieval, planning, styling, visualization, and critique. Adopt the separation of semantic planning from styling and a final critic loop. Keep this suite's output deterministic and editable when vector shapes or exact plots are sufficient.

Source: https://github.com/dwzhu-pku/PaperBanana

## Explicit experiment templates

AI Scientist v1 keeps experiment code, plotting code, prompts, seed ideas, and LaTeX templates as distinct artifacts. Adopt explicit file roles and reproducible outputs. Avoid assuming that one universal template fits every domain.

Source: https://github.com/SakanaAI/AI-Scientist

## Exploration guided by an experiment manager

AI Scientist v2 uses progressive agentic tree search guided by an experiment manager and notes that strong templates can outperform open-ended search when objectives are clear. Adopt claim-uncertainty-driven experiment selection and choose templated or exploratory mode from the current state.

Source: https://github.com/SakanaAI/AI-Scientist-v2

## Multi-faceted validation

CodeScientist evaluates research artifacts with paper review, code review, and replication attempts. Adopt evidence gates beyond prose quality: result readback, implementation checks, and replication when the claim warrants it.

Source: https://github.com/allenai/codescientist

## Hierarchical writing and visible refinement

AI-Researcher separates resource collection/filtering, design/implementation/validation/refinement, and hierarchical paper writing. Adopt stage-specific contracts and make refinement depend on observed validation results.

Source: https://github.com/HKUDS/AI-Researcher

## Persistent research memory

AutoSci emphasizes structured memory across the research lifecycle. Adopt a compact research-state file and append-only round ledger so each result becomes the next round's starting point.

Source: https://github.com/skyllwt/AutoSci
