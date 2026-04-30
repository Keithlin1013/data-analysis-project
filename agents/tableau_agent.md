# Sub Agent: Tableau Project Builder

## Your Single Responsibility

Build **Project 3** of the Stock Market Performance Analysis suite:
**Stock Market Storytelling Report** in Tableau Public.

You are working in parallel with two other sub agents (Excel and Power BI).
Stay in your lane.

## Your Inputs (READ ONLY)

- `data/cleaned/stocks_cleaned.csv` — daily OHLCV data with returns
- `data/cleaned/summary_stats.csv` — per-ticker summary metrics

## Your Outputs (CREATE THESE)

1. `tableau/stock_market_story.twbx` — packaged Tableau workbook
2. `tableau/tableau_story_notes.md` — calculated fields, sheet specs, story flow

## Hard Rules

- **DO NOT** modify `/data/`, `/python/`, `/sql/`, or `README.md`
- **DO NOT** touch `/excel/` or `/powerbi/` folders
- **DO** test the story — click through all 4 points, verify visuals
- **DO** take a screenshot → `screenshots/tableau_story.png`

## Build Specification

### Data Source

Connect to BOTH:
- `stocks_cleaned.csv` (primary, daily granularity)
- `summary_stats.csv` (secondary, ticker-level summary)

Relate them on `ticker`.

### Worksheets to Build

#### WS1: Price Trend Lines
- Columns: date (continuous month)
- Rows: close
- Color: ticker
- Filter: ticker (multi-select)

#### WS2: Returns Cross-Tab (THE CENTERPIECE)
- Columns: year + month (date hierarchy)
- Rows: ticker
- Text: avg daily return
- Color: avg daily return (red-white-green diverging)
- Format: percentage, 2 decimals

#### WS3: Risk vs. Return Scatter
- Columns: Annualized Volatility (calculated)
- Rows: Annualized Return (calculated)
- Marks: Circle, sized by Avg Volume, labeled by ticker
- Reference line: average return across all stocks

#### WS4: Volume Analysis
- Columns: ticker
- Rows: AVG(volume)
- Sort descending

#### WS5: Daily Return Distribution
- Columns: bin of daily_return (histogram with 1% bins)
- Rows: count of records
- Color: ticker

### Required Calculated Fields

```
// Annualized Return
[Annualized Return] = AVG([log_return]) * 252

// Annualized Volatility
[Annualized Volatility] = STDEV([log_return]) * SQRT(252)

// Sharpe Ratio (using 4.5% risk-free rate)
[Sharpe Ratio] = ([Annualized Return] - 0.045) / [Annualized Volatility]

// Up Day Flag (for counting positive return days)
[Up Day] = IF [daily_return] > 0 THEN 1 ELSE 0 END

// Year-Month label for cross-tab
[Year-Month] = DATETRUNC('month', [date])
```

### Dashboards (Combine Worksheets)

**Dashboard 1: Market Overview**
- WS1 (price trends, top)
- WS4 (volume, bottom-left)
- WS5 (return distribution, bottom-right)

**Dashboard 2: Risk-Return Analysis**
- WS2 (cross-tab, top — full width)
- WS3 (scatter, bottom)

### Story (4 Points) — REQUIRED

This is what makes it a STORYTELLING dashboard. Each story point gets a
caption that frames the insight.

**Story Point 1 — "Three Years, Four Companies, One Market"**
- Show: Dashboard 1 (Market Overview)
- Caption: "From 2022 to 2024, four tech-heavy stocks moved through wildly
  different paths — but every path was shaped by the same macro forces."

**Story Point 2 — "Returns Tell Half the Story"**
- Show: WS2 (cross-tab) zoomed in
- Caption: "Average returns hide month-to-month volatility. The cross-tab
  reveals how often each stock turned green — and how often it didn't."

**Story Point 3 — "Risk Is What You Pay for Performance"**
- Show: Dashboard 2 (Risk-Return Analysis) with WS3 highlighted
- Caption: "[NVDA's] return is impressive — but adjusted for volatility,
  the picture changes. Sharpe ratios separate winners from gamblers."
  (Update with actual ticker after you compute Sharpe.)

**Story Point 4 — "Where the Smart Money Should Go"**
- Show: a custom layout with KPI text + WS3
- Caption: Based on actual computed Sharpe ratios, name the
  best risk-adjusted performer and the recommendation for a balanced investor.

## Documentation Requirements

`tableau/tableau_story_notes.md` must contain:

1. **Data source setup** (file paths, join logic between the two CSVs)
2. **All calculated fields** with formulas and business meaning
3. **Worksheet-by-worksheet build steps** (what goes on rows/columns/marks)
4. **Dashboard layout** specs
5. **Story captions** (final wording, with actual numbers filled in)
6. **Color palette** chosen and why

## Acceptance Criteria

- [ ] `.twbx` opens without errors and is fully packaged (data embedded)
- [ ] All 5 worksheets render correctly
- [ ] Both dashboards lay out cleanly (no overlapping visuals)
- [ ] Story has 4 points, each with a caption
- [ ] Cross-tab is readable (text + color combination works)
- [ ] Calculated fields use `log_return` (not `daily_return`) for vol/Sharpe
- [ ] Screenshot saved to `screenshots/tableau_story.png`
- [ ] `tableau_story_notes.md` complete

## Your Final Report

1. ✅ Files created
2. ✅ Tests performed
3. 📊 3-line summary of the story's main insight
4. ⚠️ Assumptions or blockers

## Pitch Yourself in One Sentence

> "In Tableau, I built a 4-step story that walks the viewer from [...] to [...]
> using calculated fields for Sharpe ratio and a cross-tab heatmap of monthly
> returns."
