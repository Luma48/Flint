from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from pathlib import Path

# Project imports
from frames.Secondary_Frame import SecondaryFrame
from managers.Resource_Manager import get_resource, load_font
from managers.Sound_Manager import play_sound_by_name, should_play_sounds
from managers.Debug_Manager import debug


#===================================================================================================================================
# The Class for Drawing the About Window
#===================================================================================================================================
class IconTypes(QWidget):
    # Class level reference
    _instance = None

    # Regular icon resources
    spm_icons = {
        "PAD_A": ("Icon_A.png", "A Button"),
        "PAD_1": ("Icon_One.png", "1 Button"),
        "PAD_2": ("Icon_Two.png", "2 Button"),
        "PAD_PLUS": ("Icon_Plus.png", "Start Button"),
        "PAD_MINUS": ("Icon_Minus.png", "Select Button"),
        "PAD": ("Icon_Pad.png", "Directional Pad Button"),
        "HM": ("Icon_Heart.png", "Heart Icon"),
    }

    # Outlier icons
    outlier_icons = {
        "Character ""Þ": ("Icon_Star.png", "Start Icon"),
        "Character ""®": ("Icon_Arrow_Left.png", "Arrow Icon"),
    }

    def __init__(self, parent=None):
        debug.debug("Initializing Icon Types Window...")
        
        # This is done so that the Window isn't owned by the main one or that causes layering issues on Windows
        super().__init__(None)
        
        # Here I keep a reference to the logical parent only for positioning/centering and event filtering
        self._owner = parent
        
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowTitleHint
        )
        #===================================================================
        # Basic Window Params
        #===================================================================
        self.setWindowTitle("Icon Types")
        SecondaryFrame.set_fixed_size(self, parent, 0.7, 0.9)

        # Window Contents
        layout = QVBoxLayout()

        # Custom font
        font_family = load_font("Packaged_Resources/Fonts/ProgramFont.ttf")
        control_font = QFont(font_family, 8)

        #===================================================================
        # Window Body
        #===================================================================
        # Add top image
        SecondaryFrame.add_image(self, layout, "Packaged_Resources/Images/Editor/IconType.png", 200)

        # Title label
        title_text = (
            f"<span style=\"font-family:'{font_family}'; font-weight:bold; font-size:16pt;\">"
            "Super Paper Mario<br>Icons"
            "</span>"
        )
        self.title_label = SecondaryFrame.add_text_label(layout, title_text, QtCore.Qt.AlignCenter)

        # Explanation block
        icon_usage = (
            f"<div style=\"font-family:'{font_family}'; font-size: 10pt;\">"
            "<div style=\"font-weight:bold; font-size:12pt; margin-bottom:15px; color:#FFBF00\">"
            "<br><br>Icon Tag Structure"
            "</div>"
            "When creating dialog in Super Paper Mario you can come across icon tags like this one:"
            "<div style='font-family:Courier New, monospace; font-size:14pt; margin:6px 0;'>"
            "<span style='color:#4CAF50;'>&lt;icon</span> "
            "<span style='color:#2196F3;'>PAD_A</span> "
            "<span style='color:#E91E63;'>0.58</span> "
            "<span style='color:#9C27B0;'>0</span> "
            "<span style='color:#FF9800;'>0</span> "
            "<span style='color:#795548;'>0</span>"
            "<span style='color:#4CAF50;'>&gt;</span>"
            "</div><br>"
            "Icon Tags found in Super Paper Mario work as follows:"
            "<ul style='margin-top:5px; margin-bottom:0; padding-left:20px;'>"
            "<li><span style='color:#4CAF50;'>&lt;icon&gt;</span> → the tag type for icons</li>"
            "<li><span style='color:#2196F3;'>PAD_A</span> → the icon resource being used</li>"
            "<li><span style='color:#E91E63;'>0.58</span> → scale of the icon</li>"
            "<li><span style='color:#9C27B0;'>0</span> → X position offset</li>"
            "<li><span style='color:#FF9800;'>0</span> → Y position offset</li>"
            "<li><span style='color:#795548;'>0</span> → unused / reserved value</li>"
            "</ul>"
            "</div><br>"
        )
        self.icon_usage_label = SecondaryFrame.add_text_label(layout, icon_usage, QtCore.Qt.AlignCenter)

        # Build and add icon lists
        icon_types_html = self.build_icon_list(
            "Super Paper Mario Icon Resources",
            self.spm_icons,
            font_family,
            description="These are the standard icons available through the <icon> tag system."
        )

        outlier_types_html = self.build_icon_list(
            "Super Paper Mario Icon Resources Outliers",
            self.outlier_icons,
            font_family,
            description="Some icons are technically part of the system but are stored in the font itself. "
                        "They appear when certain characters are used instead of being standalone resources."
        )


        self.icon_types_label = SecondaryFrame.add_text_label(layout, icon_types_html, QtCore.Qt.AlignCenter)
        self.outlier_types_label = SecondaryFrame.add_text_label(layout, outlier_types_html, QtCore.Qt.AlignCenter)

        #===================================================================
        # Drawing the Window
        #===================================================================
        main_layout = QVBoxLayout()

        # Scrollable content
        scrollable = SecondaryFrame.make_scrollable(layout, self, width=self.width()-10, height=self.height()-50)
        main_layout.addWidget(scrollable)

        # Close button outside scrollable content
        close_layout = QHBoxLayout()
        SecondaryFrame.add_button(close_layout, self, "Close", on_click=self.close, click_sound="menu_about_close", alignment=QtCore.Qt.AlignCenter, min_width=200, font=control_font)
        main_layout.addLayout(close_layout)

        self.setLayout(main_layout)
        debug.info("Icon Type Window layout successfully initialized!")

        # Play sound when About opens
        if should_play_sounds():
            play_sound_by_name("menu_about_open")

    #===================================================================
    # Helper to build HTML lists
    #===================================================================
    @staticmethod
    def build_icon_list(title: str, icon_dict: dict, font_family: str, description: str = "") -> str:
        list_items = []
        for tag, (filename, desc) in icon_dict.items():
            icon_path = Path(get_resource(f"Packaged_Resources/Images/Icons/{filename}")).as_uri()
            li = (
                f"<li><span style='color:#2196F3;'>{tag}</span> → "
                f"<img src='{icon_path}' width='40' height='40' style='vertical-align:middle;'> "
                f"<span style='color:#FF0000;'>{desc}</span></li>"
            )
            list_items.append(li)

        return (
            f"<div style=\"font-family:'{font_family}'; margin-bottom:1.5rem;\">"
            f"<div style=\"font-weight:bold; font-size:12pt; margin-bottom:10px; color:#FFBF00\">{title}</div>"
            f"<div style=\"font-weight:normal; font-size:10pt; line-height:130%; margin-bottom:8px;\">{description}</div>"
            "<ul style='margin-top:5px; margin-bottom:0; padding-left:20px;'>"
            + "".join(list_items) +
            "</ul>"
            "</div><br>"
        )

    #===================================================================
    # Export as Method for Toolbar Button Actions
    #===================================================================
    @classmethod
    def show_icon_types(cls, parent=None):
        debug.debug("Opening Icon Type Window from toolbar...")
        if cls._instance is None:
            cls._instance = cls(parent)
            cls._instance.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            cls._instance.destroyed.connect(lambda: setattr(cls, "_instance", None))

        cls._instance.show()
        cls._instance.raise_()
        cls._instance.activateWindow()
        debug.info("Icon Type Window Closed!")