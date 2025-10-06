import sys
import ctypes
import logging

# =====================================================================
# Detects if a console is attatched (0 means no console is attached)
# =====================================================================
def is_console_available():
    try:
        if sys.platform == "win32":
            # GetConsoleWindow returns 0 if no console is attached
            return ctypes.windll.kernel32.GetConsoleWindow() != 0
        elif sys.platform in ("cygwin", "msys"):
            # These are Unix-like environments on Windows
            return sys.stdout.isatty()
        else:
            # Linux, macOS, and other POSIX systems
            return sys.stdout.isatty()
    except Exception:
        # Fallback: assume no console is available on error
        return False

   
# =====================================================================
# ANSI colour codes
# =====================================================================
RESET = "\033[0m"
COLORS = {
    "DEBUG": "\033[36m",   # Cyan
    "INFO": "\033[32m",    # Green
    "WARNING": "\033[33m", # Yellow
    "ERROR": "\033[31m",   # Red
    "CRITICAL": "\033[41m" # Red background
}

# =====================================================================
# Custom Formatter with colours
# =====================================================================
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        if levelname in COLORS:
            record.levelname = f"{COLORS[levelname]}{levelname}{RESET}"
            record.msg = f"{COLORS[levelname]}{record.msg}{RESET}"
        return super().format(record)

#===================================================================================================================================
# Debug Manager
#===================================================================================================================================
class DebugManager:
    def __init__(self):
        # Detect debug mode
        self.debug_mode = ('--debug' in sys.argv) or is_console_available()

        # Create logger
        self.logger = logging.getLogger("flint")
        self.logger.setLevel(logging.DEBUG if self.debug_mode else logging.WARNING)

        # Prevent duplicate handlers if reloaded (e.g., in hot reload dev)
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(ColoredFormatter('[%(levelname)s] %(message)s'))
            self.logger.addHandler(handler)

    def is_debug(self):
        return self.debug_mode

    def debug(self, msg, *args, **kwargs):
        if self.debug_mode:
            self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

# =====================================================================
# Singleton pattern
# =====================================================================
_debug_instance = None

def get_debug_manager():
    global _debug_instance
    if _debug_instance is None:
        _debug_instance = DebugManager()
    return _debug_instance

# Easy global access
debug = get_debug_manager()