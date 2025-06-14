import asyncio
import logging

import aiohttp

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, token: str, chat_id: str) -> None:
        self.base_url = f"https://api.telegram.org/bot{token}/sendMessage"
        self.chat_id = chat_id

    async def send(self, message: str) -> None:
        async with aiohttp.ClientSession() as session:
            payload = {"chat_id": self.chat_id, "text": message}
            try:
                async with session.post(self.base_url, data=payload) as resp:
                    if resp.status != 200:
                        logger.error("Telegram notification failed: %s", await resp.text())
            except Exception as exc:  # pragma: no cover - network
                logger.error("Telegram error: %s", exc)


__all__ = ["TelegramNotifier"]
