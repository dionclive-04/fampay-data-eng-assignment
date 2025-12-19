import os
import pandas as pd


def write_per_ticker(df: pd.DataFrame, output_dir: str) -> None:
    """
    Writes one CSV file per ticker with exactly 24 monthly records.
    """

    os.makedirs(output_dir, exist_ok=True)

    for ticker, ticker_df in df.groupby("ticker"):
        ticker_df = ticker_df.sort_values("date")

        # Defensive validation
        assert len(ticker_df) == 24, f"{ticker} does not have 24 months of data"

        file_path = os.path.join(output_dir, f"result_{ticker}.csv")
        ticker_df.to_csv(file_path, index=False)
