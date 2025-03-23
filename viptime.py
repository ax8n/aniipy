import requests
import csv
import webbrowser
import sys
import time
from datetime import datetime

# 🔹 ANSI Color Codes
BOLD_YELLOW = "\033[1;93m"
BOLD_GREEN = "\033[1;92m"
BOLD_RED = "\033[1;91m"

# 🔹 CSV File Link (GitHub)
CSV_URL = "https://raw.githubusercontent.com/ax8n/aniipy/refs/heads/main/expire_list.csv"

# 🔹 Typewriter Effect Function
def combo(s, color="", delay=0.03, end="\n"):
    sys.stdout.write("\n")  
    for char in s:
        sys.stdout.write(color + char + '\033[0m')
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)

# 🔹 Fetch CSV File
def fetch_csv(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        combo("➜ Error fetching CSV: " + str(e), BOLD_RED)
        return None

# 🔹 Check Expiry (Only Remaining Time)
def check_expiry(user_id, csv_data):
    reader = csv.reader(csv_data.splitlines())
    next(reader)

    user_found = False
    expiry_date = None

    for row in reader:
        if row[0] == user_id:
            user_found = True
            try:
                expiry_date = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                combo("➜ Error: Invalid date format in CSV!", BOLD_RED)
                return

            current_time = datetime.now()
            expiry_timestamp = time.mktime(expiry_date.timetuple())
            current_timestamp = time.mktime(current_time.timetuple())

            if current_timestamp > expiry_timestamp:
                combo("➜ Your access has expired! Please contact the developer for more time.", BOLD_RED)
                combo("➜ Contact: @AniiRo", BOLD_GREEN)
                webbrowser.open("https://t.me/AniiRo")
                exit()
            else:
                remaining_time = expiry_timestamp - current_timestamp
                days = int(remaining_time // 86400)
                hours = int((remaining_time % 86400) // 3600)
                minutes = int((remaining_time % 3600) // 60)
                seconds = int(remaining_time % 60)

                formatted_remaining = f"{days} days, {hours:02d}:{minutes:02d}:{seconds:02d}"

                combo("\n⏳ Remaining Time: ", BOLD_YELLOW, delay=0.03, end="")
                combo(formatted_remaining, BOLD_GREEN, delay=0.03)
            return

    if not user_found:
        combo("➜ Access denied! You must purchase the tool first before continuing.", BOLD_RED)
        combo("➜ Contact: @AniiRo", BOLD_GREEN)
        webbrowser.open("https://t.me/AniiRo")
        exit()

# 🔹 Fetch User ID from External Variable
USER_ID = str(ID)  # ✅ Tumhari original script jaisa

csv_content = fetch_csv(CSV_URL)
if csv_content:
    check_expiry(USER_ID, csv_content)
