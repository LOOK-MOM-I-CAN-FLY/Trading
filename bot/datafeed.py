import asyncio
import logging
from abc import ABC, abstractmethod
from typing import AsyncIterator

import ccxt.async_support as ccxt


logger = logging.getLogger(__name__)


class DataFeed(ABC):
    @abstractmethod
    async def subscribe(self, symbol: str) -> AsyncIterator[dict]:
        """Yield ticker data indefinitely."""
        pass

    @abstractmethod
    async def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int) -> list:
        """Fetch OHLCV data for the given symbol."""
        pass


class CCXTDataFeed(DataFeed):
    def __init__(self, exchange: str) -> None:
        self.exchange = getattr(ccxt, exchange)()

    async def subscribe(self, symbol: str) -> AsyncIterator[dict]:
        while True:
            try:
                ticker = await self.exchange.fetch_ticker(symbol)
                yield ticker
                await asyncio.sleep(1)
            except Exception as exc:  # pragma: no cover - network
                logger.error("Data feed error: %s", exc)
                await asyncio.sleep(5)

    async def fetch_ohlcv(
        self, symbol: str, timeframe: str = "1m", limit: int = 100
    ) -> list:
        """Return historical OHLCV data."""
        try:
            return await self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        except Exception as exc:  # pragma: no cover - network
            logger.error("OHLCV fetch error: %s", exc)
            return []


__all__ = ["DataFeed", "CCXTDataFeed"]
