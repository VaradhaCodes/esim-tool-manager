# logger.py

import os
from datetime import datetime

# We keep logs in a "logs" folder, so everything's in one place.
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "tool_manager.log")

os.makedirs(LOG_DIR, exist_ok=True)

def log_event(event_type: str, tool: str, status: str, message: str = ""):
    # Just a quick file-based logger. Simple, but it works fine for a CLI tool.
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{event_type.upper()}] Tool: {tool} | Status: {status.upper()} | {message}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)
