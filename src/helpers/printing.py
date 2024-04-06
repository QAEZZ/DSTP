import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def notice(header: str, notice: str) -> None:
    print(f"{Style.BRIGHT}{header}:{Style.RESET_ALL} {notice}")

def prompt(to_prompt: str) -> str:
    return input(f"{Style.BRIGHT}{to_prompt}:{Style.RESET_ALL} ")

def message(message: str) -> None:
    print(f"{Fore.MAGENTA}{message}")

