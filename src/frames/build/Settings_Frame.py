from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout
)

# Project Imports
from managers.Theme_Manager import handle_color_slider_change, import_custom_theme, export_custom_theme, handle_dark_theme_toggle, handle_custom_theme_toggle
from frames.Secondary_Frame import SecondaryFrame
from managers.Resource_Manager import get_external_resource, load_font
from managers.Sound_Manager import play_sound_by_name, should_play_sounds, set_volume_for_all, set_bgm_volume, set_sfx_muted, set_bgm_muted, get_available_bgm_tracks, play_bgm_track, handle_loop_current_toggle, handle_loop_all_toggle
from managers.Debug_Manager import debug

#===================================================================================================================================
# The Class for Drawing the Settings Window
#===================================================================================================================================
class Settings(QDialog):
    def __init__(self, parent=None):
        debug.debug("Initializing Settings Window...")
        super().__init__(parent)

        #===================================================================
        # Settings states and initial load
        #===================================================================
        # Track exactly which settings changed
        self._changed_keys = set()

        # Initialize persistent settings saved by the user
        self.settings = QSettings(get_external_resource("Settings.ini"), QSettings.IniFormat)

        #===================================================================
        # Basic Window Params
        #===================================================================
        self.setWindowTitle("Settings")
        SecondaryFrame.set_fixed_size(self, parent, 0.6, 0.85)

        # Window Contents
        layout = QVBoxLayout()

        # Custom font
        font_family = load_font("Packaged_Resources/Fonts/ProgramFont.ttf")
        control_font = QFont(font_family, 10)

        #===================================================================
        # Window Body
        #===================================================================
        # Add image
        SecondaryFrame.add_image(self, layout, "Packaged_Resources/Images/Editor/Settings.png", 200)

        # The header
        header_text = (
            f'<span style="font-family:\'{font_family}\'; font-weight:bold; font-size:16pt;">'
            "Application Settings<br>"
            "</span>"
        )
        self.about_label = SecondaryFrame.add_text_label(layout, header_text, QtCore.Qt.AlignCenter)

        # All controls defined here
        controls_info = [
            {'type': 'checkbox', 'label': 'Mute SFX', 'setting_key': 'disable_sounds', 'font': QFont(font_family, 10), 'on_change': lambda checked: set_sfx_muted(checked)},
            {'type': 'slider', 'label': 'Sound Effects Volume', 'setting_key': 'sfx_volume', 'min': 1, 'max': 100, 'font': QFont(font_family, 8), 'on_change': lambda value: (set_volume_for_all(value / 100.0),play_sound_by_name("menu_select") if should_play_sounds() else None)},
            {'type': 'dropdown', 'label': 'Track Selection', 'setting_key': 'bgm_track', 'options': get_available_bgm_tracks("Audio/BGM"), 'font': QFont(font_family, 9), 'on_change': lambda track: play_bgm_track("Audio/BGM", track) if track else None},
            {'type': 'checkbox', 'label': 'Mute BGM', 'setting_key': 'disable_bgm', 'font': QFont(font_family, 10), 'on_change': lambda checked: set_bgm_muted(checked)},
            
            {'type': 'checkbox', 'label': 'Loop Selected Track', 'setting_key': 'loop_current', 'font': QFont(font_family, 10), 'on_change': lambda checked: handle_loop_current_toggle(self.settings, self.controls, checked)},
            {'type': 'checkbox', 'label': 'Loop All Tracks', 'setting_key': 'loop_all', 'font': QFont(font_family, 10), 'on_change': lambda checked: handle_loop_all_toggle(self.settings, self.controls, checked)},
            
            {'type': 'slider', 'label': 'BGM Volume', 'setting_key': 'bgm_volume', 'min': 1, 'max': 100, 'font': QFont(font_family, 8), 'on_change': lambda value: set_bgm_volume(value / 100.0)},
            {'type': 'dropdown', 'label': 'Language', 'setting_key': 'language', 'options': ['English', 'French', 'Japanese'], 'font': QFont(font_family, 9), 'option_callbacks': { 'English': lambda:print("English Selected!"), 'French': lambda:print("French Selected!"), 'Japanese': lambda:print("Japanese Selected!")}},

            # Theme Control
            {'type': 'checkbox', 'label': 'Use Dark Theme', 'setting_key': 'dark_theme', 'font': QFont(font_family, 10), 'on_change': lambda checked: handle_dark_theme_toggle(self.settings, self.controls, checked)},
            {'type': 'checkbox', 'label': 'Use Custom Theme', 'setting_key': 'use_custom_theme', 'font': QFont(font_family, 10), 'on_change': lambda checked: handle_custom_theme_toggle(self.settings, self.controls, checked)},
            
            # Background + text
            {'type': 'slider', 'label': 'Window RGB', 'setting_key': 'window_r', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='window_r': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'window_g', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='window_g': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'window_b', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='window_b': handle_color_slider_change(self.settings, k, value)},

            {'type': 'slider', 'label': 'Window Text RGB', 'setting_key': 'window_text_r', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='window_text_r': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'window_text_g', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='window_text_g': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'window_text_b', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='window_text_b': handle_color_slider_change(self.settings, k, value)},

            # Base
            {'type': 'slider', 'label': 'Base RGB', 'setting_key': 'base_r', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='base_r': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'base_g', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='base_g': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'base_b', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='base_b': handle_color_slider_change(self.settings, k, value)},

            # Alternate Base
            {'type': 'slider', 'label': 'Alternate Base RGB', 'setting_key': 'alternate_base_r', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='alternate_base_r': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'alternate_base_g', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='alternate_base_g': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'alternate_base_b', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='alternate_base_b': handle_color_slider_change(self.settings, k, value)},

            # Tooltip Base
            {'type': 'slider', 'label': 'Tooltip Base RGB', 'setting_key': 'tooltip_base_r', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='tooltip_base_r': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'tooltip_base_g', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='tooltip_base_g': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'tooltip_base_b', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='tooltip_base_b': handle_color_slider_change(self.settings, k, value)},

            # Tooltip Text
            {'type': 'slider', 'label': 'Tooltip Text RGB', 'setting_key': 'tooltip_text_r', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='tooltip_text_r': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'tooltip_text_g', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='tooltip_text_g': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'tooltip_text_b', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='tooltip_text_b': handle_color_slider_change(self.settings, k, value)},

            # Text
            {'type': 'slider', 'label': 'Text RGB', 'setting_key': 'text_r', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='text_r': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'text_g', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='text_g': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'text_b', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='text_b': handle_color_slider_change(self.settings, k, value)},

            # Button
            {'type': 'slider', 'label': 'Button RGB', 'setting_key': 'button_r', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='button_r': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'button_g', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='button_g': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'button_b', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='button_b': handle_color_slider_change(self.settings, k, value)},

            # Button Text
            {'type': 'slider', 'label': 'Button Text RGB', 'setting_key': 'button_text_r', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='button_text_r': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'button_text_g', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='button_text_g': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'button_text_b', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='button_text_b': handle_color_slider_change(self.settings, k, value)},

            # Bright Text
            {'type': 'slider', 'label': 'Bright Text RGB', 'setting_key': 'bright_text_r', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='bright_text_r': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'bright_text_g', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='bright_text_g': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'bright_text_b', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='bright_text_b': handle_color_slider_change(self.settings, k, value)},

            # Highlight
            {'type': 'slider', 'label': 'Highlight RGB', 'setting_key': 'highlight_r', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='highlight_r': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'highlight_g', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='highlight_g': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'highlight_b', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='highlight_b': handle_color_slider_change(self.settings, k, value)},

            # Highlighted Text
            {'type': 'slider', 'label': 'Highlighted Text RGB', 'setting_key': 'highlighted_text_r', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='highlighted_text_r': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'highlighted_text_g', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='highlighted_text_g': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'highlighted_text_b', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='highlighted_text_b': handle_color_slider_change(self.settings, k, value)},

            # Disabled Text
            {'type': 'slider', 'label': 'Disabled Text RGB', 'setting_key': 'disabled_text_r', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='disabled_text_r': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'disabled_text_g', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='disabled_text_g': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'disabled_text_b', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='disabled_text_b': handle_color_slider_change(self.settings, k, value)},

            # Disabled Button Text
            {'type': 'slider', 'label': 'Disabled Button Text RGB', 'setting_key': 'disabled_button_text_r', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='disabled_button_text_r': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'disabled_button_text_g', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='disabled_button_text_g': handle_color_slider_change(self.settings, k, value)},
            {'type': 'slider', 'setting_key': 'disabled_button_text_b', 'min': 0, 'max': 255, 'font': control_font, 'on_change': lambda value, k='disabled_button_text_b': handle_color_slider_change(self.settings, k, value)},
        ]

        #===================================================================
        # Default Fallback Method for Sliders
        #===================================================================
        def on_slider_change(key, value):
            # Mark as changed for all sliders
            self._mark_changed(key)
            debug.debug("Slider '%s' changed to %d%%", key, value)

        #===================================================================
        # Default Fallback Method for DropDowns
        #===================================================================
        def on_dropdown_change(key, value):
            self._mark_changed(key)
            debug.debug("Dropdown '%s' changed to '%s'", key, value)

        
        # Build all controls
        self.controls = SecondaryFrame.add_controls(
            layout,
            self.settings,
            controls_info,
            self,
            font=control_font,
            on_slider_change=on_slider_change,
            on_dropdown_change=on_dropdown_change
        )
        


        # Enforce initial mutual exclusivity
        dark_checked = self.settings.value("dark_theme", False, type=bool)
        custom_checked = self.settings.value("use_custom_theme", False, type=bool)
        self.controls['dark_theme']["checkbox"].setEnabled(not custom_checked)
        self.controls['use_custom_theme']["checkbox"].setEnabled(not dark_checked)
        debug.debug("Applied initial theme checkbox exclusivity: dark_theme=%s, use_custom_theme=%s", dark_checked, custom_checked)

        # Enforce initial mutual exclusivity for looping
        loop_current_checked = self.settings.value("loop_current", True, type=bool)
        loop_all_checked = self.settings.value("loop_all", False, type=bool)
        self.controls['loop_current']["checkbox"].setEnabled(not loop_all_checked)
        self.controls['loop_all']["checkbox"].setEnabled(not loop_current_checked)
        debug.debug("Applied initial loop checkbox exclusivity: loop_current=%s, loop_all=%s", loop_current_checked, loop_all_checked)
        
        #===================================================================
        # Drawing the Window
        #===================================================================
        main_layout = QVBoxLayout(self)

        # Import/Export Theme Buttons
        import_btn = SecondaryFrame.add_button(layout, self, "Import Theme", on_click=lambda: import_custom_theme(self.settings, self.controls, self), click_sound="menu_save_popup", alignment=QtCore.Qt.AlignCenter, font=control_font)
        export_btn = SecondaryFrame.add_button(layout, self, "Export Theme", on_click=lambda: export_custom_theme(self.settings, self), click_sound="menu_save_popup", alignment=QtCore.Qt.AlignCenter, font=control_font)

        # Scrollable settings content
        scrollable = SecondaryFrame.make_scrollable(layout, self, width=self.width()-10, height=self.height()-50)
        main_layout.addWidget(scrollable)

        # Close button outside scrollable content
        close_layout = QHBoxLayout()
        SecondaryFrame.add_button(close_layout, self, "Close", on_click=self.close, click_sound="menu_cancel", alignment=QtCore.Qt.AlignCenter, min_width=200, font=control_font)
        main_layout.addLayout(close_layout)

        # Applying the main layout
        self.setLayout(main_layout)
        debug.info("Settings Window layout successfully initialized!")

        # Play a sound when settings are opened
        if should_play_sounds():
            play_sound_by_name("menu_open")
    #===================================================================
    # Internal Helpers
    #===================================================================
    def _mark_changed(self, key: str):
        self._changed_keys.add(key)

    #===================================================================
    # Export as Method for Toolbar Button Actions
    #===================================================================
    @classmethod
    def show_settings(cls, parent=None):
        debug.debug("Opening Settings Window from toolbar...")
        dlg = cls(parent)
        dlg.exec_()
        debug.info("Settings Window Closed!")

        # Only refresh if something actually changed
        if dlg._changed_keys:
            debug.debug("Settings changed: %s", dlg._changed_keys)
            # Only refresh view if necessary; for now no settings require it (unlike in a dev build with the SPM toggle lol)
            # File open/save already handles refresh so we skip it since it would be slooooow and costly for no real reason
            # If in the future I add some settings affecting bubble content I gotta add them here dipshit:
            # BUBBLE_RELEVANT_KEYS = {"spm_text_on"} -> my example case since this existed before
            # if dlg._changed_keys & BUBBLE_RELEVANT_KEYS and parent and hasattr(parent, "refresh_view"):
            #     parent.refresh_view(dlg._changed_keys)