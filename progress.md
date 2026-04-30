# Project Progress — Stock Market Performance Analysis

**Suite:** 3-project portfolio (Excel · Power BI · Tableau)  
**Tickers:** AAPL · TSLA · NVDA · MSFT | **Period:** 2022-01-04 → 2024-12-31  
**Data source:** Synthetic GBM (yfinance blocked by network; fallback activated)

---

## Shared Foundation

| Phase | Name | Status | Output | Notes |
|---|---|---|---|---|
| 1 | Project Setup | ✅ Done | Folder structure, `requirements.txt`, `.gitignore`, `README.md`, `git init` | Working dir = project root |
| 2 | Data Download | ✅ Done | `data/raw/stocks_raw.csv` — 3,128 rows, 4 tickers × 782 rows | GBM fallback; seed 42 |
| 3 | Data Cleaning | ✅ Done | `data/cleaned/stocks_cleaned.csv` — 3,124 rows, 13 columns | First row/ticker dropped (no prior close) |
| 4 | SQL Analysis | ✅ Done | `sql/stock_analysis.sql`, `python/load_db.py`, `stocks.db` | 8 queries; 3 indexes on stock_data |
| 5 | Python Analysis | ✅ Done | `data/cleaned/summary_stats.csv`, `data/cleaned/correlation_matrix.csv` | Sharpe, drawdown, volatility, correlation |

---

## Tool Projects (Phases 6–8)

| Phase | Tool | Status | Output | Notes |
|---|---|---|---|---|
| 6 | Excel | ✅ Done (partial) | `excel/stock_analyst_workbook.xlsx` (318 KB) + `excel/workbook_notes.md` | Built via openpyxl — **PivotTables + Slicers require GUI** (see workbook_notes.md) |
| 7 | Power BI | 📋 Notes ready | `powerbi/dashboard_notes.md` | `.pbix` requires Power BI Desktop GUI — full step-by-step instructions written |
| 8 | Tableau | 📋 Notes ready | `tableau/tableau_story_notes.md` | `.twbx` requires Tableau Desktop/Public GUI — full step-by-step instructions written |

### Phase 6 — Excel Detail

**Built programmatically (`python/build_excel.py` → openpyxl):**
- Sheet 1: Cover (title, meta, business questions, navigation)
- Sheet 2: Raw Data — 3,124 rows as Excel Table `tbl_Stocks` (TableStyleMedium9)
- Sheet 3: KPI Summary — values from `summary_stats.csv`, conditional formatting (red-white-green on Sharpe + Drawdown), Excel 365 formula references shown
- Sheet 4: Pivot Analysis — pre-computed pivot-equivalent tables (Pivot 1: return by ticker×year, Pivot 2: volume by month, Pivot 3: up/down days) with embedded GUI instructions
- Sheet 5: Charts — 3 openpyxl charts (line: price trend, bar: volume, scatter: risk vs. return)
- Sheet 6: Insights — 6 written analytical findings with investment recommendation

**Must be added manually (GUI only — openpyxl limitation):**
- Live interactive PivotTables (step-by-step: `excel/workbook_notes.md`)
- Slicers connected across pivot tables
- PivotChart linked to Pivot 1

### Phase 7 — Power BI Detail (GUI instructions written)

`powerbi/dashboard_notes.md` covers:
- Data import and type verification for both CSVs
- Data model (relationship `Summary[ticker]` → `Stocks[ticker]`)
- All 7 DAX measures with inline comments (Total Return, Ann. Return, Ann. Vol, Sharpe, Avg Volume, Up/Down Days, Rolling 30D Volatility)
- Page 1: Executive Overview — 4 KPI cards, line chart, scatter chart, slicers
- Page 2: Matrix Analysis — returns heatmap (ticker × year-month), volume matrix with drill-down, conditional formatting
- Page 3: Deep Dive — volume bar chart, return distribution histogram, 30-day rolling volatility line chart
- Colour theme and ticker colour assignments
- Screenshot + save instructions

### Phase 8 — Tableau Detail (GUI instructions written)

`tableau/tableau_story_notes.md` covers:
- Data source setup (two CSVs connected via `ticker` relationship)
- All 5 calculated fields with formulas and business explanations
- All 5 worksheets (Price Trends, Cross-Tab Heatmap, Risk-Return Scatter, Volume Bar, Return Distribution)
- Both dashboards (Market Overview, Risk-Return Analysis)
- Full 4-point story with exact caption text (updated with real Sharpe values)
- Packaging as `.twbx` (self-contained)
- Colour palette rationale

---

## Final Integration

| Phase | Name | Status | Output | Notes |
|---|---|---|---|---|
| 9 | README & Polish | ⏳ Not started | `README.md` (final) | After all three tools complete |
| 10 | Interview Prep | ⏳ Not started | Pitch + Q&A answers | |
| 11 | Publish | ⏳ Not started | GitHub push | |

---

## Key Numbers (from Phase 5)

### Summary Stats

| Ticker | Total Return | Ann. Return | Ann. Volatility | Sharpe | Max Drawdown | Avg Vol/Day |
|---|---|---|---|---|---|---|
| MSFT | +96.4% | +25.7% | 25.1% | **0.84** | −35.9% | 25.9M |
| NVDA | +54.4% | +33.9% | 66.7% | 0.44 | −64.1% | 53.1M |
| TSLA | −51.5% | −2.6% | 65.0% | −0.11 | −89.0% | 103.9M |
| AAPL | −5.5% | +1.2% | 26.7% | −0.12 | −40.4% | 83.2M |

### Correlation Matrix (close prices, Pearson)

|  | AAPL | MSFT | NVDA | TSLA |
|---|---|---|---|---|
| **AAPL** | 1.00 | −0.59 | 0.20 | −0.29 |
| **MSFT** | −0.59 | 1.00 | 0.38 | 0.06 |
| **NVDA** | 0.20 | 0.38 | 1.00 | −0.51 |
| **TSLA** | −0.29 | 0.06 | −0.51 | 1.00 |

### Interview-ready insights
- **MSFT** is the clear winner on risk-adjusted return — highest Sharpe (0.84), modest volatility, 96% total gain.
- **NVDA** has the highest raw return (+34% annualized) but at 67% volatility — a high-risk high-reward bet.
- **TSLA** is the worst outcome: negative total return with near-NVDA volatility. Maximum drawdown hit −89% at its trough.
- **AAPL** is the "safe but disappointing" story — low volatility but barely broke even over 3 years.
- AAPL and MSFT are **negatively correlated (−0.59)**, which matters for portfolio construction — a holding of both partially hedges risk.

---

## Files Created So Far

```
data/
  raw/stocks_raw.csv                 (3,128 rows — raw OHLCV)
  cleaned/stocks_cleaned.csv         (3,124 rows — with returns + time dims)
  cleaned/summary_stats.csv          (4 rows — per-ticker metrics)
  cleaned/correlation_matrix.csv     (4×4 — Pearson close price correlation)
python/
  download_data.py                   (yfinance + GBM fallback)
  clean_data.py                      (dtype coercion, returns, time dims)
  load_db.py                         (SQLite schema + indexes)
  analysis.py                        (summary stats + correlation)
  build_excel.py                     (openpyxl workbook generator)
sql/
  stock_analysis.sql                 (8 analytical queries)
excel/
  stock_analyst_workbook.xlsx        (318 KB — 6 sheets, tbl_Stocks, 3 charts)
  workbook_notes.md                  (full rebuild instructions + PivotTable GUI steps)
powerbi/
  dashboard_notes.md                 (DAX measures + 3-page build instructions)
tableau/
  tableau_story_notes.md             (calculated fields + 4-point story build instructions)
stocks.db                            (SQLite, 572 KB — gitignored)
```

---

## Limitations Documented

| Tool | Limitation | Workaround |
|---|---|---|
| Excel | openpyxl cannot create PivotTables or Slicers | Pre-computed pivot-equivalent tables + step-by-step GUI instructions in `workbook_notes.md` |
| Power BI | `.pbix` is a binary format — not generatable by code | Full step-by-step GUI build instructions in `dashboard_notes.md` |
| Tableau | `.twbx` is a binary format — not generatable by code | Full step-by-step GUI build instructions in `tableau_story_notes.md` |
| Data | yfinance blocked by network | Synthetic GBM (seed 42) — documented in README and progress.md |

---

## Next Steps

1. **Phase 6 (complete):** Open `excel/stock_analyst_workbook.xlsx` → follow `workbook_notes.md` to add live PivotTables and Slicers → take screenshot → save to `screenshots/excel_pivot_view.png`
2. **Phase 7:** Open Power BI Desktop → follow `powerbi/dashboard_notes.md` → build dashboard → save as `powerbi/stock_executive_dashboard.pbix` → screenshot
3. **Phase 8:** Open Tableau Public → follow `tableau/tableau_story_notes.md` → build story → export as `tableau/stock_market_story.twbx` → screenshot
4. **Phase 9:** Update `README.md` with actual screenshots, insights, and file links.
5. **Phase 10–11:** Interview prep → GitHub publish.
