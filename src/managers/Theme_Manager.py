import os
import sys
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog
from PyQt5.QtGui import QPalette, QColor
import json

# Project Imports
from managers.Debug_Manager import debug
from managers.Resource_Manager import get_external_resource
from managers.Sound_Manager import play_sound_by_name

# =====================================================================
# Main theme environment configuration
# =====================================================================
def configure_qt_environment():
    # Force Fusion style everywhere
    os.environ["QT_STYLE_OVERRIDE"] = "fusion"

    # On Linux, force X11 backend instead of Wayland
    if sys.platform.startswith("linux"):
        os.environ["QT_QPA_PLATFORM"] = "xcb"

# =====================================================================
# Dark Theme Toggle Handler
# =====================================================================
def handle_dark_theme_toggle(settings: QSettings, controls: dict, dark_enabled: bool):

    settings.setValue("dark_theme", dark_enabled)
    debug.debug("Saved 'use_custom_theme' = %s to settings", dark_enabled)

    # Disable custom theme checkbox if dark theme is on
    if "use_custom_theme" in controls and "checkbox" in controls["use_custom_theme"]:
        controls["use_custom_theme"]["checkbox"].setEnabled(not dark_enabled)
        debug.debug("Custom theme checkbox %s", "disabled" if dark_enabled else "enabled")

    app = QApplication.instance()
    if app:
        debug.debug("QApplication instance found, applying theme...")
        apply_theme_to(app)
        debug.debug("No QApplication instance available, skipping theme apply")

# =====================================================================
# Custom Theme Toggle Handler
# =====================================================================
def handle_custom_theme_toggle(settings: QSettings, controls: dict, custom_enabled: bool):

    settings.setValue("use_custom_theme", custom_enabled)
    debug.debug("Saved 'use_custom_theme' = %s to settings", custom_enabled)

    # Disable dark theme checkbox if custom theme is on
    if "dark_theme" in controls and "checkbox" in controls["dark_theme"]:
        controls["dark_theme"]["checkbox"].setEnabled(not custom_enabled)
        debug.debug("Dark theme checkbox %s", "disabled" if custom_enabled else "enabled")
    app = QApplication.instance()
    if app:
        debug.debug("QApplication instance found, applying theme...")
        apply_theme_to(app)
        debug.debug("Theme applied successfully after toggle")
    else:
        debug.debug("No QApplication instance available, skipping theme apply")

# =====================================================================
# Applying theme Method
# =====================================================================
def apply_theme_to(app):
    settings = QSettings(get_external_resource("Settings.ini"), QSettings.IniFormat)
    
    # Check if custom theme is enabled
    if settings.value("use_custom_theme", False, type=bool):
        debug.debug("Applying custom theme from Settings.ini...")
        app.setPalette(_custom_palette(settings))
        debug.info("Applied custom theme from Settings.ini!")
    elif settings.value("dark_theme", False, type=bool):
        debug.debug("Applying built-in dark Fusion theme...")
        app.setPalette(_fusion_dark_palette())
        debug.info("Applied built-in dark Fusion theme!")
    else:
        debug.debug("Applying default Fusion light theme...")
        app.setPalette(app.style().standardPalette())
        debug.info("Applied default Fusion light theme!")

# =====================================================================
# Dark Theme Method (I'll add more later)
# =====================================================================
def _fusion_dark_palette():
    palette = QPalette()

    # Background and Text Colours
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    
    # Secondary background and for entry fields (my text editor)
    palette.setColor(QPalette.Base, QColor(42, 42, 42))

    # Colour for Alternating colour for lists, tool tips and tooltip text
    palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)

    # Standard Text Colour, Button Background Colour, Button text Colour and Special Alert text Colour
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)

    # Highlight for selected item in row, list or slider and text colour in the highlight
    palette.setColor(QPalette.Highlight, QColor(100, 100, 255))
    palette.setColor(QPalette.HighlightedText, Qt.black)

    # Disabled state text colours
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))

    return palette

# =====================================================================
# Custom Theme Method (slider-based colours)
# =====================================================================
def _custom_palette(settings: QSettings) -> QPalette:
    palette = QPalette()

    def get_color(key, default):
        r = settings.value(f"{key}_r", default[0], type=int)
        g = settings.value(f"{key}_g", default[1], type=int)
        b = settings.value(f"{key}_b", default[2], type=int)
        return QColor(r, g, b)

    # Background and Text Colours
    palette.setColor(QPalette.Window, get_color("window", (53, 53, 53)))
    palette.setColor(QPalette.WindowText, get_color("window_text", (255, 255, 255)))

    # Secondary background and entry fields
    palette.setColor(QPalette.Base, get_color("base", (42, 42, 42)))

    # Alternating background, tooltips
    palette.setColor(QPalette.AlternateBase, get_color("alternate_base", (66, 66, 66)))
    palette.setColor(QPalette.ToolTipBase, get_color("tooltip_base", (255, 255, 255)))
    palette.setColor(QPalette.ToolTipText, get_color("tooltip_text", (255, 255, 255)))

    # Standard text, buttons, alerts
    palette.setColor(QPalette.Text, get_color("text", (255, 255, 255)))
    palette.setColor(QPalette.Button, get_color("button", (53, 53, 53)))
    palette.setColor(QPalette.ButtonText, get_color("button_text", (255, 255, 255)))
    palette.setColor(QPalette.BrightText, get_color("bright_text", (255, 0, 0)))

    # Highlight + text
    palette.setColor(QPalette.Highlight, get_color("highlight", (100, 100, 255)))
    palette.setColor(QPalette.HighlightedText, get_color("highlighted_text", (0, 0, 0)))

    # Disabled state
    palette.setColor(QPalette.Disabled, QPalette.Text, get_color("disabled_text", (127, 127, 127)))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, get_color("disabled_button_text", (127, 127, 127)))

    return palette

# =====================================================================
# Slider handler for Colour changes
# =====================================================================
def handle_color_slider_change(settings: QSettings, key: str, value: int):
    settings.setValue(key, value)

    # Only apply theme if custom theme is enabled
    if settings.value("use_custom_theme", False, type=bool):
        app = QApplication.instance()
        if app:
            apply_theme_to(app)

# =====================================================================
# Export Custom Theme
# =====================================================================
def export_custom_theme(settings: QSettings, parent=None):
    debug.debug("Theme Export Process Starting")
    theme_data = {}
    for key_base in ["window","window_text","base","alternate_base","tooltip_base","tooltip_text",
                    "text","button","button_text","bright_text","highlight","highlighted_text",
                    "disabled_text","disabled_button_text"]:
        r = settings.value(f"{key_base}_r", 0, type=int)
        g = settings.value(f"{key_base}_g", 0, type=int)
        b = settings.value(f"{key_base}_b", 0, type=int)
        theme_data[key_base] = [r, g, b]
    debug.debug(f"Theme Data Collected for Export: {theme_data}")

    file_path, _ = QFileDialog.getSaveFileName(parent, "Export Theme", "", "JSON Files (*.json)")
    debug.debug(f"File selected for export: {file_path}")
    if file_path:
        try:
            with open(file_path, "w") as f:
                json.dump(theme_data, f, indent=4)
            debug.debug("Theme Exported Successfully to: %s", file_path)
            play_sound_by_name("menu_theme_save")
            QMessageBox.information(parent, "Export Successful", "Theme exported successfully!")
            play_sound_by_name("menu_cancel")
        except Exception as e:
            debug.error("Theme Export Failed: %s", str(e))
            play_sound_by_name("menu_failed")
            QMessageBox.warning(parent, "Error", f"Failed to export theme: {e}")
            play_sound_by_name("menu_cancel")


# =====================================================================
# Import Custom Theme
# =====================================================================
def import_custom_theme(settings: QSettings, controls: dict, parent=None):
    debug.debug("Theme Import Process Starting")
    if not settings.value("use_custom_theme", False, type=bool):
        debug.debug("Theme Import Failed: 'Use Custom Theme' is not enabled")
        play_sound_by_name("menu_failed")
        QMessageBox.information(parent, "Info", "Enable 'Use Custom Theme' first.")
        play_sound_by_name("menu_cancel")
        return

    file_path, _ = QFileDialog.getOpenFileName(parent, "Import Theme", "", "JSON Files (*.json)")
    debug.debug(f"File selected for import: {file_path}")
    if not file_path:
        debug.debug("Theme Import cancelled: No file selected")
        return

    try:
        with open(file_path, "r") as f:
            theme_data = json.load(f)
        debug.debug(f"Theme Imported Successfully with values: {theme_data}")
    except Exception as e:
        debug.error("Theme Import Failed: %s", str(e))
        play_sound_by_name("menu_failed")
        QMessageBox.warning(parent, "Error", f"Failed to load theme: {e}")
        play_sound_by_name("menu_cancel")
        return

    for key_base, rgb in theme_data.items():
        if len(rgb) == 3:
            debug.debug(f"Applying color values for '{key_base}': {rgb}")
            settings.setValue(f"{key_base}_r", rgb[0])
            settings.setValue(f"{key_base}_g", rgb[1])
            settings.setValue(f"{key_base}_b", rgb[2])

            # Update slider widgets if they exist
            for channel, value in zip(["_r","_g","_b"], rgb):
                slider_key = f"{key_base}{channel}"
                if slider_key in controls and "slider" in controls[slider_key]:
                    controls[slider_key]["slider"].setValue(value)

    # Apply theme immediately
    app = QApplication.instance()
    if app:
        apply_theme_to(app)
    debug.debug("Theme Import and Application Completed Successfully")
    play_sound_by_name("menu_theme_switch")
    QMessageBox.information(parent, "Import Successful", "Theme imported successfully!")
    play_sound_by_name("menu_cancel")
