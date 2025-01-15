import os
import time
import psutil  

# Monitored file name
script_name = "fetch_tweets.py"

def is_script_running(name):
    """Check If Script is Running"""
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check if the running task contains the script name
            cmdline = process.info.get('cmdline')
            if cmdline and name in cmdline:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

while True:
    # Check if the script is running 
    if not is_script_running(script_name):
        print(f"{script_name} is not running. Starting it now...")
        os.system(f"python {script_name}")
    else:
        print(f"{script_name} is already running.")

    # Check every 5 mins
    time.sleep(300)

