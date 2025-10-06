from PyQt5.QtWidgets import QToolBar, QPushButton, QShortcut
from PyQt5.QtGui import QKeySequence, QFont

# Project Imports
from managers.Toolbar_Adaptive_Widgets import AdaptiveSeparator, AdaptiveLabel
from frames.build.BoxTypes_Frame import BoxTypes
from frames.build.TagTypes_Frame import TagTypes
from frames.build.IconTypes_Frame import IconTypes
from frames.build.About_Frame import About
from frames.build.Settings_Frame import Settings
from renderer.File_Handler import open_file_or_folder, save_file
from managers.Debug_Manager import debug
from managers.Resource_Manager import load_font

#===================================================================================================================================
# Toolbar Building Method
#===================================================================================================================================
def build_toolbar(parent, text_editor, status_label):
    debug.debug("Building toolbar...")

    # =====================================================================
    # Creating the Movable Toolbar
    # =====================================================================
    toolbar = QToolBar("Main Toolbar", parent)
    toolbar.setFloatable(False)
    toolbar.setMovable(True)
    debug.debug("Toolbar created and set movable in the container")

    # =====================================================================
    # Creating the buttons buttons
    # =====================================================================
    btn_open_file = QPushButton("Open Text...", parent)
    btn_save_file = QPushButton("Save Text", parent)
    btn_param_box = QPushButton("Bubble Types", parent)
    btn_param_tag = QPushButton("Tag Types", parent)
    btn_param_icon = QPushButton("Icon Types", parent)
    btn_settings = QPushButton("Settings", parent)
    btn_about = QPushButton("About", parent)
    debug.debug("All toolbar buttons created")

    # =====================================================================
    # Setting font for buttons
    # =====================================================================
    button_font = QFont(load_font("Packaged_Resources/Fonts/ProgramFont.ttf"), 8)

    for btn in [btn_open_file, btn_save_file, btn_param_box, btn_param_tag, btn_param_icon, btn_settings, btn_about]:
        btn.setFont(button_font)

    # =====================================================================
    # Tooltips (show shortcuts too!)
    # =====================================================================
    btn_open_file.setToolTip("Open Text... (Ctrl+O)")
    btn_save_file.setToolTip("Save Text (Ctrl+S)")
    btn_settings.setToolTip("Settings (Ctrl+P)")
    btn_about.setToolTip("About (Ctrl+I)")
    debug.debug("Tooltips set for shortcut buttons")
    
    # =====================================================================
    # Enable/disable buttons
    # =====================================================================
    btn_open_file.setEnabled(True)
    btn_save_file.setEnabled(True)

    for btn in [btn_param_box, btn_param_tag, btn_param_icon]:
        btn.setEnabled(False)

    debug.debug("Initial button states set: open_file enabled, save/add_npc disabled, params disabled")

    # =====================================================================
    # Connect buttons to actions
    # =====================================================================
    btn_open_file.clicked.connect(lambda: open_file_or_folder(parent, text_editor, status_label, btn_param_box, btn_param_tag ,btn_param_icon))
    btn_save_file.clicked.connect(lambda: save_file(parent, text_editor, status_label))
    btn_param_box.clicked.connect(lambda: BoxTypes.show_box_types(parent))
    btn_param_tag.clicked.connect(lambda: TagTypes.show_tag_types(parent))
    btn_param_icon.clicked.connect(lambda: IconTypes.show_icon_types(parent))
    btn_about.clicked.connect(lambda: About.show_about(parent))
    btn_settings.clicked.connect(lambda: Settings.show_settings(parent))
    debug.debug("Button click actions connected")

    # =====================================================================
    # Keyboard shortcuts
    # =====================================================================
    QShortcut(QKeySequence("Ctrl+O"), parent, activated=btn_open_file.click)
    QShortcut(QKeySequence("Ctrl+S"), parent, activated=btn_save_file.click)
    QShortcut(QKeySequence("Ctrl+P"), parent, activated=btn_settings.click)
    QShortcut(QKeySequence("Ctrl+I"), parent, activated=btn_about.click)
    debug.debug("Keyboard shortcuts registered: Ctrl+O, Ctrl+S, Ctrl+P, Ctrl+I")

    # =====================================================================
    # Connect Adaptive widgets
    # =====================================================================
    lbl_params = AdaptiveLabel("Params: ")
    lbl_settings = AdaptiveLabel("Misc: ")
    sep1 = AdaptiveSeparator()
    sep2 = AdaptiveSeparator()
    debug.debug("All Adaptive labels and Separators created")

    # =====================================================================
    # # Add all widgets to toolbar
    # =====================================================================
    toolbar.addWidget(btn_open_file)
    toolbar.addWidget(btn_save_file)
    toolbar.addWidget(sep1)
    toolbar.addWidget(lbl_params)
    toolbar.addWidget(btn_param_box)
    toolbar.addWidget(btn_param_tag)
    toolbar.addWidget(btn_param_icon)
    toolbar.addWidget(sep2)
    toolbar.addWidget(lbl_settings)
    toolbar.addWidget(btn_settings)
    toolbar.addWidget(btn_about)
    debug.debug("All widgets added to toolbar")

    # Collect adaptive widgets for orientation management
    adaptive_widgets = [lbl_params, lbl_settings, sep1, sep2]
    debug.info("Toolbar build complete with %d adaptive widgets!", len(adaptive_widgets))

    return toolbar, adaptive_widgets