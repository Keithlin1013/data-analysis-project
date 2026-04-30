# CLAUDE.md

## Project Suite
**Stock Market Performance Analysis** — a 3-project portfolio suite for Data
Analyst job applications. Same dataset, same business questions, three
different tools to demonstrate breadth.

## Strategy: Why Three Projects?

Most job candidates show one project per tool. By analyzing the **same dataset**
in **three different tools**, this portfolio demonstrates:

1. **Tool-agnostic thinking** — the analyst chooses the right tool for the job
2. **Direct skill comparison** — recruiters can see the same insight executed
   three ways
3. **Coverage of all common job requirements** — Excel, Power BI, and Tableau
   are listed in ~90% of NYC Data Analyst job postings

## The Three Projects

| # | Project Name | Tool | Positioning | Key Feature |
|---|---|---|---|---|
| 1 | Stock Analyst's Workbook | Excel | Hands-on exploratory analysis | **PivotTables, PivotCharts, Slicers** |
| 2 | Stock Performance Executive Dashboard | Power BI | Enterprise KPI monitoring | **Matrix visuals, DAX measures, drill-through** |
| 3 | Stock Market Storytelling Report | Tableau | Narrative-driven insights | **Story points, calculated fields, cross-tabs** |

All three projects answer the same business questions:
- Stock price trends
- Daily and average returns
- Volatility / risk
- Trading volume patterns
- Risk vs. return comparison
- Investment recommendations

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Data ingestion | Python (yfinance) | Pull historical OHLCV data |
| Cleaning & analysis | Python (pandas, numpy) | Transform raw data, compute metrics |
| Analytical queries | SQL (SQLite) | Window functions, aggregations |
| Project 1 | Microsoft Excel | PivotTables, PivotCharts, Slicers, formulas |
| Project 2 | Power BI Desktop | DAX, matrix visuals, dashboards |
| Project 3 | Tableau Public | Story points, calculated fields, dashboards |
| Documentation | Markdown (GitHub README) | Portfolio presentation |

## Critical Rule: Test Before Delivery

After writing or modifying ANY code, run it and verify the output before
considering the task complete.

Before responding with "done," verify ALL of the following:

1. The Python script runs without errors
2. The SQL queries execute and return non-empty results
3. Output files are created in the expected paths
4. The dataset loads correctly and row counts match expectations
5. File paths in code are RELATIVE (not hardcoded absolute paths)
6. The README accurately describes what was built (no aspirational claims)
7. The final project structure matches the layout in this file

For Excel/Power BI/Tableau files, since they're built manually in the GUI:
the corresponding `_notes.md` file must contain detailed enough build
instructions that another analyst could rebuild the file from scratch.

If there is an error, fix it first, then re-run. Never deliver untested code.

## Data Source Handling

Primary source: Yahoo Finance via `yfinance` (free, no API key).

Fallback: If `yfinance` is unreachable, `download_data.py` falls back to a
synthetic Geometric Brownian Motion generator with realistic per-ticker drift
and volatility. The README must clearly state which source was used.

## Coding Standards

- **Python:** PEP 8, type hints where helpful, docstrings on functions
- **SQL:** Uppercase keywords, one clause per line, comments above each query
- **Excel formulas:** Use named ranges, document any complex formulas in notes
- **DAX measures:** Comment what each measure computes and why
- **File paths:** Always relative to project root
- **Reproducibility:** Set random seeds in synthetic data generation

## Expected Project Structure

```
stock-market-analysis/
├── data/
│   ├── raw/
│   │   └── stocks_raw.csv
│   └── cleaned/
│       ├── stocks_cleaned.csv
│       └── summary_stats.csv
├── python/
│   ├── download_data.py
│   ├── clean_data.py
│   └── analysis.py
├── sql/
│   └── stock_analysis.sql
├── excel/
│   ├── stock_analyst_workbook.xlsx
│   └── workbook_notes.md
├── powerbi/
│   ├── stock_executive_dashboard.pbix
│   └── dashboard_notes.md
├── tableau/
│   ├── stock_market_story.twbx
│   └── tableau_story_notes.md
├── screenshots/
│   ├── excel_pivot_view.png
│   ├── powerbi_dashboard.png
│   └── tableau_story.png
├── README.md
├── requirements.txt
├── CLAUDE.md
└── todo.md
```

## Definition of Done (Whole Suite)

The portfolio is complete when:

- [ ] All three project files (`.xlsx`, `.pbix`, `.twbx`) exist and open without errors
- [ ] Each project answers all 6 business questions listed above
- [ ] Each project includes at least one pivot/matrix/cross-tab analysis
- [ ] Screenshots of all three dashboards are in `/screenshots`
- [ ] README has separate sections for each of the three projects
- [ ] All three are linkable from the resume as one portfolio
- [ ] You can verbally explain why you chose each tool for its role
