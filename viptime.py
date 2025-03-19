import requests
import csv
import webbrowser
import sys
import time
from datetime import datetime

# ANSI Color Codes
BOLD_YELLOW = "\033[1;93m"
BOLD_GREEN = "\033[1;92m"
BOLD_RED = "\033[1;91m"

CSV_URL = "https://raw.githubusercontent.com/ax8n/aniipy/refs/heads/main/expire_list.csv"
USER_ID = str(ID)  

# Typewriter effect function with extra newline
def combo(s, color="", delay=0.05, end="\n"):
    """Prints text character by character with color and delay for a typing effect."""
    sys.stdout.write("\n")  # This ensures the text starts from the second line
    for char in s:
        sys.stdout.write(color + char + '\033[0m')
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)

def fetch_csv(url):
    """Fetches CSV data from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text
    except requests.exceptions.RequestException as e:
        combo("➜ Error fetching CSV: " + str(e), BOLD_RED)
        return None

def check_expiry(user_id, csv_data):
    """Checks if the user ID is in the CSV and verifies expiry status."""
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
            if current_time > expiry_date:
                combo("➜ Your access has expired! Please contact the developer for more time.", BOLD_RED)
                combo("➜ Contact: @AniiRo", BOLD_GREEN)
                webbrowser.open("https://t.mAniiRo")
                exit()
            else:
                remaining_time = expiry_date - current_time
                combo("➜ Your access remains valid till •    ", BOLD_YELLOW, delay=0.03, end="")
                combo(str(remaining_time), BOLD_GREEN, delay=0.03)
            return

    if not user_found:
        combo("➜ Access denied! You must purchase the file first before continuing.", BOLD_RED)
        combo("➜ Contact: @AniiRo", BOLD_GREEN)
        webbrowser.open("https://t.me/AniiRo")
        exit()

csv_content = fetch_csv(CSV_URL)
if csv_content:
    check_expiry(USER_ID, csv_content)