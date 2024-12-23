import os

class Printer:
    COLORS = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }

    def __init__(self, file_name: str):
        self.file_name = os.path.basename(file_name)

    def _log(self, color: str, *args, sep=" ", end="\n"):
        color_code = self.COLORS.get(color, self.COLORS["reset"])
        message = sep.join(map(str, args))  # Convert all arguments to strings and join them
        print(f"{color_code}[{self.file_name}] {message}{self.COLORS['reset']}", end=end)

    def red(self, *args, sep=" ", end="\n"):
        self._log("red", *args, sep=sep, end=end)

    def green(self, *args, sep=" ", end="\n"):
        self._log("green", *args, sep=sep, end=end)

    def yellow(self, *args, sep=" ", end="\n"):
        self._log("yellow", *args, sep=sep, end=end)

    def blue(self, *args, sep=" ", end="\n"):
        self._log("blue", *args, sep=sep, end=end)

    def magenta(self, *args, sep=" ", end="\n"):
        self._log("magenta", *args, sep=sep, end=end)

    def cyan(self, *args, sep=" ", end="\n"):
        self._log("cyan", *args, sep=sep, end=end)

    def white(self, *args, sep=" ", end="\n"):
        self._log("white", *args, sep=sep, end=end)

    def custom(self, color_code: str, *args, sep=" ", end="\n"):
        """Prints a message with a custom ANSI color code."""
        message = sep.join(map(str, args))  # Convert all arguments to strings and join them
        print(f"{color_code}[{self.file_name}] {message}{self.COLORS['reset']}", end=end)


