import os
from pathlib import Path
from colorama import Fore, Style, init
import pyfiglet
import tkinter as tk
from tkinter import filedialog
import core

init(autoreset=True)

RISK_COLOR = {"HIGH": Fore.RED, "MEDIUM": Fore.YELLOW, "LOW": Fore.GREEN}


def clear():
    os.system("clear")


def banner():
    clear()
    print(Fore.CYAN + pyfiglet.figlet_format("MetaCheck", font="slant"))
    print(Fore.CYAN + "=" * 60)
    print(Fore.WHITE + " Metadata Privacy Checker" + Fore.GREEN + "  v1.0")
    print(Fore.WHITE + " Author : " + Fore.YELLOW + "nikhileshk0375-hash")
    print(Fore.WHITE + " Github : " + Fore.YELLOW + "github.com/nikhileshk0375-hash/metadata-checker")
    print(Fore.CYAN + "=" * 60 + "\n")


def menu():
    print(Fore.GREEN + " [1] " + Fore.WHITE + "Check a single file")
    print(Fore.GREEN + " [2] " + Fore.WHITE + "Check all files in a folder")
    print(Fore.GREEN + " [3] " + Fore.WHITE + "Clean a file (remove metadata)")
    print(Fore.GREEN + " [0] " + Fore.WHITE + "Exit")
    print(Fore.CYAN + "-" * 60)


def pick_folder():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    folder = filedialog.askdirectory(title="Select a folder to scan")
    root.destroy()
    return folder


def pick_file():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Supported files", "*.jpg *.jpeg *.pdf *.docx")])
    root.destroy()
    return path


def show_result(path, result):
    level = result["risk"]
    color = RISK_COLOR[level]
    print(f"\n{Fore.CYAN}File: {Fore.WHITE}{path}")
    print(f"{color}{Style.BRIGHT}RISK: {level}{Style.RESET_ALL}  {Fore.WHITE}({result['reasons'][0]})")
    if result["fields"]:
        for name, value in result["fields"]:
            print(f"  {Fore.YELLOW}{name}: {Fore.WHITE}{value}")
    else:
        print(f"  {Fore.GREEN}No metadata found. Looks clean!")


def check_single():
    print(Fore.CYAN + "\nOpening file picker... (check your taskbar if it doesn't appear)")
    path = pick_file()
    if not path:
        print(Fore.YELLOW + "No file selected.")
        return
    if not Path(path).exists():
        print(Fore.RED + "File not found.")
        return
    try:
        result = core.analyze(path)
        show_result(path, result)
    except Exception as e:
        print(Fore.RED + f"Error: {e}")


def check_folder():
    print(Fore.CYAN + "\nOpening folder picker... (check your taskbar if it doesn't appear)")
    folder = pick_folder()
    if not folder:
        print(Fore.YELLOW + "No folder selected.")
        return
    p = Path(folder)
    if not p.is_dir():
        print(Fore.RED + "Folder not found.")
        return
    files = [f for f in sorted(p.iterdir())
             if f.suffix.lower() in core.SUPPORTED and "_clean" not in f.stem]
    if not files:
        print(Fore.YELLOW + "No supported files found.")
        return
    for f in files:
        try:
            show_result(f.name, core.analyze(f))
        except Exception as e:
            print(Fore.RED + f"{f.name}: {e}")


def clean_file():
    print(Fore.CYAN + "\nOpening file picker... (check your taskbar if it doesn't appear)")
    path = pick_file()
    if not path:
        print(Fore.YELLOW + "No file selected.")
        return
    if not Path(path).exists():
        print(Fore.RED + "File not found.")
        return
    try:
        out = core.clean(path)
        print(Fore.GREEN + f"\nCleaned copy saved as: {out}")
        show_result(out, core.analyze(out))
    except Exception as e:
        print(Fore.RED + f"Error: {e}")


def main():
    actions = {"1": check_single, "2": check_folder, "3": clean_file}
    while True:
        banner()
        menu()
        choice = input(Fore.CYAN + " Select an option: " + Fore.WHITE).strip()
        if choice == "0":
            print(Fore.CYAN + "\nGoodbye!\n")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print(Fore.RED + "Invalid option.")
        input(Fore.CYAN + "\nPress Enter to continue...")


main()
