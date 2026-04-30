# Sub Agent: Excel Project Builder

## Your Single Responsibility

Build **Project 1** of the Stock Market Performance Analysis suite:
**Stock Analyst's Workbook** in Microsoft Excel.

You are working in parallel with two other sub agents (Power BI and Tableau).
Stay in your lane.

## Your Inputs (READ ONLY — do not modify)

- `data/cleaned/stocks_cleaned.csv` — daily OHLCV data with returns
- `data/cleaned/summary_stats.csv` — per-ticker summary metrics
- `sql/stock_analysis.sql` — reference for analytical logic (optional)

## Your Outputs (CREATE THESE)

1. `excel/stock_analyst_workbook.xlsx` — the actual Excel workbook
2. `excel/workbook_notes.md` — detailed build instructions

## Hard Rules

- **DO NOT** modify anything in `/data/`, `/python/`, `/sql/`, or `README.md`
- **DO NOT** touch `/powerbi/` or `/tableau/` folders (other agents own those)
- **DO** test your work — open the file, verify pivots and slicers function
- **DO** take a screenshot → `screenshots/excel_pivot_view.png`

## Build Specification

The workbook must contain these 6 sheets:

### Sheet 1: Cover
- Project title, your name placeholder, date
- Brief description of business questions
- Hyperlinks to other sheets for navigation

### Sheet 2: Raw Data
- Import `stocks_cleaned.csv` as an Excel Table
- Name the table `tbl_Stocks`
- Apply table style for readability

### Sheet 3: KPI Summary
Formula-driven (NOT hardcoded). Use `tbl_Stocks` references:

| KPI | Formula approach |
|---|---|
| Total Return % | (last close / first close) - 1, per ticker |
| Annualized Volatility | STDEV(daily_return) * SQRT(252) |
| Annualized Return | AVERAGE(daily_return) * 252 |
| Sharpe Ratio | (Ann Return - 0.045) / Ann Volatility |
| Avg Daily Volume | AVERAGE(volume) |

Use AVERAGEIFS / STDEV.S with ticker filter, or set up one row per ticker.

### Sheet 4: PivotTable Analysis (THE CENTERPIECE)

Build **three pivot tables** with these specs:

**Pivot 1 — Returns by Ticker × Year**
- Rows: ticker
- Columns: year
- Values: AVERAGE of daily_return
- Number format: percentage, 2 decimals
- Conditional formatting: red-white-green color scale

**Pivot 2 — Volume by Month × Ticker**
- Rows: month (extracted from date)
- Columns: ticker
- Values: SUM of volume
- Number format: thousands separator, no decimals

**Pivot 3 — Up Days vs. Down Days**
- Rows: ticker
- Values: count of days where daily_return > 0, count where < 0
- Show as percentage of total

**Slicers (REQUIRED):**
- Ticker slicer (connected to all 3 pivots)
- Year slicer (connected to Pivot 1 and Pivot 2)

**Pivot Chart:** at least one PivotChart linked to Pivot 1 (clustered column).

### Sheet 5: Charts
- Line chart: close price over time, all 4 tickers
- Scatter plot: x = annualized volatility, y = annualized return, label = ticker
- Bar chart: average daily volume by ticker

### Sheet 6: Insights
Written analyst commentary (3–5 bullets):
- What the pivots reveal
- Which stock is best risk-adjusted performer
- Volume patterns observed
- Recommendation for a hypothetical investor

## Documentation Requirements

`excel/workbook_notes.md` must contain:

1. **Sheet-by-sheet build steps** (clear enough that another analyst could
   rebuild from scratch)
2. **All formulas used** in Sheet 3 (KPI Summary)
3. **Pivot table field configuration** (rows, columns, values, filters)
4. **Slicer setup instructions** (Insert → Slicer → connections)
5. **Conditional formatting rules** applied
6. **Number formatting standards** used

## Acceptance Criteria

Before reporting "done," verify:

- [ ] All 6 sheets exist and are named correctly
- [ ] PivotTables update when slicers are clicked
- [ ] No `#REF!`, `#DIV/0!`, or `#NAME?` errors anywhere
- [ ] Cover sheet hyperlinks work
- [ ] Screenshot saved to `screenshots/excel_pivot_view.png`
- [ ] `workbook_notes.md` is detailed enough to reproduce the workbook

## Your Final Report

When done, return:

1. ✅ Files created (list paths)
2. ✅ Tests performed
3. 📊 3-line summary of what the pivots revealed
4. ⚠️ Any assumptions made or blockers encountered

## Pitch Yourself in One Sentence

When done, write one sentence I can use in interviews:
> "In Excel, I built a [...] that [...]"
