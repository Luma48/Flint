import sys
import ctypes
import shutil
from PyQt5.QtGui import QIcon
import os

# Project Imports
from managers.Debug_Manager import debug
from managers.Resource_Manager import get_resource, gstreamer_linux_bgm

#===================================================================================================================================
# Helper Function for Installing Icons to XDG Structure
#===================================================================================================================================
def install_multi_resolution_icons():
    user_home = os.path.expanduser("~")
    icon_sizes = [16, 24, 32, 48, 64, 96, 128, 256]

    for size in icon_sizes:
        # Target directory and icon name
        target_icon_dir = os.path.join(
            user_home, ".local", "share", "icons", "hicolor", f"{size}x{size}", "apps"
        )
        os.makedirs(target_icon_dir, exist_ok=True)

        source_icon_name = f"Icon{size}x{size}.png"
        source_icon_path = get_resource(f"Packaged_Resources/Images/Editor/{source_icon_name}")
        target_icon_path = os.path.join(target_icon_dir, "flint.png")

        # Copy if it doesn't exist already
        if not os.path.exists(target_icon_path):
            try:
                shutil.copy(source_icon_path, target_icon_path)
                debug.info("Copied icon: %s → %s", source_icon_path, target_icon_path)
            except Exception as e:
                debug.error("Failed to copy %s: %s", source_icon_path, e)

#===================================================================================================================================
# Helper Function for Linux Icon and Desktop File Handling                                                                                         
#===================================================================================================================================
def ensure_desktop_file():
    user_home = os.path.expanduser("~")
    
    # Standard XDG paths
    desktop_dir = os.path.join(user_home, ".local", "share", "applications")
    desktop_file = os.path.join(desktop_dir, "Flint.desktop")

    # Ensure application directory exists
    os.makedirs(desktop_dir, exist_ok=True)

    debug.debug("Ensured XDG desktop directory exists")

    # Install all icon sizes
    try:
        install_multi_resolution_icons()
    except Exception as e:
        debug.warning("Icon installation failed: %s", e)

    # Determine executable path
    exec_path = os.path.abspath(sys.executable)  # PyInstaller binary path

    # Create the .desktop entry
    desktop_entry = f"""[Desktop Entry]
Version=1.0
Name=Flint
Comment=Super Paper Mario Robust Text Editor
Exec=\"{exec_path}\"
Icon=flint
Terminal=false
Type=Application
Categories=Utility;TextEditor;
StartupWMClass=Flint
StartupNotify=true
"""

    # Write .desktop file
    try:
        with open(desktop_file, "w") as f:
            f.write(desktop_entry)
        os.chmod(desktop_file, 0o755)
        debug.info("Created/updated .desktop file at: %s", desktop_file)
    except Exception as e:
        debug.error("Failed to write .desktop file: %s", e)

    # Update system icon and desktop caches
    try:
        os.system("gtk-update-icon-cache -f ~/.local/share/icons/hicolor")
        os.system("update-desktop-database ~/.local/share/applications")
        debug.info("Updated icon and desktop entry caches")
    except Exception as e:
        debug.warning("Failed to update desktop caches: %s", e)

def program_icon_loader(app):
    # =====================================================================
    # Windows Icon Loader
    # =====================================================================
    if sys.platform == "win32":
        debug.debug("Platform detected: Windows — setting AppUserModelID and Icon...")
        try:
            myappid = 'com.luma48.flint'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            app.setWindowIcon(QIcon(get_resource("Packaged_Resources/Images/Editor/Icon.ico")))
            debug.info("AppUserModelID and Icon set!")
        except Exception as e:
            debug.error("Failed to set Windows AppUserModelID or Icon: %s", e)

    # =====================================================================
    # Mac OSX Icon Loader
    # =====================================================================
    elif sys.platform == "darwin":
        debug.debug("Platform detected: macOS — setting Dock icon.")
        try:
            from AppKit import NSApplication, NSImage
            icon_path = get_resource("Packaged_Resources/Images/Editor/Icon.icns")
            if not os.path.exists(icon_path):
                debug.warning("macOS icon file not found: %s", icon_path)
            else:
                nsapp = NSApplication.sharedApplication()
                nsimage = NSImage.alloc().initWithContentsOfFile_(icon_path)
                nsapp.setApplicationIconImage_(nsimage)
                app.setWindowIcon(QIcon(icon_path))
                debug.info("Dock Icon set!")
        except Exception as e:
            debug.error("Failed to set macOS icon: %s", e)

    # =====================================================================
    # Linux/Cross-platform Icon Loader
    # =====================================================================
    else:  # Linux basically
        debug.debug("Platform detected: Linux/Other — ensuring desktop file and initializing gstreamer.")
        try:
            ensure_desktop_file()
        except Exception as e:
            debug.warning("Could not ensure desktop file: %s", e)

        try:
            gstreamer_linux_bgm()
            debug.info("Initialized gstreamer for Linux.")
        except Exception as e:
            debug.warning("Failed to initialize gstreamer: %s", e)