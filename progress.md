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

## Tool Projects (Parallel — start after Phase 5)

| Phase | Tool | Status | Output | Notes |
|---|---|---|---|---|
| 6 | Excel | ⏳ Not started | `excel/stock_analyst_workbook.xlsx` | Delegate to Excel Agent |
| 7 | Power BI | ⏳ Not started | `powerbi/stock_executive_dashboard.pbix` | Delegate to Power BI Agent |
| 8 | Tableau | ⏳ Not started | `tableau/stock_market_story.twbx` | Delegate to Tableau Agent |

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
  raw/stocks_raw.csv            (3,128 rows — raw OHLCV)
  cleaned/stocks_cleaned.csv    (3,124 rows — with returns + time dims)
  cleaned/summary_stats.csv     (4 rows — per-ticker metrics)
  cleaned/correlation_matrix.csv (4×4 — Pearson close price correlation)
python/
  download_data.py              (yfinance + GBM fallback)
  clean_data.py                 (dtype coercion, returns, time dims)
  load_db.py                    (SQLite schema + indexes)
  analysis.py                   (summary stats + correlation)
sql/
  stock_analysis.sql            (8 analytical queries)
stocks.db                       (SQLite, 572 KB — gitignored)
```

---

## Next Steps

1. **Phase 6–8 (Parallel):** Open Excel, Power BI Desktop, and Tableau — build all three tool projects using `stocks_cleaned.csv` and `summary_stats.csv` as inputs.
2. **Phase 9:** Update `README.md` with actual screenshots, insights, and file links.
3. **Phase 10–11:** Interview prep → GitHub publish.
