"""
clean_data.py
-------------
Business question: Prepare a clean, enriched dataset from raw OHLCV data so
that all three portfolio projects (Excel, Power BI, Tableau) share the same
analytical foundation.

Steps:
  1. Load data/raw/stocks_raw.csv
  2. Coerce dtypes (date → datetime, prices/volume → numeric)
  3. Remove duplicates and rows with null prices
  4. Sort by ticker → date
  5. Compute daily_return and log_return per ticker (first row per ticker is
     dropped — no prior close exists)
  6. Add time-dimension columns: year, month, quarter, day_of_week
     (these feed directly into pivot tables and slicers)
  7. Validate: zero nulls in critical columns, dates monotonically sorted
  8. Save to data/cleaned/stocks_cleaned.csv

Output columns:
  date, ticker, open, high, low, close, volume,
  daily_return, log_return,
  year, month, quarter, day_of_week
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

INPUT_PATH = Path("data/raw/stocks_raw.csv")
OUTPUT_PATH = Path("data/cleaned/stocks_cleaned.csv")

CRITICAL_PRICE_COLS = ["open", "high", "low", "close"]
CRITICAL_RETURN_COLS = ["daily_return", "log_return"]


# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------

def load_raw(path: Path) -> pd.DataFrame:
    """Load CSV and coerce dtypes. Errors in numeric columns become NaN."""
    df = pd.read_csv(path)

    df["date"] = pd.to_datetime(df["date"])

    numeric_cols = ["open", "high", "low", "close", "volume"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    return df


# ---------------------------------------------------------------------------
# Clean
# ---------------------------------------------------------------------------

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates(subset=["ticker", "date"])
    n = before - len(df)
    if n:
        print(f"  Removed {n} duplicate (ticker, date) rows.")
    return df


def remove_null_prices(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.dropna(subset=CRITICAL_PRICE_COLS)
    n = before - len(df)
    if n:
        print(f"  Removed {n} rows with null prices.")
    return df


def compute_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute per-ticker daily and log returns.

    daily_return = (close_t - close_{t-1}) / close_{t-1}
    log_return   = ln(close_t / close_{t-1})  [≡ ln(1 + daily_return)]

    The first row of each ticker group has no prior close — those rows are
    dropped so return columns are always non-null.
    """
    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)

    df["daily_return"] = df.groupby("ticker")["close"].pct_change()
    # log(1 + pct_change) = log(close_t / close_{t-1}) — exact log return
    df["log_return"] = np.log(1 + df["daily_return"])

    before = len(df)
    df = df.dropna(subset=CRITICAL_RETURN_COLS)
    n = before - len(df)
    print(f"  Dropped {n} first-row-per-ticker (no prior close for return calc).")

    return df


def add_time_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add calendar columns that pivot tables and slicers can filter on."""
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["quarter"] = df["date"].dt.quarter
    df["day_of_week"] = df["date"].dt.day_name()
    return df


# ---------------------------------------------------------------------------
# Validate
# ---------------------------------------------------------------------------

def validate(df: pd.DataFrame) -> None:
    """
    Hard checks before saving. Exits with code 1 if any check fails so the
    pipeline never silently produces bad data.
    """
    all_critical = CRITICAL_PRICE_COLS + CRITICAL_RETURN_COLS
    null_counts = df[all_critical].isnull().sum()
    if null_counts.any():
        print("\nERROR: Nulls found in critical columns:")
        print(null_counts[null_counts > 0])
        sys.exit(1)

    for ticker, grp in df.groupby("ticker"):
        if not grp["date"].is_monotonic_increasing:
            print(f"\nERROR: Dates not sorted for ticker {ticker}")
            sys.exit(1)

    # Sanity-check return magnitude (daily returns > 100% are suspicious)
    extreme = df[df["daily_return"].abs() > 1.0]
    if len(extreme):
        print(f"  Warning: {len(extreme)} rows with |daily_return| > 100%. Review GBM params.")

    print("  Validation passed: zero nulls in critical columns, dates sorted.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    print("Loading raw data...")
    df = load_raw(INPUT_PATH)
    print(f"  Raw shape: {df.shape}")
    print(f"  Dtypes:\n{df.dtypes.to_string()}")

    print("\nCleaning...")
    df = remove_duplicates(df)
    df = remove_null_prices(df)
    df = compute_returns(df)
    df = add_time_columns(df)
    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)

    print("\nValidating...")
    validate(df)

    df.to_csv(OUTPUT_PATH, index=False)

    # ---- Summary report ----
    print(f"\n{'='*50}")
    print(f"Saved to:  {OUTPUT_PATH}")
    print(f"Shape:     {df.shape}")
    print(f"Columns:   {list(df.columns)}")
    print(f"\nRows per ticker:")
    print(df.groupby("ticker").size().to_string())
    print(f"\nDate range: {df['date'].min().date()} → {df['date'].max().date()}")
    print(f"\nReturn stats (daily_return):")
    print(df.groupby("ticker")["daily_return"].agg(["mean", "std", "min", "max"])
            .round(4).to_string())
    print(f"\nFirst 5 rows:")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()
