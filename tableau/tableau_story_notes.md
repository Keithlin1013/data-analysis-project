# Tableau Story Build Notes
## Stock Market Storytelling Report — `stock_market_story.twbx`

> **Limitation:** `.twbx` files cannot be generated programmatically.
> These instructions rebuild the complete 4-point story from scratch in
> Tableau Public (free) or Tableau Desktop in approximately 60–90 minutes.
> Tableau Public download: https://public.tableau.com/en-us/s/download

---

## Prerequisites

- Tableau Public (free) or Tableau Desktop
- `data/cleaned/stocks_cleaned.csv`
- `data/cleaned/summary_stats.csv`

---

## Step 1: Data Source Setup

1. Open Tableau → **Connect → Text File** → select `stocks_cleaned.csv`
2. In the Data Source tab, verify column types:

| Column | Tableau type |
|---|---|
| `date` | Date |
| `ticker` | String (Dimension) |
| `open`, `high`, `low`, `close` | Number (Decimal) |
| `volume` | Number (Whole) |
| `daily_return`, `log_return` | Number (Decimal) |
| `year`, `month`, `quarter` | Number (Whole) — drag to Dimensions |
| `day_of_week` | String (Dimension) |

3. Add a second data source: **Data → New Data Source → Text File** → `summary_stats.csv`
4. In the Data Source tab, click **Relationships** → drag `summary_stats[ticker]` to connect
   to `stocks_cleaned[ticker]` on a relationship (not a join — keep them as separate logical tables)

---

## Step 2: Calculated Fields

Create each calculated field: **Analysis → Create Calculated Field** (or right-click
in the Data pane → Create Calculated Field).

```
// Annualized Return
// Business use: scale daily log_return to annual for Sharpe and scatter plot
[Annualized Return]
= AVG([log_return]) * 252


// Annualized Volatility
// Business use: standard deviation of log returns, annualized
[Annualized Volatility]
= STDEV([log_return]) * SQRT(252)


// Sharpe Ratio
// Business use: risk-adjusted return, using 4.5% risk-free rate (2022-2024 avg Treasury)
[Sharpe Ratio]
= ([Annualized Return] - 0.045) / [Annualized Volatility]


// Up Day Flag
// Business use: count positive return days for Pivot 3 equivalent
[Up Day]
= IF [daily_return] > 0 THEN 1 ELSE 0 END


// Year-Month (for cross-tab column header)
// Business use: group dates to monthly granularity for the returns heatmap
[Year-Month]
= DATETRUNC('month', [date])
```

**Verify calculated fields:**
- Click each field → should show green checkmark (no syntax errors)
- `[Annualized Return]` should preview a value near 0.25–0.34 for MSFT/NVDA when filtered

---

## Step 3: Build Worksheets

### WS1: Price Trend Lines

1. New worksheet → rename to `Price Trends`
2. **Columns:** `[date]` (drag to Columns → right-click → **Exact Date** → set to **Continuous**)
3. **Rows:** `SUM([close])` → change aggregation to `AVG` (right-click → Measure → Average)
4. **Color mark:** drag `[ticker]` to Color
5. **Marks card:** set to **Line**
6. Assign custom colours: right-click the colour legend → **Edit Colors**
   - AAPL: `#808080`
   - MSFT: `#00A4EF`
   - NVDA: `#76B900`
   - TSLA: `#CC0000`
7. **Filter:** drag `[ticker]` to Filters → Show Filter → set filter style to **Multiple Values (list)**
8. Title: "Closing Price by Ticker (2022–2024)"
9. Format Y axis: right-click → Format → Numbers → Currency (Custom) → `$#,##0.00`

---

### WS2: Returns Cross-Tab — THE CENTERPIECE

1. New worksheet → rename to `Monthly Returns Cross-Tab`
2. **Columns:** `[Year-Month]` (the calculated field) → set to **Discrete** → **Exact Date**
3. **Rows:** `[ticker]`
4. **Marks → Text:** `AVG([daily_return])`
5. **Marks → Color:** `AVG([daily_return])`
6. Change **Mark type** to **Square** (makes it a heatmap / cross-tab)
7. Format the colour: click **Color → Edit Colors**
   - Palette: **Custom Diverging**
   - Start: `#9C0006` (dark red)
   - Center: `#FFFFFF` (white) at 0
   - End: `#375623` (dark green)
   - Check **Use Full Color Range** and **Stepped Color** (9 steps)
8. Format the text mark:
   - Right-click AVG([daily_return]) on Marks → Format
   - Numbers → Percentage, 2 decimal places
9. Format columns: right-click X axis → **Format → Alignment → Rotate 45°**
10. Title: "Average Daily Return by Ticker × Month"

---

### WS3: Risk vs. Return Scatter

1. New worksheet → rename to `Risk vs Return`
2. **Columns:** `[Annualized Volatility]` (calculated field, aggregated as AVG)
3. **Rows:** `[Annualized Return]` (calculated field, aggregated as AVG)
4. **Marks → Detail:** drag `[ticker]`
5. **Marks → Color:** drag `[ticker]` (same custom colours as WS1)
6. **Marks → Size:** drag `AVG([volume])` to Size
7. **Marks → Label:** drag `[ticker]` to Label → always show labels
8. Mark type: **Circle**
9. Add a reference line: **Analytics pane → Reference Line → Table → Line: Average → `[Annualized Return]`**
10. Adjust axes: right-click X axis → Edit Axis → Fixed range 0.0 to 0.80
11. Format both axes: Numbers → Percentage, 1 decimal place
12. Title: "Risk vs. Return by Ticker (bubble size = avg volume)"

---

### WS4: Volume Bar Chart

1. New worksheet → rename to `Volume Analysis`
2. **Columns:** `[ticker]`
3. **Rows:** `AVG([volume])`
4. **Color mark:** `[ticker]` (same custom colours)
5. Sort: descending by `AVG([volume])`
6. Add data labels: **Marks → Label → Show mark labels → On**
7. Format Y axis: Numbers → Number (Custom) → `#,##0`
8. Title: "Average Daily Trading Volume by Ticker"

---

### WS5: Daily Return Distribution (Histogram)

1. New worksheet → rename to `Return Distribution`
2. Right-click `[daily_return]` in the Data pane → **Create → Bins**
   - Bin size: `0.01` (1%)
   - Name: `daily_return (bin)`
3. **Columns:** `[daily_return (bin)]` → set to **Continuous**
4. **Rows:** `CNT([daily_return])` (Count)
5. **Color mark:** `[ticker]`
6. Mark type: **Bar**
7. Set **Stack marks → Off** (so bars overlay rather than stack)
   → `Analysis → Stack Marks → Off`
8. Adjust opacity: Color mark → Opacity → 60%
9. Title: "Distribution of Daily Returns by Ticker"

---

## Step 4: Build Dashboards

### Dashboard 1: Market Overview

1. New Dashboard → rename to `Market Overview`
2. Size: **Automatic** (or 1200 × 800 px)
3. Drag worksheets from the left panel:
   - **WS1 (Price Trends)** — top, full width
   - **WS4 (Volume Analysis)** — bottom-left
   - **WS5 (Return Distribution)** — bottom-right
4. Add a **Text object** at top: "Stock Market Performance Analysis — 2022–2024"
   Font: Arial 16pt bold, dark blue `#1F4E79`
5. Use floating layout for the text object
6. Add a **Ticker filter** from WS1 to filter all sheets:
   - Click the WS1 view in the dashboard → click the filter icon (funnel) in the top-right
   - Repeat for WS4 and WS5 to apply the same filter across all

### Dashboard 2: Risk-Return Analysis

1. New Dashboard → rename to `Risk-Return Analysis`
2. Drag worksheets:
   - **WS2 (Monthly Returns Cross-Tab)** — top, full width (60% height)
   - **WS3 (Risk vs. Return Scatter)** — bottom, full width (40% height)
3. Add a title text object: "Risk-Adjusted Performance Analysis"

---

## Step 5: Build the Story (4 Points)

1. New Story → rename to `Stock Market Story`
2. Size: match dashboard size (Automatic or 1200 × 800)

### Story Point 1 — "Three Years, Four Companies, One Market"

1. Drag **Dashboard 1 (Market Overview)** into the story canvas
2. Click the caption box → type:
   > "From 2022 to 2024, four technology stocks navigated the same macro
   > environment — rising interest rates, the AI boom, and sector rotation —
   > but arrived at dramatically different destinations."
3. Click **Add caption** → rename the story point tab to `Three Years`

### Story Point 2 — "Returns Tell Half the Story"

1. Click **Blank** to add a new story point
2. Drag **WS2 (Monthly Returns Cross-Tab)** into the canvas
3. Caption:
   > "Average returns hide month-to-month volatility. This heatmap reveals
   > how often each stock turned green — and how often it didn't. NVDA's
   > 2023 run (green across the board) stands in stark contrast to TSLA's
   > persistent red."
4. Rename tab: `Returns Heatmap`
5. Optional: add an annotation on NVDA April 2023 → right-click the cell → Annotate → Mark
   → Text: "+30.3% in April 2023"

### Story Point 3 — "Risk Is What You Pay for Performance"

1. Click **Blank** for a new story point
2. Drag **Dashboard 2 (Risk-Return Analysis)** into the canvas
3. Caption:
   > "NVDA's return is impressive — but adjusted for volatility, the picture
   > changes. MSFT delivered nearly 26% annualized return at only 25%
   > volatility. TSLA carried near-NVDA volatility but produced a negative
   > total return. Sharpe ratios separate winners from gamblers."
4. Rename tab: `Risk vs Return`

### Story Point 4 — "Where the Smart Money Should Go"

1. Click **Blank** for a new story point
2. Drag **WS3 (Risk vs. Return Scatter)** into the canvas
3. Caption:
   > "MSFT is the clear winner: Sharpe ratio 0.84, total return +96%, max
   > drawdown only −36%. For growth exposure, NVDA offers the highest raw
   > return but demands a high-volatility stomach. TSLA and AAPL both
   > underperformed on a risk-adjusted basis in this three-year window.
   > Recommendation: overweight MSFT, tactical allocation to NVDA,
   > underweight TSLA and AAPL."
4. Rename tab: `Recommendation`

---

## Step 6: Save & Package

1. `File → Save As` → name: `stock_market_story`
2. Save to `tableau/` folder
3. `File → Export Packaged Workbook` → save as `stock_market_story.twbx`
   (`.twbx` embeds the CSV data so the file is self-contained)
4. Verify: close and reopen the `.twbx` — all worksheets and story should render
   without prompting for the CSV files

**Screenshot:**
1. Navigate to Story Point 1
2. `Dashboard → Export Image` (Tableau Desktop) or use OS screenshot tool
3. Save to `screenshots/tableau_story.png`

---

## Colour Palette Used

| Element | Hex | Rationale |
|---|---|---|
| AAPL | `#808080` | Neutral gray — Apple's understated brand |
| MSFT | `#00A4EF` | Microsoft blue |
| NVDA | `#76B900` | NVIDIA green |
| TSLA | `#CC0000` | Tesla red |
| Positive return | `#375623` | Dark green |
| Negative return | `#9C0006` | Dark red |
| Neutral / center | `#FFFFFF` | White for diverging scale midpoint |
| Background | `#F2F2F2` | Light gray — reduces eye strain on dense data |

---

## Acceptance Checklist

- [ ] `.twbx` opens without prompting for external files (data embedded)
- [ ] All 5 worksheets render correctly
- [ ] Both dashboards lay out without overlapping visuals
- [ ] Story has exactly 4 points, each with a caption
- [ ] Cross-tab (WS2) shows red-white-green colour scale correctly
- [ ] Calculated fields `[Annualized Return]`, `[Annualized Volatility]`, `[Sharpe Ratio]` use `log_return` (not `daily_return`)
- [ ] Scatter (WS3) has data labels showing ticker names
- [ ] Screenshot saved to `screenshots/tableau_story.png`
- [ ] Story captions reference actual computed Sharpe values (not placeholders)

---

## Interview Pitch

> "In Tableau, I built a 4-step story that walks the viewer from a macro
> overview of three years of price trends, through a monthly returns
> cross-tab heatmap, to a risk-return scatter plot, and finally to a
> data-driven investment recommendation — using calculated fields for
> Sharpe ratio and annualized volatility based on log returns, and a
> custom diverging colour palette that makes month-by-month performance
> instantly legible."
