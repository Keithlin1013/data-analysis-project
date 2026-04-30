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
- **Source used:** _(to be filled after Phase 2 completes)_

---

## Project 1: Stock Analyst's Workbook (Excel)

> _Section to be completed after Phase 6._

**Tool:** Microsoft Excel  
**Why Excel:** Best tool for hands-on exploratory analysis where the analyst
needs to slice data interactively and build formula-driven summaries quickly.

**File:** `excel/stock_analyst_workbook.xlsx`  
**Build notes:** `excel/workbook_notes.md`

### Screenshot
_(to be added after Phase 6)_

### Key Insights
_(to be filled after Phase 6)_

---

## Project 2: Stock Performance Executive Dashboard (Power BI)

> _Section to be completed after Phase 7._

**Tool:** Power BI Desktop  
**Why Power BI:** Best for enterprise KPI monitoring where stakeholders need
a live, filterable dashboard with calculated metrics and drill-through.

**File:** `powerbi/stock_executive_dashboard.pbix`  
**Build notes:** `powerbi/dashboard_notes.md`

### Screenshot
_(to be added after Phase 7)_

### Key Insights
_(to be filled after Phase 7)_

---

## Project 3: Stock Market Storytelling Report (Tableau)

> _Section to be completed after Phase 8._

**Tool:** Tableau Public  
**Why Tableau:** Best for narrative-driven presentations where the goal is
guiding a non-technical audience through a sequence of insights.

**File:** `tableau/stock_market_story.twbx`  
**Build notes:** `tableau/tableau_story_notes.md`

### Screenshot
_(to be added after Phase 8)_

### Key Insights
_(to be filled after Phase 8)_

---

## Top 5 Insights

_(to be filled after all three projects complete)_

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
cd stock-market-analysis

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

_(Your name here)_  
Data Analyst | New York, NY  
[LinkedIn]() · [GitHub]()
