from rich.console import Console
from datetime import datetime
import asyncio
import httpx


class Logger:
    def __init__(self, show_date_time: bool, webhook_url: str):
        self.show_date_time = show_date_time
        self.webhook_url = webhook_url

        self._webhooks_enabled = False

        self.webhook_queue = asyncio.Queue()
        self.webhook_session = httpx.AsyncClient()
        self.console = Console(highlight=False)

    def toggle_webhooks(self, enabled: bool) -> None:
        self._webhooks_enabled = enabled

    def onrep_show_date_time(self, show_date_time: bool) -> None:
        self.show_date_time = show_date_time

    def onrep_discord_webhook_url(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url

    def message(
        self,
        text: str = "",
        end: str = "\n",
        hide_date_time: bool = False,
        webhook_sendable: bool = False,
    ) -> None:
        if self.show_date_time and not hide_date_time:
            date = datetime.now().strftime("[%Y/%m/%d %H:%M:%S]")
            lines = [
                f"{date} {line}" if line.strip() else line for line in text.split("\n")
            ]
            text = "\n".join(lines)

        if self.webhook_url and self._webhooks_enabled:
            for line in text.split("\n"):
                self.webhook_queue.put_nowait(line)

        self.console.print(text, end=end)

    async def webhook_loop(self) -> None:
        while True:
            lines = []
            while not self.webhook_queue.empty():
                lines.append(self.webhook_queue.get_nowait())

            text = "\n".join(lines)

            if text:
                try:
                    await self.webhook_session.post(
                        self.webhook_url, json={"content": text}
                    )
                except:
                    pass

            await asyncio.sleep(0.7)
