import logging
from dataclasses import dataclass
from typing import Iterable

import pandas as pd

from .indicators import ema, rsi


logger = logging.getLogger(__name__)


@dataclass
class Signal:
    side: str  # "BUY" or "SELL"
    price: float
    symbol: str


class Strategy:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    def generate(self, df: pd.DataFrame) -> Iterable[Signal]:
        raise NotImplementedError


class EMARsiStrategy(Strategy):
    def __init__(self, symbol: str, ema_fast: int = 12, ema_slow: int = 26, rsi_len: int = 14) -> None:
        super().__init__(symbol)
        self.ema_fast = ema_fast
        self.ema_slow = ema_slow
        self.rsi_len = rsi_len

    def generate(self, df: pd.DataFrame) -> Iterable[Signal]:
        df = df.copy()
        df["ema_fast"] = ema(df["close"], self.ema_fast)
        df["ema_slow"] = ema(df["close"], self.ema_slow)
        df["rsi"] = rsi(df["close"], self.rsi_len)

        latest = df.iloc[-1]
        if latest["ema_fast"] > latest["ema_slow"] and latest["rsi"] < 70:
            logger.debug("Buy signal generated")
            yield Signal(side="BUY", price=float(latest["close"]), symbol=self.symbol)
        elif latest["ema_fast"] < latest["ema_slow"] and latest["rsi"] > 30:
            logger.debug("Sell signal generated")
            yield Signal(side="SELL", price=float(latest["close"]), symbol=self.symbol)



__all__ = ["Signal", "Strategy", "EMARsiStrategy"]
