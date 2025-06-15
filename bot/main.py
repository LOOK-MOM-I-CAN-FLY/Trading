import asyncio
import logging
from pathlib import Path

import pandas as pd
import typer

from .backtest import Backtester
from .datafeed import CCXTDataFeed
from .execution import CCXTExecution
from .notifier import TelegramNotifier
from .risk import PositionSizing
from .settings import load_settings
from .strategy import EMARsiStrategy, EMAScalpingStrategy, Signal


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def init_project(config_path: Path = Path("config.yml")) -> None:
    if not config_path.exists():
        config_path.write_text("exchange:\n  name: binance\ntrading_pairs:\n  - BTC/USDT\n")
        typer.echo(f"Created default config at {config_path}")
    else:
        typer.echo("Config already exists")


@app.command()
def backtest(config: Path = Path("config.yml")) -> None:
    settings = load_settings(config)
    df = pd.DataFrame()  # placeholder: load your historical data here
    backtester = Backtester(df)
    backtester.run(lambda s: EMAScalpingStrategy(s), settings.trading_pairs[0])


@app.command()
def run_live(config: Path = Path("config.yml")) -> None:
    settings = load_settings(config)
    feed = CCXTDataFeed(settings.exchange.name)
    exec_client = CCXTExecution(settings.exchange.name, settings.exchange.api_key, settings.exchange.api_secret)
    notifier = None
    if settings.telegram_token and settings.telegram_chat_id:
        notifier = TelegramNotifier(settings.telegram_token, settings.telegram_chat_id)

    position = PositionSizing(balance=100.0, risk_per_trade=settings.risk_per_trade, leverage=settings.leverage)

    async def run() -> None:
        async for data in feed.subscribe(settings.trading_pairs[0]):
            df = pd.DataFrame([data])
            strategy = EMAScalpingStrategy(settings.trading_pairs[0])
            for signal in strategy.generate(df):
                size = position.calculate_size(stop_distance=10)
                await exec_client.create_order(signal.symbol, signal.side, size)
                if notifier:
                    await notifier.send(f"{signal.side} {signal.symbol} at {signal.price}")
    asyncio.run(run())


@app.command()
def report() -> None:
    typer.echo("Reporting is not implemented yet")


if __name__ == "__main__":
    app()
