# Trading Bot

This repository contains an example of a modular cryptocurrency trading bot written in Python 3.11. It is tuned for scalping on 1–5 minute charts and supports asynchronous data feeds via CCXT, indicator calculations, risk management, order execution, Telegram notifications and a CLI interface.

The code is organized in the `bot` package with the following modules and focuses on scalping strategies for very small timeframes:

- `settings.py` – load configuration and API keys from YAML/JSON and environment variables.
- `datafeed.py` – asynchronous market data using CCXT.
- `indicators.py` – indicator helpers based on pandas-ta.
- `strategy.py` – strategy base class and an EMA-based scalping strategy tuned for 1–5 minute charts.
- `risk.py` – position sizing based on fixed risk per trade.
- `execution.py` – order execution layer using CCXT.
- `notifier.py` – Telegram notification helper.
- `backtest.py` – very lightweight backtesting skeleton.
- `main.py` – CLI with commands `init-project`, `backtest`, `run-live`, `report`.

Install dependencies and run `python -m bot.main --help` for usage information.
