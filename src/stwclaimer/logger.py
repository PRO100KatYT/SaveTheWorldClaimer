from rich.console import Console
from datetime import datetime


class Logger:
    def __init__(self, show_date_time: bool, colorful_display: bool):
        self.show_date_time = show_date_time

        self.console = Console(no_color=not colorful_display)

    def onrep_show_date_time(self, show_date_time: bool) -> None:
        self.show_date_time = show_date_time

    def onrep_colorful_display(self, colorful_display: bool) -> None:
        self.console.no_color = not colorful_display

    def message(self, text: str) -> None:
        if self.show_date_time:
            date = datetime.now().strftime("[%Y/%m/%d %H:%M:%S]")
            lines = [
                f"{date} {line}" if line.strip() else line for line in text.split("\n")
            ]
            text = "\n".join(lines)

        self.console.print(text)
