import os
import time
import sys
import webbrowser

RED_GRADIENT = [
    "\033[38;2;80;0;0m",
    "\033[38;2;110;0;0m",
    "\033[38;2;140;0;0m",
    "\033[38;2;170;0;0m",
    "\033[38;2;200;0;0m",
    "\033[38;2;220;20;20m",
    "\033[38;2;240;40;40m",
    "\033[38;2;255;60;60m",
    "\033[38;2;255;90;90m"
]
PURPLE = "\033[38;2;128;0;128m"
RESET = "\033[0m"

ascii_logo = r"""
▒███████▒ ▄▄▄██▀▀▀▓██   ██▓ ▄▄▄      
▒ ▒ ▒ ▄▀░   ▒██    ▒██  ██▒▒████▄    
░ ▒ ▄▀▒░    ░██     ▒██ ██░▒██  ▀█▄  
  ▄▀▒   ░▓██▄██▓    ░ ▐██▓░░██▄▄▄▄██ 
▒███████▒ ▓███▒     ░ ██▒▓░ ▓█   ▓██▒
░▒▒ ▓░▒░▒ ▒▓▒▒░      ██▒▒▒  ▒▒   ▓▒█░
░░▒ ▒ ░ ▒ ▒ ░▒░    ▓██ ░▒░   ▒   ▒▒ ░
░ ░ ░ ░ ░ ░ ░ ░    ▒ ▒ ░░    ░   ▒   
  ░ ░     ░   ░    ░ ░           ░  ░
░   
"""

lines = [
    "Select an option:",
    "[1] Checker",
    "[2] Login by Cookie",
    "[0] Exit",
    "Enter option number: ",
    "Invalid selection."
]

cookie_instructions = [
    "1. Ensure you are logged in to Roblox on your browser.",
    "2. Install Cookie-Editor from the Chrome Web Store.",
    "3. Go to Extensions > Manage Extensions in Chrome.",
    "4. Enable 'Allow access to file URLs' for Cookie-Editor.",
    "5. Visit https://www.roblox.com/pl/users/147675/profile in the opened tab.",
    "6. Open Cookie-Editor, find '.ROBLOSECURITY' cookie.",
    "7. Paste your new cookie value and ensure it is valid (you can use our checker).",
    "8. Save the cookie in Cookie-Editor."
]

def main_menu():
    print(RED_GRADIENT[0] + ascii_logo + RESET)
    print(RED_GRADIENT[1] + lines[0] + RESET)
    print(RED_GRADIENT[3] + lines[1] + RESET)
    print(RED_GRADIENT[5] + lines[2] + RESET)
    print(RED_GRADIENT[7] + lines[3] + RESET)

def show_cookie_instructions():
    print(PURPLE + "\nFollow these steps to set the cookie:" + RESET)
    for i, instruction in enumerate(cookie_instructions, 1):
        print(PURPLE + f"Step {i}: {instruction}" + RESET)

def main():
    while True:
        try:
            main_menu()
            print(RED_GRADIENT[6] + lines[4], end='', flush=True)
            choice = input()
            print(RESET, end='')
            if choice == "1":
                os.system("start cmd /k python scripts/checker.py")
                sys.exit()
            elif choice == "2":
                webbrowser.open("https://www.roblox.com/pl/users/147675/profile")
                webbrowser.open("https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm")
                show_cookie_instructions()
                print(PURPLE + "\nWaiting 5 minutes before closing..." + RESET)
                spinner = ['/', '-', '\\', '|']
                for _ in range(300):
                    for spin in spinner:
                        print(PURPLE + f"\rTime left: {300 - _}s {spin} " + RESET, end='', flush=True)
                        time.sleep(0.25)
                print()
                sys.exit()
            elif choice == "0":
                spinner = ['/', '-', '\\', '|']
                for i in range(3, 0, -1):
                    for spin in spinner:
                        print(RED_GRADIENT[8] + f"\rExit in {i} {spin} " + RESET, end='', flush=True)
                        time.sleep(0.25)
                print()
                sys.exit()
            else:
                print(RED_GRADIENT[8] + lines[5] + RESET)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
