import logging
from typing import Callable

import pandas as pd


logger = logging.getLogger(__name__)


class Backtester:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def run(self, strategy_factory: Callable[[str], "Strategy"], symbol: str) -> None:
        strategy = strategy_factory(symbol)
        for i in range(50, len(self.data)):
            df_slice = self.data.iloc[: i + 1]
            for signal in strategy.generate(df_slice):
                logger.info("Backtest signal: %s", signal)


__all__ = ["Backtester"]
