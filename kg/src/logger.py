
def color_print(text: str, color: str = "blue") -> None:
    colors = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
    }
    print(f"{colors.get(color, '\033[34m')}{text}\033[0m")
