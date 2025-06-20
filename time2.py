import os, requests
from requests import get
import sys
import time
import webbrowser
from datetime import datetime
EXPIRE_TIME = '2024-06-24 20:50:20'
EXPIRE_MSG = '\033[38;5;167m- This tool has been stopped by the developer.'

def check_expiration():
    current_time = datetime.now()
    expiration_time = datetime.strptime(EXPIRE_TIME, '%Y-%m-%d %H:%M:%S')
    if current_time > expiration_time:
        print(EXPIRE_MSG)
        sys.exit(1)
check_expiration()
