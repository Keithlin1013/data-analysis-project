-- stock_analysis.sql
-- ==================
-- Analytical queries for the Stock Market Performance Analysis portfolio.
-- Tickers: AAPL, TSLA, NVDA, MSFT | Date range: 2022-01-04 to 2024-12-31
--
-- Prerequisites: run `python python/load_db.py` to create and populate stocks.db.
--
-- Usage:
--   sqlite3 stocks.db < sql/stock_analysis.sql
-- ---------------------------------------------------------------------------

.headers ON
.mode column

-- ===========================================================================
-- Query 1: Daily return verification using LAG()
-- Business question: How did each stock's daily price change day-over-day,
-- and does the pre-computed daily_return column match a LAG()-derived value?
-- ===========================================================================
SELECT '=== Q1: Daily return via LAG() (first 10 rows per ticker) ===' AS "";

SELECT
    date,
    ticker,
    ROUND(close, 2)                                                        AS close,
    ROUND(LAG(close) OVER (PARTITION BY ticker ORDER BY date), 2)          AS prev_close,
    ROUND(
        (close - LAG(close) OVER (PARTITION BY ticker ORDER BY date))
        / LAG(close) OVER (PARTITION BY ticker ORDER BY date),
    6)                                                                     AS lag_daily_return,
    ROUND(daily_return, 6)                                                 AS stored_daily_return
FROM  stock_data
WHERE date IN (
    SELECT DISTINCT date
    FROM   stock_data
    ORDER  BY date
    LIMIT  10
)
ORDER BY ticker, date;


-- ===========================================================================
-- Query 2: Average daily return per ticker
-- Business question: Which stock had the highest average daily return,
-- and what does that translate to on an annualized basis?
-- ===========================================================================
SELECT '=== Q2: Average daily return per ticker ===' AS "";

SELECT
    ticker,
    ROUND(AVG(daily_return), 6)        AS avg_daily_return,
    ROUND(AVG(daily_return) * 252, 4)  AS annualized_return,
    COUNT(*)                           AS trading_days
FROM  stock_data
GROUP BY ticker
ORDER BY annualized_return DESC;


-- ===========================================================================
-- Query 3: Volatility per ticker
-- Business question: Which stock carried the most risk (highest price
-- variability), measured as annualized standard deviation of daily returns?
-- Note: SQLite has no STDEV function. Population std dev is computed as
--       SQRT( AVG(x^2) - AVG(x)^2 ), equivalent to pandas .std(ddof=0).
-- ===========================================================================
SELECT '=== Q3: Annualized volatility per ticker ===' AS "";

SELECT
    ticker,
    ROUND(
        SQRT(AVG(daily_return * daily_return) - AVG(daily_return) * AVG(daily_return)),
    6)                                                                      AS daily_vol,
    ROUND(
        SQRT(AVG(daily_return * daily_return) - AVG(daily_return) * AVG(daily_return))
        * SQRT(252),
    4)                                                                      AS annualized_volatility
FROM  stock_data
GROUP BY ticker
ORDER BY annualized_volatility DESC;


-- ===========================================================================
-- Query 4: Average daily volume per ticker
-- Business question: Which stock attracted the most trading activity,
-- and how much did volume vary?
-- ===========================================================================
SELECT '=== Q4: Average daily volume per ticker ===' AS "";

SELECT
    ticker,
    CAST(ROUND(AVG(volume)) AS INTEGER)  AS avg_daily_volume,
    MAX(volume)                          AS max_daily_volume,
    MIN(volume)                          AS min_daily_volume,
    CAST(ROUND(MAX(volume) - MIN(volume)) AS INTEGER) AS volume_range
FROM  stock_data
GROUP BY ticker
ORDER BY avg_daily_volume DESC;


-- ===========================================================================
-- Query 5a: Top 10 single-day gains
-- Query 5b: Top 10 single-day losses
-- Business question: What were the most extreme single-day price moves,
-- and which stocks were most prone to large swings?
-- ===========================================================================
SELECT '=== Q5a: Top 10 single-day gains ===' AS "";

SELECT
    ticker,
    date,
    ROUND(close, 2)        AS close,
    ROUND(daily_return, 4) AS daily_return
FROM  stock_data
ORDER BY daily_return DESC
LIMIT 10;

SELECT '=== Q5b: Top 10 single-day losses ===' AS "";

SELECT
    ticker,
    date,
    ROUND(close, 2)        AS close,
    ROUND(daily_return, 4) AS daily_return
FROM  stock_data
ORDER BY daily_return ASC
LIMIT 10;


-- ===========================================================================
-- Query 6: 30-day rolling average close price
-- Business question: What was the smoothed price trend for each stock,
-- filtering out day-to-day noise?
-- (Showing the last 5 rows per ticker for brevity)
-- ===========================================================================
SELECT '=== Q6: 30-day rolling average close (last 5 rows per ticker) ===' AS "";

SELECT
    date,
    ticker,
    ROUND(close, 2)  AS close,
    ROUND(
        AVG(close) OVER (
            PARTITION BY ticker
            ORDER BY date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ),
    2)               AS rolling_30d_avg
FROM  stock_data
WHERE date IN (
    SELECT DISTINCT date
    FROM   stock_data
    ORDER  BY date DESC
    LIMIT  5
)
ORDER BY ticker, date;


-- ===========================================================================
-- Query 7: Risk-adjusted return (Sharpe ratio proxy)
-- Business question: Which stock offered the best return per unit of risk?
-- Sharpe = (annualized_return - risk_free_rate) / annualized_volatility
-- Risk-free rate: 4.5% (approximate 2022-2024 US Treasury average)
-- ===========================================================================
SELECT '=== Q7: Sharpe ratio per ticker ===' AS "";

SELECT
    ticker,
    ROUND(AVG(daily_return) * 252, 4)   AS ann_return,
    ROUND(
        SQRT(AVG(daily_return * daily_return) - AVG(daily_return) * AVG(daily_return))
        * SQRT(252),
    4)                                   AS ann_volatility,
    ROUND(
        (AVG(daily_return) * 252 - 0.045)
        / (SQRT(AVG(daily_return * daily_return) - AVG(daily_return) * AVG(daily_return))
           * SQRT(252)),
    4)                                   AS sharpe_ratio
FROM  stock_data
GROUP BY ticker
ORDER BY sharpe_ratio DESC;


-- ===========================================================================
-- Query 8: Monthly returns by ticker — pivot-style
-- Business question: How did monthly performance compare across all four
-- stocks simultaneously? This pivot view feeds directly into Excel and
-- is the SQL analogue of a PivotTable.
-- ===========================================================================
SELECT '=== Q8: Monthly returns by ticker (pivot) ===' AS "";

SELECT
    STRFTIME('%Y-%m', date)                                    AS year_month,
    ROUND(AVG(CASE WHEN ticker = 'AAPL' THEN daily_return END) * 21, 4) AS AAPL,
    ROUND(AVG(CASE WHEN ticker = 'MSFT' THEN daily_return END) * 21, 4) AS MSFT,
    ROUND(AVG(CASE WHEN ticker = 'NVDA' THEN daily_return END) * 21, 4) AS NVDA,
    ROUND(AVG(CASE WHEN ticker = 'TSLA' THEN daily_return END) * 21, 4) AS TSLA
FROM  stock_data
GROUP BY year_month
ORDER BY year_month;
