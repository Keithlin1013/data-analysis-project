"""
analysis.py
-----------
Business question: Produce a concise per-ticker summary of risk, return, and
volume metrics — and a correlation matrix of closing prices — so that all
three portfolio tools (Excel, Power BI, Tableau) can consume ready-made
summary data without recomputing statistics from scratch.

Outputs:
  data/cleaned/summary_stats.csv    — one row per ticker, 12 metrics
  data/cleaned/correlation_matrix.csv — 4×4 Pearson correlation of daily closes

Metrics computed:
  total_return          (last close / first close) - 1
  annualized_return     mean(daily_return) × 252
  annualized_volatility std(daily_return, ddof=1) × √252   [sample std dev]
  sharpe_ratio          (ann_return - 0.045) / ann_volatility
  max_drawdown          maximum peak-to-trough decline in close price
  avg_daily_volume      mean(volume)
  trading_days          row count per ticker
  start_date / end_date first and last date in the series
  start_price / end_price first and last closing price

Sharpe uses a 4.5 % risk-free rate (approximate 2022-2024 US Treasury avg).
Volatility uses sample std dev (ddof=1), consistent with financial convention.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

INPUT_PATH = Path("data/cleaned/stocks_cleaned.csv")
SUMMARY_PATH = Path("data/cleaned/summary_stats.csv")
CORR_PATH = Path("data/cleaned/correlation_matrix.csv")

RISK_FREE_RATE = 0.045  # annualized, used for Sharpe ratio
TRADING_DAYS_PER_YEAR = 252


# ---------------------------------------------------------------------------
# Metric helpers
# ---------------------------------------------------------------------------

def total_return(prices: pd.Series) -> float:
    """Percentage change from first to last observed close."""
    return (prices.iloc[-1] / prices.iloc[0]) - 1


def annualized_return(daily_returns: pd.Series) -> float:
    return daily_returns.mean() * TRADING_DAYS_PER_YEAR


def annualized_volatility(daily_returns: pd.Series) -> float:
    """Sample std dev (ddof=1) scaled to annual."""
    return daily_returns.std(ddof=1) * np.sqrt(TRADING_DAYS_PER_YEAR)


def sharpe_ratio(ann_ret: float, ann_vol: float) -> float:
    if ann_vol == 0:
        return np.nan
    return (ann_ret - RISK_FREE_RATE) / ann_vol


def max_drawdown(prices: pd.Series) -> float:
    """
    Maximum peak-to-trough percentage decline over the full period.
    A value of -0.30 means the stock fell 30 % from its highest point
    before recovering.
    """
    rolling_peak = prices.cummax()
    drawdown = (prices - rolling_peak) / rolling_peak
    return drawdown.min()


# ---------------------------------------------------------------------------
# Summary stats
# ---------------------------------------------------------------------------

def compute_summary(df: pd.DataFrame) -> pd.DataFrame:
    records = []
    for ticker, grp in df.groupby("ticker"):
        grp = grp.sort_values("date").reset_index(drop=True)
        prices = grp["close"]
        rets = grp["daily_return"]

        ann_ret = annualized_return(rets)
        ann_vol = annualized_volatility(rets)

        records.append(
            {
                "ticker": ticker,
                "start_date": grp["date"].iloc[0],
                "end_date": grp["date"].iloc[-1],
                "trading_days": len(grp),
                "start_price": round(prices.iloc[0], 2),
                "end_price": round(prices.iloc[-1], 2),
                "total_return": round(total_return(prices), 4),
                "annualized_return": round(ann_ret, 4),
                "annualized_volatility": round(ann_vol, 4),
                "sharpe_ratio": round(sharpe_ratio(ann_ret, ann_vol), 4),
                "max_drawdown": round(max_drawdown(prices), 4),
                "avg_daily_volume": int(grp["volume"].mean().round()),
            }
        )

    return pd.DataFrame(records).sort_values("sharpe_ratio", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Correlation matrix
# ---------------------------------------------------------------------------

def compute_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivot daily closes to wide format (date × ticker) and compute Pearson
    correlation. Correlation of closes (not returns) shows how similarly
    the absolute price levels move — useful for scatter plots in Tableau
    and Power BI.
    """
    wide = df.pivot(index="date", columns="ticker", values="close")
    corr = wide.corr(method="pearson").round(4)
    return corr


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_summary(df: pd.DataFrame) -> None:
    assert len(df) == 4, f"Expected 4 ticker rows, got {len(df)}"
    assert set(df["ticker"]) == {"AAPL", "TSLA", "NVDA", "MSFT"}

    # Sharpe ratios should be in a sane range for any 3-year equity period
    assert df["sharpe_ratio"].between(-3, 5).all(), "Sharpe out of [-3, 5] range"

    # Max drawdown must be negative (it's a loss)
    assert (df["max_drawdown"] <= 0).all(), "Max drawdown must be ≤ 0"

    # Annualized volatility for equities: expect 10%-100%
    assert df["annualized_volatility"].between(0.10, 1.00).all(), \
        "Volatility outside expected 10%-100% range"

    assert df.isnull().sum().sum() == 0, "Nulls found in summary_stats"
    print("  summary_stats validation passed.")


def validate_correlation(df: pd.DataFrame) -> None:
    assert df.shape == (4, 4), f"Expected 4×4 matrix, got {df.shape}"

    # Diagonal must be 1.0
    for ticker in df.index:
        assert df.loc[ticker, ticker] == 1.0, f"Diagonal [{ticker}] != 1.0"

    # All values in [-1, 1]
    assert ((df >= -1) & (df <= 1)).all().all(), "Correlation out of [-1, 1]"
    print("  correlation_matrix validation passed.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not INPUT_PATH.exists():
        print(f"ERROR: {INPUT_PATH} not found. Run python/clean_data.py first.")
        sys.exit(1)

    print("Loading cleaned data...")
    df = pd.read_csv(INPUT_PATH, parse_dates=["date"])
    print(f"  {len(df):,} rows, {df['ticker'].nunique()} tickers loaded.")

    # ---- Summary stats ----
    print("\nComputing summary statistics...")
    summary = compute_summary(df)

    print("\nValidating summary stats...")
    validate_summary(summary)

    summary.to_csv(SUMMARY_PATH, index=False)
    print(f"  Saved → {SUMMARY_PATH}")

    # ---- Correlation matrix ----
    print("\nComputing correlation matrix...")
    corr = compute_correlation(df)

    print("Validating correlation matrix...")
    validate_correlation(corr)

    corr.to_csv(CORR_PATH)
    print(f"  Saved → {CORR_PATH}")

    # ---- Console report ----
    print(f"\n{'='*60}")
    print("SUMMARY STATS (sorted by Sharpe ratio, best first):")
    print(f"{'='*60}")

    display_cols = [
        "ticker", "total_return", "annualized_return",
        "annualized_volatility", "sharpe_ratio", "max_drawdown",
        "avg_daily_volume",
    ]
    print(summary[display_cols].to_string(index=False))

    print(f"\n{'='*60}")
    print("CORRELATION MATRIX (close prices, Pearson):")
    print(f"{'='*60}")
    print(corr.to_string())

    print(f"\n{'='*60}")
    print("KEY TAKEAWAYS:")
    best = summary.iloc[0]
    worst_sharpe = summary.iloc[-1]
    most_volatile = summary.loc[summary["annualized_volatility"].idxmax()]
    print(f"  Best risk-adjusted:  {best['ticker']} "
          f"(Sharpe {best['sharpe_ratio']:.2f}, "
          f"ann. return {best['annualized_return']:.1%})")
    print(f"  Most volatile:       {most_volatile['ticker']} "
          f"(ann. vol {most_volatile['annualized_volatility']:.1%})")
    print(f"  Worst Sharpe:        {worst_sharpe['ticker']} "
          f"(Sharpe {worst_sharpe['sharpe_ratio']:.2f})")


if __name__ == "__main__":
    main()
