import logging
from abc import ABC, abstractmethod

import ccxt.async_support as ccxt


logger = logging.getLogger(__name__)


class Execution(ABC):
    @abstractmethod
    async def create_order(self, symbol: str, side: str, amount: float, price: float | None = None) -> dict:
        pass


class CCXTExecution(Execution):
    def __init__(self, exchange: str, api_key: str, api_secret: str) -> None:
        exchange_class = getattr(ccxt, exchange)
        self.client = exchange_class({
            "apiKey": api_key,
            "secret": api_secret,
            "enableRateLimit": True,
        })

    async def create_order(self, symbol: str, side: str, amount: float, price: float | None = None) -> dict:
        try:
            order = await self.client.create_order(symbol, "market", side.lower(), amount, price)
            logger.info("Order created: %s", order)
            return order
        except Exception as exc:  # pragma: no cover - network
            logger.error("Order failed: %s", exc)
            raise


__all__ = ["Execution", "CCXTExecution"]
