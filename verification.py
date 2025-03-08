import requests
import sys
import time
import webbrowser

# Telegram Bot Token and Channel Username
BOT_TOKEN = "7680543388:AAGrvEshVkfSuFiyh9MB5SxjBIMooZRgehM"
CHANNEL_USERNAME = "@aniisolo"

# Use a session for faster requests
session = requests.Session()

def is_member(user_id):
    """Check if the user is a member of the Telegram channel."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={CHANNEL_USERNAME}&user_id={user_id}"
    
    try:
        response = session.get(url, timeout=3)  # Timeout set to 3 seconds
        data = response.json()
        if data.get("ok") and data.get("result", {}).get("status") in ["member", "administrator", "creator"]:
            return True
    except requests.exceptions.RequestException:
        print(f"{red}➜ Network error! Please check your connection.")
        time.sleep(2)
        sys.exit()
    
    return False

def verify_user():
    """Runs verification before executing the script."""
    global ID  # Global variable to store chat ID
    try:
        ID = int(input(f"{white}➜ {cyan} 𝐂𝐇𝐀𝐓 𝐈𝐃 •   {red} "))
    except ValueError:
        print(f"{red}➜ STUPID ASS ENTER YOUR ID THERE 🗿🖕🏻  ")
        time.sleep(2)
        sys.exit()

    if not is_member(ID):
        print("➜ Access denied! Join @aniisolo to use this file. ")
        time.sleep(2)
        webbrowser.open("https://t.me/aniisolo")
        sys.exit()

    time.sleep(1)  # Short delay before continuing execution

# Run verification
verify_user()