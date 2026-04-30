# TODO.md

## Project: Stock Market Performance Analysis (3-Project Suite)

Three portfolio projects, same data, three different tools. Build the shared
foundation first (Phases 1–5), then build each tool-specific project (Phases
6, 7, 8).

---

## SHARED FOUNDATION

### Phase 1: Project Setup

- [ ] Create project folder: `stock-market-analysis`
- [ ] Create folders:
  - [ ] `data/raw`, `data/cleaned`
  - [ ] `python`, `sql`
  - [ ] `excel`, `powerbi`, `tableau`
  - [ ] `screenshots`
- [ ] Create `requirements.txt` with pinned versions
- [ ] Create `README.md` (initial skeleton with 3-project structure)
- [ ] Create `CLAUDE.md`, `todo.md`
- [ ] Initialize git repo, add `.gitignore`

**Acceptance:** Folder structure matches CLAUDE.md exactly.

---

### Phase 2: Data Collection

- [ ] Choose tickers: AAPL, TSLA, NVDA, MSFT
- [ ] Define date range: **2022-01-03 to 2024-12-31**
- [ ] Create `python/download_data.py`
- [ ] Implement primary path: `yfinance`
- [ ] Implement fallback: synthetic GBM
- [ ] Save raw data to `data/raw/stocks_raw.csv`
- [ ] Confirm columns: date, ticker, open, high, low, close, volume

### Required Test
```bash
python python/download_data.py
head data/raw/stocks_raw.csv
```

**Acceptance:** CSV has all 7 columns, all 4 tickers, ~750 rows per ticker.

---

### Phase 3: Data Cleaning

- [ ] Create `python/clean_data.py`
- [ ] Convert date to datetime, validate numeric dtypes
- [ ] Remove nulls and duplicates
- [ ] Sort by ticker then date
- [ ] Calculate `daily_return` and `log_return` per ticker
- [ ] Add `year`, `month`, `quarter`, `day_of_week` columns (helps pivot tables)
- [ ] Save to `data/cleaned/stocks_cleaned.csv`

### Required Test
```bash
python python/clean_data.py
python -c "import pandas as pd; df = pd.read_csv('data/cleaned/stocks_cleaned.csv'); print(df.info())"
```

**Acceptance:** Zero nulls in critical columns, dates sorted, returns computed per ticker.

---

### Phase 4: SQL Analysis

- [ ] Create `sql/stock_analysis.sql` with these queries:
  - [ ] Daily return using `LAG()`
  - [ ] Average daily return per ticker
  - [ ] Volatility per ticker
  - [ ] Average daily volume per ticker
  - [ ] Top 10 single-day gains and losses
  - [ ] 30-day rolling average close price
  - [ ] Risk-adjusted return (Sharpe proxy)
  - [ ] **Monthly returns by ticker (pivot-style query)** — useful for Excel
- [ ] Comment each query with the business question

### Required Test
```bash
sqlite3 stocks.db < sql/stock_analysis.sql
```

**Acceptance:** Every query returns results.

---

### Phase 5: Python Analysis & Summary Output

- [ ] Create `python/analysis.py`
- [ ] Compute per-ticker summary: total return, ann. return, ann. volatility, Sharpe, max drawdown, avg volume
- [ ] Compute correlation matrix between tickers
- [ ] Save `data/cleaned/summary_stats.csv` (one row per ticker)
- [ ] Save `data/cleaned/correlation_matrix.csv`

### Required Test
```bash
python python/analysis.py
cat data/cleaned/summary_stats.csv
```

**Acceptance:** Summary CSV has all 4 tickers with sensible values.

---

## PROJECT 1: EXCEL — STOCK ANALYST'S WORKBOOK

### Phase 6: Excel Build

**Goal:** Show mastery of Excel as a flexible analyst tool. The centerpiece is
**PivotTables and PivotCharts** with **Slicers** for interactivity.

#### File Structure (`excel/stock_analyst_workbook.xlsx`)

- [ ] **Sheet 1: Cover** — project title, business questions, navigation links
- [ ] **Sheet 2: Raw Data** — import `stocks_cleaned.csv` as Excel Table named `tbl_Stocks`
- [ ] **Sheet 3: KPI Summary** — formulas pulling from `tbl_Stocks`:
  - [ ] Total return per ticker (formula-driven, not hardcoded)
  - [ ] Annualized volatility (using STDEV × SQRT(252))
  - [ ] Average daily volume
  - [ ] Sharpe ratio
- [ ] **Sheet 4: PivotTable Analysis** — REQUIRED:
  - [ ] **Pivot 1:** Average daily return by ticker × year (rows = ticker, cols = year)
  - [ ] **Pivot 2:** Total volume by ticker × month (rows = month, cols = ticker)
  - [ ] **Pivot 3:** Count of positive vs. negative return days by ticker
  - [ ] Add **Slicers** for ticker and year
  - [ ] Add at least one **PivotChart** linked to a pivot
- [ ] **Sheet 5: Charts** — line chart of close prices, scatter plot of risk vs. return
- [ ] **Sheet 6: Insights** — written insights and recommendations

#### Build Documentation

- [ ] Create `excel/workbook_notes.md` documenting:
  - [ ] Step-by-step pivot setup (Insert → PivotTable → field placement)
  - [ ] Formulas used in KPI sheet
  - [ ] Slicer configuration
  - [ ] Any conditional formatting

### Required Test

- [ ] Open the .xlsx file, verify all sheets render
- [ ] Click a slicer and confirm pivots update
- [ ] Take a screenshot of the pivot view → save to `screenshots/excel_pivot_view.png`

**Acceptance:** PivotTables work interactively, slicers filter all pivots, no broken formulas.

---

## PROJECT 2: POWER BI — EXECUTIVE DASHBOARD

### Phase 7: Power BI Build

**Goal:** Show enterprise BI skills. The centerpiece is the **Matrix visual**
(Power BI's pivot table equivalent) with **DAX measures**.

#### File Structure (`powerbi/stock_executive_dashboard.pbix`)

- [ ] **Page 1: Executive Overview**
  - [ ] KPI cards: total return, ann. volatility, Sharpe ratio, avg volume
  - [ ] Line chart: close price over time, all tickers
  - [ ] Scatter plot: risk vs. return (one bubble per ticker, sized by volume)
  - [ ] Slicer: date range, ticker
- [ ] **Page 2: Matrix (Pivot) Analysis** — REQUIRED:
  - [ ] **Matrix visual:** ticker (rows) × year-month (columns), values = avg daily return
  - [ ] **Matrix visual:** ticker (rows) × quarter (columns), values = total volume
  - [ ] Conditional formatting (red/green color scale on returns)
- [ ] **Page 3: Volume & Volatility Deep Dive**
  - [ ] Volume bar chart by ticker
  - [ ] Daily return distribution histogram
  - [ ] 30-day rolling volatility line chart

#### Required DAX Measures

- [ ] `Total Return % = ...`
- [ ] `Annualized Volatility = STDEVX.P(...) * SQRT(252)`
- [ ] `Sharpe Ratio = ...`
- [ ] `Avg Daily Return = AVERAGE(Stocks[daily_return])`

#### Build Documentation

- [ ] Create `powerbi/dashboard_notes.md` documenting:
  - [ ] Data import steps
  - [ ] All DAX measures with comments
  - [ ] Each visual's field mappings
  - [ ] Color theme used

### Required Test

- [ ] Open .pbix, verify all pages render
- [ ] Use slicers to filter, confirm matrix updates
- [ ] Screenshot Page 1 → `screenshots/powerbi_dashboard.png`

**Acceptance:** All visuals work, slicers filter correctly, DAX measures return sensible values.

---

## PROJECT 3: TABLEAU — STORYTELLING REPORT

### Phase 8: Tableau Build

**Goal:** Show data storytelling. The centerpiece is a **4-step Story** with
**calculated fields** and a **cross-tab (pivot)** view.

#### File Structure (`tableau/stock_market_story.twbx`)

- [ ] **Data Source:** connect to `stocks_cleaned.csv` and `summary_stats.csv`
- [ ] **Worksheets to build first:**
  - [ ] WS1: Price trend lines (all tickers, time series)
  - [ ] WS2: **Cross-tab (pivot view)** — ticker × month × avg return, color-coded
  - [ ] WS3: Risk vs. return scatter
  - [ ] WS4: Volume bar chart
  - [ ] WS5: Distribution of daily returns (histogram)
- [ ] **Dashboards:** combine worksheets into 2 dashboards
- [ ] **Story (4 points):**
  - [ ] Story Point 1: "Three Years, Four Companies, One Market"
  - [ ] Story Point 2: "Returns Tell Half the Story"
  - [ ] Story Point 3: "Risk Is What You Pay for Performance"
  - [ ] Story Point 4: "Where the Smart Money Should Go"

#### Required Calculated Fields

- [ ] `Annualized Return` = AVG([log_return]) * 252
- [ ] `Annualized Volatility` = STDEV([log_return]) * SQRT(252)
- [ ] `Sharpe Ratio` = ([Annualized Return] - 0.045) / [Annualized Volatility]
- [ ] `Up Day Flag` = IF [daily_return] > 0 THEN 1 ELSE 0 END

#### Build Documentation

- [ ] Create `tableau/tableau_story_notes.md` documenting:
  - [ ] Calculated fields with explanations
  - [ ] Each worksheet's setup (rows, columns, marks)
  - [ ] Story point captions and key takeaway

### Required Test

- [ ] Open .twbx, verify all worksheets and story render
- [ ] Click through all 4 story points
- [ ] Screenshot the story → `screenshots/tableau_story.png`

**Acceptance:** Story flows logically, cross-tab is readable, calculated fields work.

---

## Phase 9: README & Portfolio Polish

- [ ] Update `README.md` with:
  - [ ] Project suite title and 3-project explanation
  - [ ] Business problem
  - [ ] Data source disclosure
  - [ ] Methodology
  - [ ] **Three separate sections** — one per project — each with:
    - [ ] Tool used and why
    - [ ] Screenshot
    - [ ] Link to the file in the repo
    - [ ] 2–3 key insights surfaced in that project
  - [ ] Combined "Top 5 Insights" section
  - [ ] How to reproduce
  - [ ] Tools used (with versions)
  - [ ] Author contact info

**Acceptance:** Recruiter understands all three projects in 60 seconds.

---

## Phase 10: Interview Prep

- [ ] Prepare 1-paragraph pitch for the full suite
- [ ] Prepare answers for:
  - [ ] Why three tools instead of one?
  - [ ] Which tool would you choose for X scenario? (and why)
  - [ ] Walk me through your pivot table analysis
  - [ ] What's the difference between Excel pivot, Power BI matrix, and Tableau cross-tab?
  - [ ] What did you learn?
  - [ ] What are your top 3 findings?
- [ ] Practice explaining Sharpe ratio, volatility, and risk-adjusted returns in plain English

**Acceptance:** You can talk about all three projects for 15 minutes without notes.

---

## Phase 11: Publish

- [ ] Final review (no typos, no leftover TODOs)
- [ ] Test full pipeline from clean clone
- [ ] Push to GitHub (public)
- [ ] Add link to resume (under "Projects" — list as one portfolio with three sub-projects)
- [ ] Add to LinkedIn featured section
- [ ] (Optional) LinkedIn post explaining the multi-tool approach

**Acceptance:** Repo is live; resume links to it; you can defend every choice in an interview.
