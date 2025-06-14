from dataclasses import dataclass
from pathlib import Path
import json
import yaml
import os
from typing import Any, Dict
from dotenv import load_dotenv


@dataclass
class ExchangeConfig:
    name: str
    api_key: str
    api_secret: str
    passphrase: str | None = None


@dataclass
class Settings:
    exchange: ExchangeConfig
    trading_pairs: list[str]
    risk_per_trade: float = 0.02
    leverage: int = 1
    telegram_token: str | None = None
    telegram_chat_id: str | None = None


CONFIG_PATH = Path("config.yml")


def load_settings(path: Path = CONFIG_PATH) -> Settings:
    load_dotenv()
    data: Dict[str, Any]
    if path.suffix in {".yml", ".yaml"}:
        data = yaml.safe_load(path.read_text())
    else:
        data = json.loads(path.read_text())

    exchange = data.get("exchange", {})
    exchange_config = ExchangeConfig(
        name=exchange.get("name", "binance"),
        api_key=os.getenv("API_KEY", exchange.get("api_key", "")),
        api_secret=os.getenv("API_SECRET", exchange.get("api_secret", "")),
        passphrase=os.getenv("PASSPHRASE", exchange.get("passphrase")),
    )

    settings = Settings(
        exchange=exchange_config,
        trading_pairs=data.get("trading_pairs", ["BTC/USDT"]),
        risk_per_trade=float(data.get("risk_per_trade", 0.02)),
        leverage=int(data.get("leverage", 1)),
        telegram_token=os.getenv("TG_TOKEN", data.get("telegram_token")),
        telegram_chat_id=os.getenv("TG_CHAT_ID", data.get("telegram_chat_id")),
    )
    return settings


__all__ = ["Settings", "load_settings"]
