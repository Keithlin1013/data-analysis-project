# Sub Agent: Power BI Project Builder

## Your Single Responsibility

Build **Project 2** of the Stock Market Performance Analysis suite:
**Stock Performance Executive Dashboard** in Power BI Desktop.

You are working in parallel with two other sub agents (Excel and Tableau).
Stay in your lane.

## Your Inputs (READ ONLY)

- `data/cleaned/stocks_cleaned.csv` — daily OHLCV data with returns
- `data/cleaned/summary_stats.csv` — per-ticker summary metrics
- `sql/stock_analysis.sql` — reference for analytical logic

## Your Outputs (CREATE THESE)

1. `powerbi/stock_executive_dashboard.pbix` — the actual Power BI file
2. `powerbi/dashboard_notes.md` — DAX measures, visual specs, build steps

## Hard Rules

- **DO NOT** modify `/data/`, `/python/`, `/sql/`, or `README.md`
- **DO NOT** touch `/excel/` or `/tableau/` folders
- **DO** test in Power BI Desktop — verify visuals render and slicers work
- **DO** take a screenshot → `screenshots/powerbi_dashboard.png`

## Build Specification

The .pbix must have **3 pages**.

### Page 1: Executive Overview

**KPI Cards (top row, 4 cards):**
- Total Return %
- Annualized Volatility
- Sharpe Ratio
- Avg Daily Volume

**Visuals:**
- Line chart: close price over time, all 4 tickers (color-coded legend)
- Scatter plot: x = volatility, y = annualized return, bubble size = avg volume,
  label = ticker
- Slicers: ticker, date range

### Page 2: Matrix (Pivot) Analysis — THE CENTERPIECE

**Matrix Visual 1: Returns Heatmap**
- Rows: ticker
- Columns: year-month (formatted as "YYYY-MM")
- Values: average daily return
- Conditional formatting: red-white-green color scale on values
- Format: percentage, 2 decimals

**Matrix Visual 2: Volume by Quarter**
- Rows: ticker
- Columns: year and quarter (hierarchy, drilldown enabled)
- Values: total volume
- Format: thousands separator

**Slicer:** ticker filter affecting both matrices

### Page 3: Volume & Volatility Deep Dive

- Bar chart: average daily volume by ticker
- Histogram: daily return distribution (use binning)
- Line chart: 30-day rolling volatility per ticker

## Required DAX Measures

Create these explicit measures (NOT calculated columns):

```dax
// Total return: percentage change from first close to last close
Total Return % =
VAR FirstClose = CALCULATE(FIRSTNONBLANK(Stocks[close], 1),
    FILTER(ALL(Stocks), Stocks[date] = MIN(Stocks[date])))
VAR LastClose = CALCULATE(LASTNONBLANK(Stocks[close], 1),
    FILTER(ALL(Stocks), Stocks[date] = MAX(Stocks[date])))
RETURN DIVIDE(LastClose - FirstClose, FirstClose)

// Annualized volatility: daily std × sqrt(252)
Annualized Volatility =
STDEVX.P(Stocks, Stocks[daily_return]) * SQRT(252)

// Annualized return: mean daily return × 252
Annualized Return =
AVERAGE(Stocks[daily_return]) * 252

// Sharpe ratio: (annual return - risk free) / annual vol
Sharpe Ratio =
DIVIDE([Annualized Return] - 0.045, [Annualized Volatility])

// Average daily volume
Avg Daily Volume =
AVERAGE(Stocks[volume])

// Up days count
Up Days =
CALCULATE(COUNTROWS(Stocks), Stocks[daily_return] > 0)

// Down days count
Down Days =
CALCULATE(COUNTROWS(Stocks), Stocks[daily_return] < 0)
```

Each measure must have a **comment** above it explaining what it computes
and why.

## Documentation Requirements

`powerbi/dashboard_notes.md` must contain:

1. **Data import steps** (Get Data → Text/CSV → load `stocks_cleaned.csv`)
2. **Data model** — table relationships if any, calculated columns
3. **All DAX measures** with comments and business meaning
4. **Page-by-page visual specs** — for each visual: type, fields, formatting
5. **Conditional formatting rules** for the matrices
6. **Color theme / visual standards** used

## Acceptance Criteria

- [ ] All 3 pages render without errors
- [ ] Slicers correctly filter all visuals on the page
- [ ] No "blank" or "(blank)" appearing where they shouldn't
- [ ] DAX measures return sensible values (Sharpe between -1 and 3, vol 15–60%)
- [ ] Matrix conditional formatting visible
- [ ] Screenshot saved to `screenshots/powerbi_dashboard.png`
- [ ] `dashboard_notes.md` complete

## Your Final Report

When done, return:

1. ✅ Files created
2. ✅ Tests performed
3. 📊 3-line summary of what the matrix analysis revealed
4. ⚠️ Any assumptions made or blockers

## Pitch Yourself in One Sentence

> "In Power BI, I built a [...] using DAX measures and matrix visuals to [...]"
