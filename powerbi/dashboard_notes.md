# Power BI Dashboard Build Notes
## Stock Performance Executive Dashboard — `stock_executive_dashboard.pbix`

> **Limitation:** `.pbix` files cannot be generated programmatically.
> These instructions are detailed enough to rebuild the dashboard from scratch
> in Power BI Desktop in approximately 60–90 minutes.
> Power BI Desktop is free: https://powerbi.microsoft.com/desktop/

---

## Prerequisites

- Power BI Desktop (latest version, free)
- `data/cleaned/stocks_cleaned.csv`
- `data/cleaned/summary_stats.csv`

---

## Step 1: Data Import

1. Open Power BI Desktop → **Get data → Text/CSV**
2. Select `data/cleaned/stocks_cleaned.csv` → **Load**
3. Repeat for `data/cleaned/summary_stats.csv`
4. In the **Fields** pane, you should see two tables: `stocks_cleaned` and `summary_stats`

**Rename the tables:**
- Right-click `stocks_cleaned` → Rename → `Stocks`
- Right-click `summary_stats` → Rename → `Summary`

**Verify column types (Transform Data → Power Query):**
| Column | Type |
|---|---|
| `date` | Date |
| `ticker` | Text |
| `open`, `high`, `low`, `close`, `daily_return`, `log_return` | Decimal Number |
| `volume`, `year`, `month`, `quarter` | Whole Number |
| `day_of_week` | Text |

5. Click **Close & Apply**

---

## Step 2: Data Model

No relationship needed between `Stocks` and `Summary` — they're used
independently on different pages. Both tables contain a `ticker` column
which Power BI visuals can slice natively.

If you want drill-through from Summary to Stocks, create a relationship:
- `Summary[ticker]` → `Stocks[ticker]` (Many-to-One, single direction)

---

## Step 3: DAX Measures

Create all measures in the `Stocks` table. Click the table name in Fields
pane → **Table tools → New measure**.

```dax
// ─── Total Return % ────────────────────────────────────────────────────────
// Percentage change from earliest to latest close price in the current filter.
Total Return % =
VAR FirstClose =
    CALCULATE(
        FIRSTNONBLANK(Stocks[close], 1),
        FILTER(ALL(Stocks[date]), Stocks[date] = MIN(Stocks[date]))
    )
VAR LastClose =
    CALCULATE(
        LASTNONBLANK(Stocks[close], 1),
        FILTER(ALL(Stocks[date]), Stocks[date] = MAX(Stocks[date]))
    )
RETURN
    DIVIDE(LastClose - FirstClose, FirstClose)


// ─── Annualized Return ─────────────────────────────────────────────────────
// Mean daily return × 252 trading days.
Annualized Return =
AVERAGE(Stocks[daily_return]) * 252


// ─── Annualized Volatility ─────────────────────────────────────────────────
// Population standard deviation of daily returns × √252.
// Uses STDEVX.P (population) for consistency with SQL analysis.
Annualized Volatility =
STDEVX.P(Stocks, Stocks[daily_return]) * SQRT(252)


// ─── Sharpe Ratio ──────────────────────────────────────────────────────────
// Risk-adjusted return: (ann. return − risk-free rate) ÷ ann. volatility.
// Risk-free rate: 4.5% (approximate 2022-2024 US Treasury average).
Sharpe Ratio =
DIVIDE(
    [Annualized Return] - 0.045,
    [Annualized Volatility]
)


// ─── Avg Daily Volume ──────────────────────────────────────────────────────
// Mean daily trading volume in the current filter context.
Avg Daily Volume =
AVERAGE(Stocks[volume])


// ─── Up Days ───────────────────────────────────────────────────────────────
// Count of days where the daily return was positive.
Up Days =
CALCULATE(COUNTROWS(Stocks), Stocks[daily_return] > 0)


// ─── Down Days ─────────────────────────────────────────────────────────────
// Count of days where the daily return was zero or negative.
Down Days =
CALCULATE(COUNTROWS(Stocks), Stocks[daily_return] <= 0)
```

**Format measures:**
- `Total Return %`, `Annualized Return`, `Annualized Volatility`: Percentage, 2 decimal places
- `Sharpe Ratio`: Fixed decimal, 2 places
- `Avg Daily Volume`: Whole number, thousands separator

---

## Step 4: Page 1 — Executive Overview

**Rename the default page:** double-click the tab → `Executive Overview`

### KPI Cards (top row)

Insert 4 **Card** visuals side by side:
1. Field: `[Total Return %]` | Label: "Total Return"
2. Field: `[Annualized Volatility]` | Label: "Ann. Volatility"
3. Field: `[Sharpe Ratio]` | Label: "Sharpe Ratio"
4. Field: `[Avg Daily Volume]` | Label: "Avg Daily Volume"

Format each card:
- **Format visual → Callout value → Font:** Segoe UI Bold, 28pt
- **Category label → Font:** Segoe UI, 11pt, gray
- Add a thin border: **Format → Border → On → 1px**

### Line Chart — Close Price Over Time

- Visual: **Line chart**
- X axis: `Stocks[date]` (set to **Continuous** in format pane → X-axis → Type)
- Y axis: `Stocks[close]`
- Legend: `Stocks[ticker]`
- Title: "Closing Price by Ticker (2022–2024)"
- Colors: AAPL = #808080, MSFT = #00A4EF, NVDA = #76B900, TSLA = #CC0000
- Line stroke: 2px

### Scatter Plot — Risk vs. Return

- Visual: **Scatter chart**
- X axis: `[Annualized Volatility]`
- Y axis: `[Annualized Return]`
- Size: `[Avg Daily Volume]`
- Legend/Details: `Stocks[ticker]`
- Title: "Risk vs. Return (bubble size = avg volume)"
- Add a constant line at Y = 0: **Analytics pane → Y-Axis Constant Line → 0**

### Slicers

- Insert **Slicer** → Field: `Stocks[ticker]` → Style: Tile
- Insert **Slicer** → Field: `Stocks[date]` → Style: Between (date range)
- Place slicers in the top-right corner of the page

---

## Step 5: Page 2 — Matrix (Pivot) Analysis

**Add a new page** → rename to `Matrix Analysis`

### Matrix 1: Returns Heatmap (Ticker × Year-Month)

1. Insert a **Matrix** visual
2. **Rows:** `Stocks[ticker]`
3. **Columns:** `Stocks[year]`, then `Stocks[month]` (create a hierarchy or use both)
   - To show "YYYY-MM": add a calculated column in Power Query:
     `YearMonth = Text.From([year]) & "-" & Text.PadStart(Text.From([month]), 2, "0")`
   - Then use `Stocks[YearMonth]` as Columns
4. **Values:** `[Avg Daily Return]` → create this measure:
   ```dax
   Avg Daily Return = AVERAGE(Stocks[daily_return])
   ```
5. Format values: Percentage, 2 decimal places
6. **Conditional formatting:** click the Values field → Format → Conditional formatting
   - Style: **Color scale**
   - Min: lowest value → Red (`#9C0006`)
   - Center: 0 → White (`#FFFFFF`)
   - Max: highest value → Green (`#375623`)

### Matrix 2: Volume by Quarter

1. Insert a second **Matrix** visual below the first
2. **Rows:** `Stocks[ticker]`
3. **Columns:** `Stocks[year]`, then `Stocks[quarter]` (drill-down enabled automatically)
4. **Values:** `SUM(Stocks[volume])` or create:
   ```dax
   Total Volume = SUM(Stocks[volume])
   ```
5. Format: Whole number, thousands separator (#,##0)
6. Enable drill-down: click the double-arrow icon on the visual header

### Slicer

- Insert **Slicer** → `Stocks[ticker]` → Style: Tile
- This slicer should filter both matrices on this page

---

## Step 6: Page 3 — Volume & Volatility Deep Dive

**Add a new page** → rename to `Deep Dive`

### Bar Chart — Avg Daily Volume by Ticker

- Visual: **Clustered bar chart**
- Y axis (categories): `Stocks[ticker]`
- X axis (values): `[Avg Daily Volume]`
- Sort: descending by value
- Title: "Average Daily Volume by Ticker"
- Data labels: On, format #,##0

### Histogram — Daily Return Distribution

Power BI doesn't have a native histogram visual, so use this approach:

**Option A (built-in binning):**
1. Insert a **Column chart**
2. Drag `Stocks[daily_return]` to X axis → right-click → **New group**
3. Group type: Bin | Bin size: 0.01 (1%)
4. Y axis: Count of rows
5. Legend: `Stocks[ticker]`

**Option B (Python/R visual):**
1. Enable Python visual: File → Options → Python scripting
2. Insert **Python visual** → drag `daily_return` and `ticker` to Values
3. Script:
   ```python
   import matplotlib.pyplot as plt
   for ticker, grp in dataset.groupby('ticker'):
       plt.hist(grp['daily_return'], bins=50, alpha=0.5, label=ticker)
   plt.legend()
   plt.xlabel('Daily Return')
   plt.ylabel('Count')
   plt.title('Distribution of Daily Returns')
   plt.show()
   ```

### Line Chart — 30-Day Rolling Volatility

Create a DAX measure for rolling volatility:
```dax
Rolling 30D Volatility =
CALCULATE(
    STDEVX.P(Stocks, Stocks[daily_return]),
    DATESINPERIOD(Stocks[date], LASTDATE(Stocks[date]), -30, DAY)
) * SQRT(252)
```

- Visual: **Line chart**
- X axis: `Stocks[date]`
- Y axis: `[Rolling 30D Volatility]`
- Legend: `Stocks[ticker]`
- Title: "30-Day Rolling Annualized Volatility"
- Format Y axis: Percentage, 0 decimal places

---

## Step 7: Formatting & Theme

**Apply a colour theme:**
1. `View → Themes → Browse for themes` or use a preset
2. Recommended: use the built-in "Executive" theme

**Consistent colours for tickers** (use throughout all pages):
| Ticker | Hex |
|---|---|
| AAPL | `#808080` (gray) |
| MSFT | `#00A4EF` (Microsoft blue) |
| NVDA | `#76B900` (NVIDIA green) |
| TSLA | `#CC0000` (Tesla red) |

To apply custom colours: Format visual → Data colors → click each series → enter hex.

**Page background:** Light gray `#F2F2F2` or white

---

## Step 8: Save & Screenshot

1. `File → Save As → stock_executive_dashboard.pbix`
2. Save to `powerbi/` folder in the project root
3. Take a screenshot of Page 1: `Windows + Shift + S` (or Snipping Tool)
4. Save to `screenshots/powerbi_dashboard.png`

---

## Acceptance Checklist

- [ ] All 3 pages render without errors
- [ ] Slicers on Page 1 filter all visuals correctly
- [ ] Matrix on Page 2 shows conditional red-white-green formatting
- [ ] Drill-down on Volume matrix works
- [ ] Sharpe ratio values in range [−1, 3]
- [ ] Annualized volatility in range [15%, 70%]
- [ ] No "(blank)" appearing in visuals
- [ ] Screenshot saved to `screenshots/powerbi_dashboard.png`
- [ ] File saved as `powerbi/stock_executive_dashboard.pbix`

---

## Interview Pitch

> "In Power BI, I built a 3-page executive dashboard using 7 DAX measures —
> including a rolling 30-day volatility measure and a Sharpe ratio calculation
> — with a Matrix visual heatmap of monthly returns by ticker, and drill-through
> from quarterly volume summaries to daily data, demonstrating how the same
> dataset that underperforms in Excel scales to enterprise BI."
