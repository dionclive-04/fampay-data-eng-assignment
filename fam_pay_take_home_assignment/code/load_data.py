import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads stock data from CSV, parses dates, and sorts records.

    Assumptions:
    - Data contains no duplicate rows per ticker per day
    - Date column is in YYYY-MM-DD format
    """
    df = pd.read_csv(file_path)

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by=["ticker", "date"]).reset_index(drop=True)
    print(df[df.duplicated()])
    return df
