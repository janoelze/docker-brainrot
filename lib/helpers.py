from rich.console import Console
from datetime import datetime

console = Console(log_path=False)

def log_message(level, message, debug_only=False):
    if debug_only and not DEBUG_MODE:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.log(f"{message}")