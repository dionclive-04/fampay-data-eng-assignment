import pandas as pd


def aggregate_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates daily stock prices into monthly OHLC values.
    """

    monthly_df = (
        df
        .groupby(
            ["ticker", pd.Grouper(key="date", freq="ME")]
        )
        .agg(
            open=("open", "first"),
            close=("close", "last"),
            high=("high", "max"),
            low=("low", "min"),
            volume=("volume", "sum")
        )
        .reset_index()
    )

    return monthly_df
