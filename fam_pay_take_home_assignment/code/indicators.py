import pandas as pd


def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates SMA and EMA indicators based on monthly closing prices.
    """

    df = df.sort_values(by=["ticker", "date"])

    df["sma_10"] = df.groupby("ticker")["close"].rolling(window=10).mean().reset_index(0, drop=True)
    df["sma_20"] = df.groupby("ticker")["close"].rolling(window=20).mean().reset_index(0, drop=True)

    df["ema_10"] = df.groupby("ticker")["close"].ewm(span=10, adjust=False).mean().reset_index(0, drop=True)
    df["ema_20"] = df.groupby("ticker")["close"].ewm(span=20, adjust=False).mean().reset_index(0, drop=True)

    return df
