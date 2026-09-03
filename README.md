# Stock Market Performance Analysis

**A 3-project portfolio suite for Data Analyst job applications.**
Same dataset. Same business questions. Three tools — to show tool-agnostic
thinking and direct skill comparison.

---

## Business Problem

Which of four tech stocks — AAPL, TSLA, NVDA, MSFT — delivered the best
risk-adjusted return over the 2022–2024 period? This suite analyzes price
trends, daily returns, volatility, trading volume, and Sharpe ratios to
produce a defensible investment recommendation.

---

## The Three Projects

| # | Project | Tool | Centerpiece |
|---|---|---|---|
| 1 | Stock Analyst's Workbook | Microsoft Excel | PivotTables + Slicers |
| 2 | Stock Performance Executive Dashboard | Power BI | Matrix visuals + DAX |
| 3 | Stock Market Storytelling Report | Tableau | 4-step Story + cross-tab |

Each project answers the same 6 business questions:

1. How did each stock's closing price trend over three years?
2. What were the average daily and annualized returns?
3. Which stock was most volatile?
4. What volume patterns are visible?
5. How does each stock compare on risk vs. return?
6. Which stock is the best investment on a risk-adjusted basis?

---

## Data Source

- **Tickers:** AAPL, TSLA, NVDA, MSFT
- **Date range:** 2022-01-03 to 2024-12-31
- **Primary source:** Yahoo Finance via `yfinance`
- **Fallback:** Synthetic data via Geometric Brownian Motion (see `python/download_data.py`)
- **Source used:** Synthetic GBM (yfinance blocked by network — fallback activated automatically; see `python/download_data.py` for parameters)

---

## Project 1: Stock Analyst's Workbook (Excel)

**Status: built.** `excel/stock_analyst_workbook.xlsx` has 12 sheets — 6
generated programmatically (`python/build_excel.py`, via openpyxl) and 6
more built by hand in Excel on top of that base.

**Tool:** Microsoft Excel  
**Why Excel:** Best tool for hands-on exploratory analysis where the analyst
needs to slice data interactively and build formula-driven summaries quickly.

**File:** `excel/stock_analyst_workbook.xlsx`  
**Build notes:** `excel/workbook_notes.md`

**Sheets:**
- **Cover** — title, business questions, navigation
- **Raw Data** — `stocks_cleaned.csv` as Excel Table `tbl_Stocks` (3,124 rows)
- **KPI Summary** — per-ticker total/annualized return, volatility, Sharpe, drawdown, avg volume, with conditional formatting
- **PT - Avg Return**, **PT - Volatility**, **PT - Return Over Time** — three live, interactive Excel PivotTables built from a shared pivot cache over `tbl_Stocks`
- **Pivot Analysis** — pre-computed pivot-equivalent tables (return by ticker×year, volume by month, up/down day counts)
- **Dashboard** — summary view pulling live formulas from KPI Summary
- **Rolling Analytics** — 30-day rolling annualized volatility and rolling Sharpe ratio per ticker
- **Portfolio Construction** — equal-weight vs. custom-weight allocation comparison
- **Charts** — line (price trend), bar (volume), scatter (risk vs. return)
- **Insights** — 6 written analytical findings with investment recommendation

**Known gap:** Slicers have not been added to the PivotTables yet (see
`excel/workbook_notes.md` for the exact remaining steps).

### Screenshot
_(pending — no GUI screenshot has been captured yet)_

### Key Insights
- MSFT has the best risk-adjusted return (Sharpe 0.84) of the four tickers
- NVDA has the highest raw annualized return (+34%) but at 67% volatility
- TSLA is the standout underperformer, with an −89% max drawdown

---

## Project 2: Stock Performance Executive Dashboard (Power BI)

**Status: build notes ready; `.pbix` not yet built.** Power BI Desktop is a
GUI application and doesn't run in this environment, so the dashboard hasn't
been assembled yet. `powerbi/dashboard_notes.md` contains a complete,
click-level build guide (data import, data model, all 7 DAX measures, and
the layout for all 3 pages) so it can be built from the CSVs in one sitting.

**Tool:** Power BI Desktop  
**Why Power BI:** Best for enterprise KPI monitoring where stakeholders need
a live, filterable dashboard with calculated metrics and drill-through.

**File:** `powerbi/stock_executive_dashboard.pbix` _(not yet created)_  
**Build notes:** `powerbi/dashboard_notes.md`

### Screenshot
_(pending — file not yet built)_

### Key Insights
_(to be filled in once the dashboard is built)_

---

## Project 3: Stock Market Storytelling Report (Tableau)

**Status: build notes ready; `.twbx` not yet built.** Same situation as
Power BI — Tableau Desktop/Public is a GUI application not available in
this environment. `tableau/tableau_story_notes.md` contains the full build
guide: 5 calculated fields, 5 worksheets, 2 dashboards, and exact caption
text for the 4-point story.

**Tool:** Tableau Public  
**Why Tableau:** Best for narrative-driven presentations where the goal is
guiding a non-technical audience through a sequence of insights.

**File:** `tableau/stock_market_story.twbx` _(not yet created)_  
**Build notes:** `tableau/tableau_story_notes.md`

### Screenshot
_(pending — file not yet built)_

### Key Insights
_(to be filled in once the story is built)_

---

## Top 5 Insights

Computed in `python/analysis.py` from three years of (synthetic) daily
price data — see `data/cleaned/summary_stats.csv` and
`data/cleaned/correlation_matrix.csv`:

1. **MSFT is the best risk-adjusted bet.** Highest Sharpe ratio (0.84) of
   the four tickers, driven by a strong +96% total return at a comparatively
   modest 25% annualized volatility.
2. **NVDA is the high-risk, high-reward story.** Highest raw annualized
   return (+34%), but at 67% annualized volatility — more than 2.5x MSFT's —
   and a −64% max drawdown along the way.
3. **TSLA is the cautionary tale.** Negative total return (−51.5%) despite
   volatility on par with NVDA, with a −89% max drawdown at its worst point.
4. **AAPL is "safe but disappointing."** Lowest volatility (26.7%) of the
   four, but total return over the period was essentially flat (−5.5%).
5. **AAPL and MSFT are negatively correlated (−0.59).** That matters for
   portfolio construction — holding both partially hedges risk, which the
   Excel workbook's Portfolio Construction sheet explores directly.

---

## How to Reproduce

### Prerequisites

- Python 3.9+
- SQLite3 (included with Python)
- Microsoft Excel (for Project 1)
- Power BI Desktop — free download from Microsoft (for Project 2)
- Tableau Public — free download from Tableau (for Project 3)

### Setup

```bash
git clone <repo-url>
cd data-analysis-project

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

### Run the Pipeline

```bash
# Phase 2: Download data
python python/download_data.py

# Phase 3: Clean data
python python/clean_data.py

# Phase 4: SQL analysis
sqlite3 stocks.db < sql/stock_analysis.sql

# Phase 5: Python analysis
python python/analysis.py
```

After these four steps, all cleaned data and summary outputs are in `data/cleaned/`.
Open the Excel, Power BI, or Tableau files to explore the results.

---

## Tools & Versions

| Tool | Version |
|---|---|
| Python | 3.9+ |
| pandas | 2.2.3 |
| numpy | 1.26.4 |
| yfinance | 0.2.51 |
| scipy | 1.13.1 |
| SQLite | 3.x (stdlib) |
| Microsoft Excel | 2021 / Microsoft 365 |
| Power BI Desktop | Latest |
| Tableau Public | Latest |

---

## Author

Data Analyst
