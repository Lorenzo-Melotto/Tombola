import os
import colorama
from colorama import Fore
colorama.init(autoreset=True)

def getRainbowString(text: str) -> str:
    """Returns a string formatted to be displayed with rainbow colors letter by letter"""
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX]
    s = ""
    for i,l in enumerate(text):
        s+= f"{colors[i%len(colors)]}{l}"
    return s + f"{Fore.RESET}"

def getMultilineRainbowString(multiLineText: str) -> str:
    """Returns a string formatted to be displayed with rainbow colors line by line"""
    # if is not multiline return the string unchanged
    if "\n" not in multiLineText: return multiLineText
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX]
    newString = ""
    lines = multiLineText.split("\n")
    for i, l in enumerate(lines):
        if l != "": newString += f"{colors[i%len(colors)]}{l}\n"
        else: newString += l
    return newString

def clearScreen() -> None:
    """Clears the terminal"""
    os.system("cls" if os.name=="nt" else "clear")