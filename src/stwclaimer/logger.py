from rich.console import Console
from datetime import datetime


class Logger:
    def __init__(self, show_date_time: bool, display_colors: bool):
        self.show_date_time = show_date_time

        self.console = Console(no_color=not display_colors)

    def onrep_show_date_time(self, show_date_time: bool) -> None:
        self.show_date_time = show_date_time

    def onrep_display_colors(self, display_colors: bool) -> None:
        self.console.no_color = not display_colors

    def message(
        self, text: str = "", end: str = "\n", hide_date_time: bool = False
    ) -> None:
        if self.show_date_time and not hide_date_time:
            date = datetime.now().strftime("[%Y/%m/%d %H:%M:%S]")
            lines = [
                f"{date} {line}" if line.strip() else line for line in text.split("\n")
            ]
            text = "\n".join(lines)

        self.console.print(text, end=end)
