# Sub Agent Setup

This folder contains prompts for orchestrated multi-agent execution of the
Stock Market Performance Analysis project.

## Files

| File | Purpose |
|---|---|
| `main_orchestrator.md` | Lead agent prompt — manages everything, delegates Phases 6–8 |
| `excel_agent.md` | Sub agent for Project 1 (Excel workbook with PivotTables) |
| `powerbi_agent.md` | Sub agent for Project 2 (Power BI executive dashboard) |
| `tableau_agent.md` | Sub agent for Project 3 (Tableau storytelling report) |

## Execution Flow

```
1. Start a session with main_orchestrator.md
   ↓
2. Orchestrator does Phase 1–5 itself
   (data download, cleaning, SQL, Python analysis)
   ↓
3. After cleaned data exists, orchestrator spawns 3 sub agents in parallel:
   ├── Excel Agent      (uses excel_agent.md)
   ├── Power BI Agent   (uses powerbi_agent.md)
   └── Tableau Agent    (uses tableau_agent.md)
   ↓
4. Sub agents return their outputs and reports
   ↓
5. Orchestrator does Phase 9–11 itself
   (README, interview prep, publish)
```

## Why This Structure Saves Time

- **Phases 1–5 are sequential** — each step depends on the previous output.
  Trying to parallelize would just cause conflicts.
- **Phases 6–8 are independent** — each consumes the same input
  (`stocks_cleaned.csv`) and produces its own isolated output. Perfect for
  parallel execution.
- **Phase 9 reconciles** — only the orchestrator can write the unified README
  because it needs to reference what all three sub-projects produced.

## Coordination Rules

- Sub agents have READ-ONLY access to `/data/`, `/python/`, `/sql/`
- Each sub agent owns exactly one folder: `/excel/`, `/powerbi/`, or `/tableau/`
- Sub agents do NOT modify `README.md` — that's the orchestrator's job
- Sub agents must report back with: files created, tests run, key insights,
  and a one-sentence "interview pitch" line

## How to Use

In your Claude Code or chat session:

1. Paste `main_orchestrator.md` as your first message
2. Make sure all three sub agent prompt files are in the project so the
   orchestrator can reference them
3. Let it run — review at each phase boundary
