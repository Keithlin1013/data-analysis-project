"""
load_db.py
----------
Business question: Persist the cleaned dataset into a relational database so
that SQL window functions, aggregations, and pivot-style queries can be run
directly against it.

Creates stocks.db (SQLite) with:
  - Table: stock_data  (schema with explicit type affinities)
  - Index: idx_ticker          — fast GROUP BY / filter on ticker
  - Index: idx_date            — fast date range filtering
  - Index: idx_ticker_date     — composite; optimal for per-ticker time series

SQLite type notes:
  - DATE is stored as TEXT ('YYYY-MM-DD') — SQLite has no native date type.
    Date comparison operators work correctly on ISO-8601 strings.
  - FLOAT maps to REAL affinity (8-byte IEEE 754 float).
  - INTEGER maps to INTEGER affinity.
"""

import sqlite3
from pathlib import Path

import pandas as pd

CSV_PATH = Path("data/cleaned/stocks_cleaned.csv")
DB_PATH = Path("stocks.db")


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

CREATE_TABLE_SQL = """
CREATE TABLE stock_data (
    date          TEXT     NOT NULL,  -- 'YYYY-MM-DD'; ISO-8601 sorts correctly
    ticker        TEXT     NOT NULL,
    open          FLOAT    NOT NULL,
    high          FLOAT    NOT NULL,
    low           FLOAT    NOT NULL,
    close         FLOAT    NOT NULL,
    volume        INTEGER  NOT NULL,
    daily_return  FLOAT    NOT NULL,
    log_return    FLOAT    NOT NULL,
    year          INTEGER  NOT NULL,
    month         INTEGER  NOT NULL,
    quarter       INTEGER  NOT NULL,
    day_of_week   TEXT     NOT NULL,
    PRIMARY KEY (ticker, date)
);
"""

INDEX_STATEMENTS = [
    "CREATE INDEX idx_ticker      ON stock_data (ticker);",
    "CREATE INDEX idx_date        ON stock_data (date);",
    "CREATE INDEX idx_ticker_date ON stock_data (ticker, date);",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def create_schema(conn: sqlite3.Connection) -> None:
    conn.execute("DROP TABLE IF EXISTS stock_data;")
    conn.execute(CREATE_TABLE_SQL)
    conn.commit()
    print("  Table stock_data created.")


def create_indexes(conn: sqlite3.Connection) -> None:
    for stmt in INDEX_STATEMENTS:
        conn.execute(stmt)
    conn.commit()
    index_names = [s.split()[2] for s in INDEX_STATEMENTS]
    print(f"  Indexes created: {', '.join(index_names)}")


def load_data(conn: sqlite3.Connection) -> int:
    df = pd.read_csv(CSV_PATH)
    # to_sql with if_exists='append' respects the existing schema (incl. PRIMARY KEY)
    df.to_sql("stock_data", conn, if_exists="append", index=False)
    return len(df)


def verify(conn: sqlite3.Connection) -> None:
    """Spot-checks to confirm data landed correctly."""
    cur = conn.cursor()

    row_count = cur.execute("SELECT COUNT(*) FROM stock_data;").fetchone()[0]
    assert row_count == 3124, f"Expected 3124 rows, got {row_count}"

    tickers = [r[0] for r in cur.execute(
        "SELECT DISTINCT ticker FROM stock_data ORDER BY ticker;"
    ).fetchall()]
    assert tickers == ["AAPL", "MSFT", "NVDA", "TSLA"], f"Unexpected tickers: {tickers}"

    nulls = cur.execute(
        "SELECT COUNT(*) FROM stock_data WHERE daily_return IS NULL OR log_return IS NULL;"
    ).fetchone()[0]
    assert nulls == 0, f"Found {nulls} null return rows"

    indexes = [r[1] for r in cur.execute("PRAGMA index_list('stock_data');").fetchall()]
    for name in ["idx_ticker", "idx_date", "idx_ticker_date"]:
        assert name in indexes, f"Missing index: {name}"

    print("  Verification passed: row count, tickers, nulls, indexes all OK.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"{CSV_PATH} not found. Run python/clean_data.py first."
        )

    # Remove stale DB so schema is always fresh
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"Removed existing {DB_PATH}.")

    print(f"Creating {DB_PATH}...")
    with sqlite3.connect(DB_PATH) as conn:
        print("Creating schema...")
        create_schema(conn)

        print("Loading data...")
        n = load_data(conn)
        print(f"  Inserted {n:,} rows into stock_data.")

        print("Creating indexes...")
        create_indexes(conn)

        print("Verifying...")
        verify(conn)

    # Summary
    size_kb = DB_PATH.stat().st_size / 1024
    print(f"\nDone. {DB_PATH} ({size_kb:.1f} KB)")
    print("Schema:\n")
    with sqlite3.connect(DB_PATH) as conn:
        schema = conn.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='stock_data';"
        ).fetchone()[0]
        print(schema)
        print("\nIndexes:")
        for row in conn.execute("PRAGMA index_list('stock_data');").fetchall():
            print(f"  {row[1]}")


if __name__ == "__main__":
    main()
