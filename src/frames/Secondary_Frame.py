import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel, QWidget, QHBoxLayout, QCheckBox, QPushButton, QSlider, QVBoxLayout, QComboBox, QScrollArea
)

# Project Imports
from managers.Sound_Manager import play_sound_by_name, should_play_sounds
from managers.Resource_Manager import get_resource
from managers.Debug_Manager import debug


class SecondaryFrame:

    # ==================================================================================================================================
    # Method for window sizing
    # ==================================================================================================================================
    @staticmethod
    def set_fixed_size(window, parent, width_divider, height_divider):
        if parent:
            parent_width = parent.width()
            parent_height = parent.height()

            debug.debug("Parent dimensions: width=%d, height=%d", parent_width, parent_height)
            debug.debug("Dividers: width_divider=%.2f, height_divider=%.2f", width_divider, height_divider)

            width = int(parent_width * width_divider)
            height = int(parent_height * height_divider)

            window.setFixedSize(width, height)

            parent_geom = parent.geometry()
            x = parent_geom.x() + (parent_geom.width() - width) // 2
            y = parent_geom.y() + (parent_geom.height() - height) // 2
            window.move(x, y)

            debug.debug("Calculated secondary window size: %dx%d", width, height)
            debug.debug("Calculated secondary window position: x=%d, y=%d", x, y)

        else:
            debug.warning("No parent provided to set_fixed_size; skipping size adjustment.")

    # ==================================================================================================================================
    # Method to wrap widgets in a scrollable container
    # ==================================================================================================================================
    @staticmethod
    def make_scrollable(layout, parent, width=None, height=None):
        debug.debug("Creating scrollable area...")

        scroll_area = QScrollArea(parent)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        container = QWidget()
        container.setLayout(layout)
        scroll_area.setWidget(container)

        if width:
            scroll_area.setFixedWidth(width)
            debug.debug("Set scroll area width: %d", width)
        else:
            debug.debug("No fixed width provided")

        if height:
            scroll_area.setFixedHeight(height)
            debug.debug("Set scroll area height: %d", height)
        else:
            debug.debug("No fixed height provided")

        debug.info("Scroll area created and returned!")
        return scroll_area

    
    # ==================================================================================================================================
    # Method for adding the image label
    # ==================================================================================================================================
    @staticmethod
    def add_image(target_widget, layout, relative_image_path, image_width):
        image_label = QLabel(target_widget)

        pixmap_path = get_resource(relative_image_path)
        debug.debug("Loading image: %s", relative_image_path)
        debug.debug("Resolved path: %s", pixmap_path)
        debug.debug("File exists: %s", os.path.exists(pixmap_path))

        pixmap = QtGui.QPixmap(pixmap_path)

        if not pixmap.isNull():
            debug.debug("Pixmap loaded successfully.")
            scaled_pixmap = pixmap.scaledToWidth(image_width, QtCore.Qt.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(QtCore.Qt.AlignCenter)
        else:
            debug.error("Pixmap failed to load.")
            image_label.setText(f"[Image not found: {relative_image_path}]")

        layout.addWidget(image_label)
        
        #filename = os.path.basename(relative_image_path)
        debug.debug("Added image '%s' to layout", relative_image_path)

    # ==================================================================================================================================
    # Method for the text label
    # ==================================================================================================================================
    @staticmethod
    def add_text_label(layout, text, alignment):
        debug.debug("Adding text label with content: %s", text)
        debug.debug("Alignment flag: %s", str(alignment))

        text_label = QLabel()
        text_label.setText(text)
        text_label.setOpenExternalLinks(True)
        text_label.setWordWrap(True)
        text_label.setAlignment(alignment)

        layout.addWidget(text_label)
        debug.debug("Text label added to layout")

        return text_label

    # ==================================================================================================================================
    # General-purpose control builder (checkboxes, sliders, dropdowns) with per-type/per-control font support
    # ==================================================================================================================================
    @staticmethod
    def add_controls(layout, settings, controls_info, parent=None,
                     font=None, fonts=None, on_slider_change=None, on_dropdown_change=None):
        controls = {}
        fonts = fonts or {}
        default_font = font  # may be None
        debug.debug("Creating settings controls (sliders, checkboxes, dropdowns)")



        def pick_font(control_type: str, info: dict):
            chosen_font = info.get("font") or fonts.get(control_type) or fonts.get("labels") or default_font
            debug.debug("Font selected for %s: %s", control_type, str(chosen_font))
            return chosen_font
        
        for info in controls_info:
            ctype = info.get("type")
            key = info.get("setting_key")

            debug.debug("Processing control: type=%s, setting_key=%s", ctype, key)

            if key is None:
                debug.warning("Control missing setting_key, skipping: %s", str(info))
                continue

            # Checkboxes
            if ctype == "checkbox":
                debug.debug("Creating checkbox: %s", info.get("label", "Checkbox"))

                container = QWidget(parent)
                container_layout = QHBoxLayout()
                container_layout.setContentsMargins(0, 0, 0, 0)

                checkbox = QCheckBox(info.get("label", "Checkbox"), parent)
                use_font = pick_font("checkbox", info)
                if use_font:
                    checkbox.setFont(use_font)

                checked = settings.value(key, False, type=bool)
                checkbox.setChecked(checked)
                debug.debug("Initial checkbox state for %s: %s", key, checked)

                def on_checkbox_state_changed(state, k=key, info=info):
                    is_checked = state == Qt.Checked
                    settings.setValue(k, is_checked)
                    debug.debug("Checkbox '%s' changed to: %s", k, is_checked)

                    if should_play_sounds():
                        play_sound_by_name("menu_select")

                    # Call per-checkbox on_change if provided
                    if "on_change" in info and callable(info["on_change"]):
                        info["on_change"](is_checked)


                checkbox.stateChanged.connect(on_checkbox_state_changed)

                container_layout.addWidget(checkbox, alignment=Qt.AlignCenter)
                container.setLayout(container_layout)
                layout.addWidget(container)

                controls[key] = {
                    "type": "checkbox",
                    "container": container,
                    "checkbox": checkbox,
                }

            # Sliders 
            elif ctype == "slider":
                label_text = info.get("label")  # no default label
                min_val = info.get("min", 0)
                max_val = info.get("max", 100)

                debug.debug("Creating slider: %s", info.get("label"))

                container = QWidget(parent)
                container_layout = QVBoxLayout()
                container_layout.setAlignment(Qt.AlignCenter)

                # Pick the font first
                title_font = pick_font("slider", info)  # always defined
                title_label = None
                if label_text:
                    title_label = QLabel(label_text, parent)
                    if title_font:
                        title_label.setFont(title_font)
                    title_label.setAlignment(Qt.AlignCenter)
                    container_layout.addWidget(title_label)

                # Row: slider + percent readout
                slider_row = QWidget(parent)
                slider_row_layout = QHBoxLayout()
                slider_row_layout.setContentsMargins(0, 0, 0, 0)

                slider = QSlider(Qt.Horizontal, parent)
                slider.setRange(min_val, max_val)
                init_val = settings.value(key, int((max_val - min_val) / 2), type=int)
                slider.setValue(init_val)

                debug.debug("Slider '%s' initial value: %d", key, init_val)

                percent_label = QLabel(f"{init_val}%", parent)
                # percent_label can always use title_font (even if title_label is None)
                if title_font:
                    percent_label.setFont(title_font)
                percent_label.setFixedWidth(48)
                percent_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

                slider_row_layout.addWidget(slider)
                slider_row_layout.addWidget(percent_label)
                slider_row.setLayout(slider_row_layout)

                container_layout.addWidget(slider_row)
                container.setLayout(container_layout)
                layout.addWidget(container)

                def handle_slider_change(value, k=key, pl=percent_label, info=info):
                    settings.setValue(k, value)
                    pl.setText(f"{value}%")
                    
                    # Call per-control handler if defined
                    if "on_change" in info and callable(info["on_change"]):
                        debug.debug("Executing general on_change callback")
                        info["on_change"](value)
                    
                    # Call global handler if provided
                    if on_slider_change:
                        on_slider_change(k, value)

                slider.valueChanged.connect(handle_slider_change)

                controls[key] = {
                    "type": "slider",
                    "container": container,
                    "slider": slider,
                    "percent_label": percent_label,
                    "title_label": title_label,  # may be None
                }


            # Dropdowns
            elif ctype == "dropdown":
                label_text = info.get("label")  # no default
                options = info.get("options", [])

                debug.debug("Creating dropdown: label='%s', key='%s', options=%s", label_text, key, options)

                container = QWidget(parent)
                container_layout = QVBoxLayout()
                container_layout.setAlignment(Qt.AlignCenter)

                dd_font = pick_font("dropdown", info)  # always defined
                title_label = None
                if label_text:
                    title_label = QLabel(label_text, parent)
                    if dd_font:
                        title_label.setFont(dd_font)
                    title_label.setAlignment(Qt.AlignCenter)
                    container_layout.addWidget(title_label)

                combo = QComboBox(parent)
                combo.addItems(options)
                if dd_font:
                    combo.setFont(dd_font)

                saved_value = settings.value(key, options[0] if options else "", type=str)
                if saved_value in options:
                    combo.setCurrentText(saved_value)

                debug.debug("Dropdown '%s' initial value: %s", key, saved_value)

                def on_combo_changed(value, k=key, info=info):
                    settings.setValue(k, value)

                    # Per-option callback (if defined)
                    if "option_callbacks" in info and value in info["option_callbacks"]:
                        debug.debug("Executing per-option callback for '%s'", value)
                        info["option_callbacks"][value]()
                    
                    # General per-control on_change callback if defined
                    if "on_change" in info and callable(info["on_change"]):
                        debug.debug("Executing general on_change callback")
                        info["on_change"](value)
                    
                     # Call global handler if provided
                    if on_dropdown_change:
                        on_dropdown_change(k, value)
                    
                    if should_play_sounds():
                        play_sound_by_name("menu_select")

                combo.currentTextChanged.connect(on_combo_changed)

                container_layout.addWidget(combo, alignment=Qt.AlignCenter)
                container.setLayout(container_layout)
                layout.addWidget(container)

                controls[key] = {
                    "type": "dropdown",
                    "container": container,
                    "combo": combo,
                    "title_label": title_label,  # may be None
                }

        debug.info("Finished creating controls! Keys: %s", list(controls.keys()))
        return controls

    # ==================================================================================================================================
    # Method for Adding a Button
    # ==================================================================================================================================
    @staticmethod
    def add_button(layout, parent, button_text, on_click=None, click_sound=None, alignment=None, min_width=None, min_height=None, fixed_width=None, fixed_height=None, font=None):
        
        debug.debug("Creating button: '%s'", button_text)
        btn = QPushButton(button_text, parent)

        # Apply font if provided
        if font:
            btn.setFont(font)
            debug.debug("Applied custom font to button '%s'", button_text)
    
        # Click behavior
        def handle_click():
            debug.debug("Button '%s' clicked", button_text)

            if click_sound:
                debug.debug("Click sound requested: '%s'", click_sound)

            if click_sound and should_play_sounds():
                debug.debug("Playing sound: '%s'", click_sound)
                play_sound_by_name(click_sound)

            if on_click:
                debug.debug("Calling on_click handler for '%s'", button_text)
                on_click()

        # Optional sizing
        if fixed_width:
            btn.setFixedWidth(fixed_width)
            debug.debug("Set fixed width for '%s': %d", button_text, fixed_width)
        elif min_width:
            btn.setMinimumWidth(min_width)
            debug.debug("Set minimum width for '%s': %d", button_text, min_width)

        if fixed_height:
            btn.setFixedHeight(fixed_height)
            debug.debug("Set fixed height for '%s': %d", button_text, fixed_height)
        elif min_height:
            btn.setMinimumHeight(min_height)
            debug.debug("Set minimum height for '%s': %d", button_text, min_height)

        btn.clicked.connect(handle_click)

        # Add to layout
        if alignment:
            layout.addWidget(btn, alignment=alignment)
            debug.debug("Button '%s' added to layout with alignment", button_text)
        else:
            layout.addWidget(btn)
            debug.debug("Button '%s' added to layout without alignment", button_text)

        return btn