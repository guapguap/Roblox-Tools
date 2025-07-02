from requests import get, post
from datetime import datetime, timezone
from time import time as __, sleep as zzz
from re import findall
import json
import os
from dotenv import load_dotenv

# Find Desktop directory and locate Roblox Tools/edit file in this folder/.env
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
WEBHOOK_URL = os.getenv("WEBHOOK_URL_CHECKER")

def log(text, sleep=None):
    print(f"[{datetime.fromtimestamp(__(), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}] → {text}")
    if sleep: zzz(sleep)

def send_webhook(embed):
    if not WEBHOOK_URL:
        log("Error: WEBHOOK_URL_CHECKER not set in .env file")
        return
    # Ensure all embed values are properly formatted
    if 'description' not in embed:
        embed['description'] = ""
    
    # Clean all field values
    if 'fields' in embed:
        for field in embed['fields']:
            if not isinstance(field['value'], str):
                field['value'] = str(field['value'])
            if len(field['value']) > 1024:
                field['value'] = field['value'][:1021] + "..."
    
    # Prepare the payload with additional webhook info
    payload = {
        "username": "Roblox Account Checker",
        "avatar_url": "https://www.roblox.com/favicon.ico",
        "embeds": [embed]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)
        log(f"Webhook sent, status: {response.status_code}")
        if response.status_code != 204:
            log(f"Webhook failed: {response.text}")
    except Exception as e:
        log(f"Webhook error: {str(e)}")

def safe_str(value, default="None", max_len=1024):
    """Convert None or empty to default, truncate to max_len chars, and convert to string."""
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return default
    s = str(value)
    if len(s) > max_len:
        s = s[:max_len - 3] + "..."
    return s

def main():
    cookie = input("Enter Roblox cookie: ").strip()
    if not cookie:
        log("No cookie provided.")
        return

    log("Checking cookie...")
    response = get('https://users.roblox.com/v1/users/authenticated', cookies={'.ROBLOSECURITY': cookie})

    if '"id":' not in response.text:
        if 'Unauthorized' in response.text:
            log("Invalid cookie.")
            embed = {
                "title": ":x: Invalid Cookie",
                "description": "The provided cookie is invalid or expired",
                "color": 0xFF0000,
                "fields": [{"name": "Passed Cookie:", "value": "```Hidden```", "inline": False}]
            }
            send_webhook(embed)
            return
        else:
            log("Roblox returned a bad response.")
            embed = {
                "title": ":x: Error",
                "description": "Roblox API returned an unexpected response",
                "color": 0xFFFF00,
                "fields": [{"name": "Error:", "value": f"```{safe_str(response.text)}```", "inline": False}]
            }
            send_webhook(embed)
            return

    log("Valid cookie detected.")
    user_id = response.json()['id']
    robux = get(f'https://economy.roblox.com/v1/users/{user_id}/currency', cookies={'.ROBLOSECURITY': cookie}).json()['robux']
    balance_credit_info = get(f'https://billing.roblox.com/v1/credit', cookies={'.ROBLOSECURITY': cookie}).json()
    balance_credit = balance_credit_info.get('balance', 0)
    balance_credit_currency = balance_credit_info.get('currencyCode', '')

    account_settings_json = get(f'https://www.roblox.com/my/settings/json', cookies={'.ROBLOSECURITY': cookie}).json()
    account_name = safe_str(account_settings_json.get('Name'), default="Unknown")
    account_display_name = safe_str(account_settings_json.get('DisplayName'), default="Unknown")
    account_email_verified_bool = account_settings_json.get('IsEmailVerified', False)
    if account_email_verified_bool:
        email = account_settings_json.get("UserEmail", "Unknown")
        account_email_verified = f"True (`{email}`)"
    else:
        account_email_verified = "False"
    account_above_13 = account_settings_json.get('UserAbove13', False)
    account_age_in_years = round(float(account_settings_json.get('AccountAgeInDays', 0) / 365), 2)
    account_has_premium = account_settings_json.get('IsPremium', False)
    account_has_pin = account_settings_json.get('IsAccountPinEnabled', False)
    account_2step = account_settings_json.get('MyAccountSecurityModel', {}).get('IsTwoStepEnabled', False)

    account_friends = get('https://friends.roblox.com/v1/my/friends/count', cookies={'.ROBLOSECURITY': cookie}).json().get('count', 0)
    account_voice_verified = get('https://voice.roblox.com/v1/settings', cookies={'.ROBLOSECURITY': cookie}).json().get('isVerifiedForVoice', False)

    account_gamepasses_resp = get(f'https://www.roblox.com/users/inventory/list-json?assetTypeId=34&cursor=&itemsPerPage=100&pageNumber=1&userId={user_id}', cookies={'.ROBLOSECURITY': cookie})
    check = findall(r'"PriceInRobux":(.*?),', account_gamepasses_resp.text)
    account_gamepasses_value = sum([int(match) if match != "null" else 0 for match in check])
    account_gamepasses = f"{account_gamepasses_value} R$"

    badges_resp = get(f'https://accountinformation.roblox.com/v1/users/{user_id}/roblox-badges', cookies={'.ROBLOSECURITY': cookie}).text
    badges_list = findall(r'"name":"(.*?)"', badges_resp)
    account_badges = ', '.join(badges_list) if badges_list else "None"
    account_badges = safe_str(account_badges)

    account_transactions = get(f'https://economy.roblox.com/v2/users/{user_id}/transaction-totals?timeFrame=Year&transactionType=summary', cookies={'.ROBLOSECURITY': cookie}).json()
    account_sales_of_goods = safe_str(account_transactions.get('salesTotal', '0'))
    account_purchases_total = abs(int(account_transactions.get('purchasesTotal', 0)))
    account_commissions = safe_str(account_transactions.get('affiliateSalesTotal', '0'))
    account_robux_purchased = safe_str(account_transactions.get('currencyPurchasesTotal', '0'))
    account_premium_payouts_total = safe_str(account_transactions.get('premiumPayoutsTotal', '0'))
    account_pending_robux = safe_str(account_transactions.get('pendingRobuxTotal', '0'))

    avatar_thumb_url = get(f'https://thumbnails.roblox.com/v1/users/avatar-headshot?size=48x48&format=png&userIds={user_id}').json().get('data', [{}])[0].get('imageUrl', '')

    embed = {
        "title": ":white_check_mark: Valid Cookie",
        "description": f"Account information for {account_name}",
        "color": 0x38d13b,
        "thumbnail": {"url": avatar_thumb_url},
        "fields": [
            {"name": "Passed Cookie:", "value": "```Hidden```", "inline": False},
            {"name": ":money_mouth: Robux", "value": str(robux), "inline": True},
            {"name": ":moneybag: Balance", "value": f"{balance_credit} {balance_credit_currency}", "inline": True},
            {"name": ":bust_in_silhouette: Account Name", "value": f"{account_name} ({account_display_name})", "inline": True},
            {"name": ":email: Email Verified", "value": account_email_verified, "inline": True},
            {"name": ":calendar: Account Age", "value": f"{account_age_in_years} years", "inline": True},
            {"name": ":baby: Above 13", "value": str(account_above_13), "inline": True},
            {"name": ":star: Premium", "value": str(account_has_premium), "inline": True},
            {"name": ":key: Has PIN", "value": str(account_has_pin), "inline": True},
            {"name": ":lock: 2-Step Verification", "value": str(account_2step), "inline": True},
            {"name": ":busts_in_silhouette: Friends", "value": str(account_friends), "inline": True},
            {"name": ":microphone2: Voice Verified", "value": str(account_voice_verified), "inline": True},
            {"name": ":video_game: Gamepasses Worth", "value": account_gamepasses, "inline": True},
            {"name": ":medal: Badges", "value": account_badges, "inline": True},
            {"name": "**↻** Transactions", "value": "View transaction details below", "inline": False},
            {"name": ":coin: Sales of Goods", "value": str(account_sales_of_goods), "inline": True},
            {"name": "💰 Premium Payouts", "value": str(account_premium_payouts_total), "inline": True},
            {"name": "📈 Commissions", "value": str(account_commissions), "inline": True},
            {"name": ":credit_card: Robux purchased", "value": str(account_robux_purchased), "inline": True},
            {"name": "🚧 Pending", "value": str(account_pending_robux), "inline": True},
            {"name": ":money_with_wings: Overall", "value": str(account_purchases_total), "inline": True}
        ]
    }

    send_webhook(embed)
    log(f"Processed cookie. [Robux: {robux} | Balance: {balance_credit} {balance_credit_currency} | Name: {account_name} ({account_display_name}) | Age: {account_age_in_years} years | Friends: {account_friends} | Gamepasses: {account_gamepasses} | Badges: {account_badges} | Sales: {account_sales_of_goods} | Premium Payouts: {account_premium_payouts_total} | Commissions: {account_commissions} | Robux Purchased: {account_robux_purchased} | Pending: {account_pending_robux} | Overall: {account_purchases_total} | Voice Verified: {account_voice_verified} | PIN: {account_has_pin} | 2-Step: {account_2step} | Premium: {account_has_premium} | Above 13: {account_above_13} | Email: {account_email_verified}]")

if __name__ == "__main__":
    main()