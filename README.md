# FamPay – Data Engineering Intern Take-Home Assignment

## Problem Statement

Financial data is typically captured at a high frequency (daily), but analytical use-cases often require a lower-frequency, macro-level view to identify trends.

The objective of this assignment is to:
- Convert **daily stock price data** into **monthly OHLC aggregates**
- Compute commonly used **technical indicators**
- Partition the final results into **per-ticker output files**

The entire solution is implemented using **Python (Pandas only)**, following a modular and production-oriented design.

---

## Dataset Overview

- **Time period:** 2 years (24 months)
- **Frequency:** Daily
- **Number of stocks:** 10

### Stock Tickers
```

AAPL, AMD, AMZN, AVGO, CSCO,
MSFT, NFLX, PEP, TMUS, TSLA

```

### Input Schema
```

date, volume, open, high, low, close, adjclose, ticker

```

---

## Solution Design (High-Level)

The solution is structured as a simple data pipeline with clearly separated responsibilities:

1. **Load & Validate Data**
2. **Aggregate Daily Data → Monthly OHLC**
3. **Calculate Technical Indicators**
4. **Write Partitioned Output Files**

Each step is implemented in its own module to improve readability, testability, and maintainability.

---

## Project Structure

```

fampay-stock-assignment/
│
├── output.csv
│
├── code/
│   ├── loader.py        # Data ingestion & validation
│   ├── aggregator.py   # Monthly OHLC aggregation
│   ├── indicators.py   # SMA & EMA calculations
│   ├── writer.py       # Output partitioning
│   └── main.py         # Pipeline orchestration
│
├── output/
│   |── result_AAPL.csv
|   ├── result_AMD.csv
|   ├── result_AMZN.csv
|   ├── result_AVGO.csv
|   ├── output/result_CSCO.csv
|   ├── output/result_MSFT.csv
|   ├── output/result_NFLX.csv
|   ├── output/result_PEP.csv
|   ├── output/result_TMUS.csv
|   ├── output/result_TSLA.csv
│
├── requirements.txt
└── README.md

```

---

## Data Loading & Validation (`loader.py`)

### Responsibilities
- Read CSV data
- Parse and validate the `date` column
- Ensure required schema is present
- Detect duplicate `(date, ticker)` records
- Ensure exactly **10 unique tickers**
- Sort data by `ticker` and `date`

### Why this matters
Monthly **Open** and **Close** values depend on record ordering.  
Explicit sorting guarantees correct first-day and last-day selection during aggregation.

Fail-fast validation prevents silent downstream data corruption.

---

## 📆 Monthly Aggregation Logic (`aggregator.py`)

Daily stock prices are resampled into **monthly OHLC** values using Pandas `Grouper`.

### Aggregation Rules

| Field  | Logic |
|------|------|
| Open | Price on the **first trading day** of the month |
| Close | Price on the **last trading day** of the month |
| High | Maximum price reached during the month |
| Low | Minimum price reached during the month |
| Volume | Sum of daily volumes |

A defensive check ensures **exactly 24 months** of data per ticker.

---

## Technical Indicators (`indicators.py`)

All indicators are calculated **only on monthly closing prices**, as required.

### Implemented Indicators
- **SMA 10** – 10-month Simple Moving Average
- **SMA 20** – 20-month Simple Moving Average
- **EMA 10** – 10-month Exponential Moving Average
- **EMA 20** – 20-month Exponential Moving Average

### Notes on Indicator Behavior
- SMA values are `NaN` for initial months due to insufficient historical data
- EMA values initialize immediately using the first available closing price
- Calculations are fully vectorized using Pandas (`rolling`, `ewm`)
- No external technical-analysis libraries are used

This behavior is mathematically correct and industry-standard.

---

## Output Generation (`writer.py`)

- One CSV file is written per stock ticker
- Each output file contains **exactly 24 rows**
- File naming convention:
```

result_<TICKER>.csv

```

Example:
```

result_AAPL.csv

````

Assertions ensure output completeness and correctness.

---

## How to Run the Project

```bash
pip install -r requirements.txt
python src/main.py
````
Note: Insert your own local path for the dataset in main.py file
All generated files will be available in the `output/` directory.

---

## Practical Assumptions

The following assumptions were made based on the problem statement and dataset:

* Each ticker has **complete daily data** for the full 24-month period
* No missing months exist for any ticker
* No duplicate `(date, ticker)` records are present
* Initial `NaN` values in SMA columns are expected due to rolling window requirements
* EMA initialization uses the first available closing price

Where possible, these assumptions are validated in code to avoid silent failures.

---

## Design Considerations

Key principles followed in this solution:

* Correct financial semantics (Open/Close are **not averages**)
* Defensive programming and early validation
* Modular, readable, and maintainable code
* Vectorized Pandas operations for performance
* Clear separation between transformation logic and I/O
* 
