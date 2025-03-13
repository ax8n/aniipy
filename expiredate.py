import sys
import time
import os

# Typewriter effect function with color support
def combo(s, color="", delay=1. / 200, end=""):
    for char in s:
        sys.stdout.write(color + char + '\033[0m')  # Reset color after each char
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)  # Custom end character (default empty)

# ANSI Color Codes
BOLD_YELLOW = "\033[1;93m"
BOLD_GREEN = "\033[1;92m"
BOLD_RED = "\033[1;91m"

# 🔹 Set Expiry Date & Time
EXPIRY_TIME = "2025-03-14 11:59:59"  # Format: "YYYY-MM-DD HH:MM:SS"

# Convert expiry time to UNIX timestamp
expiry_date = time.mktime(time.strptime(EXPIRY_TIME, "%Y-%m-%d %H:%M:%S"))

# Get the current time
current_time = time.mktime(time.localtime())

# Check if expired
if current_time > expiry_date:
    combo("\n[!] This file has expired. Please contact the dev; @AniiRo", BOLD_RED)
    exit()  # 🔹 Script yahi exit kar jayegi

# Expiry valid, show expiry time in one line
combo("\n➜ Expiry Time: ", BOLD_YELLOW, delay=0.03, end="")  # Yellow text, no newline
combo(  EXPIRY_TIME, BOLD_GREEN, delay=0.03, end="\n")  # Green text, newline at the end
