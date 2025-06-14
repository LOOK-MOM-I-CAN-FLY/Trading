import logging
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class PositionSizing:
    balance: float
    risk_per_trade: float
    leverage: int

    def calculate_size(self, stop_distance: float) -> float:
        if stop_distance <= 0:
            raise ValueError("Stop distance must be positive")
        risk_amount = self.balance * self.risk_per_trade
        size = (risk_amount * self.leverage) / stop_distance
        logger.debug("Calculated position size: %s", size)
        return size


__all__ = ["PositionSizing"]
