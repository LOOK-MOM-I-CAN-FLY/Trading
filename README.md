# Trading Bot

This repository contains a minimal yet extendable cryptocurrency trading bot written in **Python&nbsp;3.11+**.  It focuses on scalping strategies for 1–5&nbsp;minute timeframes and includes all the building blocks required to send trade signals via Telegram or execute them through a connected exchange.

## Installation

1. Clone the repository and create a virtual environment:

   ```bash
   git clone https://example.com/trading-bot.git
   cd trading-bot
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `config.example.yml` to `config.yml` and fill in your API keys and Telegram chat details. Environment variables from a `.env` file override the values in the config.

4. Display the available CLI commands:

   ```bash
   python -m bot.main --help
   ```

Use `python -m bot.main run-live` to start streaming data and receive signals in Telegram. Run `python -m bot.main backtest` once you have prepared historical data for analysis.

## Disclaimer

This project is provided for educational purposes only. Trading cryptocurrencies involves significant risk, and you remain solely responsible for any financial decisions made when using this code.

The code is organized in the `bot` package with the following modules:

- `settings.py` – load configuration and API keys from YAML/JSON and environment variables.
- `datafeed.py` – asynchronous market data using CCXT.
- `indicators.py` – indicator helpers based on pandas-ta.
- `strategy.py` – strategy base class and an EMA+RSI example strategy.
- `risk.py` – position sizing based on fixed risk per trade.
- `execution.py` – order execution layer using CCXT.
- `notifier.py` – Telegram notification helper.
- `backtest.py` – very lightweight backtesting skeleton.
- `main.py` – CLI with commands `init-project`, `backtest`, `run-live`, `report`.

Install dependencies and run `python -m bot.main --help` for usage information.
