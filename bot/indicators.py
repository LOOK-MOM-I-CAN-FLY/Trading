import pandas as pd
import numpy as np

# pandas_ta on NumPy >=2 requires NaN constant
if not hasattr(np, "NaN"):  # pragma: no cover - compatibility
    np.NaN = np.nan

import pandas_ta as ta


def ema(series: pd.Series, length: int = 20) -> pd.Series:
    return ta.ema(series, length=length)


def rsi(series: pd.Series, length: int = 14) -> pd.Series:
    return ta.rsi(series, length=length)


def supertrend(df: pd.DataFrame, length: int = 10, multiplier: float = 3.0) -> pd.DataFrame:
    st = ta.supertrend(high=df["high"], low=df["low"], close=df["close"],
                       length=length, multiplier=multiplier)
    return st


__all__ = ["ema", "rsi", "supertrend"]
