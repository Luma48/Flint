import os
import sys
import subprocess
from PyQt5.QtGui import QFontDatabase

# Project Imports
from managers.Debug_Manager import debug

#===================================================================================================================================
# Method for getting resources compiled or external (uses a relative path)                                                                               
#===================================================================================================================================
def get_resource(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller extracts to _MEIPASS
        base_path = sys._MEIPASS
    else:
        # Development mode: assume you're running from the project root or from src/ so we normalize the path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.abspath(os.path.join(script_dir, "../.."))

    return os.path.join(base_path, relative_path)

# Windows: C:\Users\Username\AppData\Local\Temp\_MEIXXXXXX
# Linux: /tmp/_MEIXXXXXX
# Mac OSX: /private/tmp/_MEIXXXXXX
# If there is any deviation from this pleeeeeeeeeeeeease let me know because I don't think there should be (but I'll blame some random Linux distro if there is)

#===================================================================================================================================
# Method for external resources not included in compiles                                                                                       
#===================================================================================================================================
def get_external_resource(relative_path: str):
    debug.debug("Resolving external resource: %s", relative_path)

    if hasattr(sys, '_MEIPASS'):
        # In PyInstaller build: executable directory
        base_path = os.path.dirname(sys.executable)
        debug.debug(f"Detected PyInstaller bundle, base_path = {base_path}")
    else:
        # In dev: relative to this scripts parent
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.abspath(os.path.join(script_dir, "../.."))
        debug.debug(f"Detected dev mode, script_dir = {script_dir}, base_path = {base_path}")

    resource_path = os.path.join(base_path, relative_path)
    debug.info("Resolved resource path: %s!", resource_path)

    return resource_path

# ==================================================================================================================================
# Method for Loading custom fonts
# ==================================================================================================================================
def load_font(path: str) -> str:
    full_path = get_resource(path)
    debug.debug("Attempting to load font from: %s", full_path)

    font_id = QFontDatabase.addApplicationFont(full_path)

    if font_id != -1:
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        debug.debug("Successfully loaded font: %s (ID: %d)", family, font_id)
        return family

    debug.error("Failed to load custom font from: %s. Falling back to Arial.", full_path)
    return "Arial"
    
#===================================================================================================================================
# Helper Function Check if the settings and theme files actually exists, if not it creates them                                                     
#===================================================================================================================================
def ensure_settings_ini_exists():
    settings_path = get_external_resource("Settings.ini")

    if not os.path.exists(settings_path):
        debug.debug("Settings.ini not found, creating default Settings.ini at %s...", settings_path)
        with open(settings_path, 'w') as f:
            f.write("""[General]
[General]
dark_theme=false
spm_text_on=true
disable_sounds=false
disable_bgm=false
sfx_volume=20
bgm_volume=20
language=English
window_r=10
window_g=10
use_custom_theme=false
window_b=30
bright_text_r=255
disabled_text_r=120
window_text_r=200
window_text_g=200
window_text_b=255
base_r=5
alternate_base_r=30
tooltip_base_g=240
tooltip_base_b=255
text_r=200
button_text_r=200
button_text_g=200
button_text_b=255
highlight_g=0
alternate_base_g=0
alternate_base_b=40
tooltip_base_r=240
tooltip_text_r=0
tooltip_text_g=0
tooltip_text_b=0
text_g=200
text_b=255
button_r=50
base_b=20
button_g=0
base_g=5
button_b=80
bright_text_g=50
disabled_text_g=120
bright_text_b=150
highlight_r=100
highlight_b=200
highlighted_text_r=255
highlighted_text_g=255
highlighted_text_b=255
disabled_text_b=160
disabled_button_text_r=120
disabled_button_text_g=120
disabled_button_text_b=160
bgm_track=Title Theme.mp3
loop_all=true
loop_current=false
""")
            debug.info("Created Default Settings.ini at %s", settings_path)

#===================================================================================================================================
# Helper Function for Linux sound Handeling                                                                                        #
#===================================================================================================================================
def gstreamer_linux_bgm():
    if getattr(sys, 'frozen', False):
        gstreamer_path = None

        try:
            result = subprocess.run(
                ['pkg-config', '--variable=pluginsdir', 'gstreamer-1.0'],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                check=True
            )
            gstreamer_path = result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        common_paths = [
            '/usr/lib/x86_64-linux-gnu/gstreamer-1.0',  # Ubuntu/Debian
            '/usr/lib64/gstreamer-1.0',                 # Fedora/RHEL/CentOS/openSUSE
            '/usr/lib/gstreamer-1.0',                   # Arch/older systems
            '/usr/local/lib/gstreamer-1.0',             # custom builds (I will end you if you dare!!!)
        ]

        if not gstreamer_path:
            for path in common_paths:
                if os.path.exists(path):
                    gstreamer_path = path
                    break

        if gstreamer_path and os.path.exists(gstreamer_path):
            os.environ['GST_PLUGIN_PATH'] = gstreamer_path
            debug.info(f"Using GStreamer plugin path: {gstreamer_path}")
        else:
            debug.warning("Warning: GStreamer plugin path not found.")