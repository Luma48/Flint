from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QApplication
from PyQt5.QtGui import QFont
from PyQt5 import QtCore


# Project imports
from frames.Secondary_Frame import SecondaryFrame
from managers.Resource_Manager import load_font
from managers.Sound_Manager import play_sound_by_name, should_play_sounds
from managers.Debug_Manager import debug

#===================================================================================================================================
# The Class for Drawing the About Window
#===================================================================================================================================
class BoxTypes(QWidget):
    # Class level reference
    _instance = None

    def __init__(self, parent=None):
        debug.debug("Initializing Box Types Window...")
        
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
        self.setWindowTitle("Speach Bubble Types")
        SecondaryFrame.set_fixed_size(self, parent, 0.7, 0.9)

        # Window Contents
        layout = QVBoxLayout()

        # Custom font
        font_family = load_font("Packaged_Resources/Fonts/ProgramFont.ttf")
        control_font = QFont(font_family, 8)
    
        #===================================================================
        # Window Body
        #===================================================================
        # Add image
        SecondaryFrame.add_image(self, layout, "Packaged_Resources/Images/Editor/BoxType.png", 200)

        # Title label
        title_text = (
            f"<span style=\"font-family:'{font_family}'; font-weight:bold; font-size:16pt;\">"
            "Super Paper Mario<br>Speach Bubbles"
            "</span>"
        )
        self.title_label = SecondaryFrame.add_text_label(layout, title_text, QtCore.Qt.AlignCenter)

        normal_text = (
            f"<div style=\"font-family:'{font_family}'; font-size: 10pt;\">"
            # h2
            "<div style=\"font-weight:bold; font-size:12pt; margin-bottom:15px; color:#FFBF00\">"
            "<br><br>Speach Bubble"
            "</div>"
            # Description
            "The Standard Bubble Styling used throughout all of the game. This one has no associated tag and the game will fall back to it if no other bubble is specified."
        )
        self.normal_label = SecondaryFrame.add_text_label(layout, normal_text, QtCore.Qt.AlignCenter)
        SecondaryFrame.add_image(self, layout, "Packaged_Resources/Images/Bubbles/Speach_Bubble.png", 400)

        small_text = (
            f"<div style=\"font-family:'{font_family}'; font-size: 10pt;\">"
            # h2
            "<div style=\"font-weight:bold; font-size:12pt; margin-bottom:15px; color:#FFBF00\">"
            "<br><br>Small Speach Bubble"
            "</div>"
            # md code syntax
            "<div style='font-family:Courier New, monospace; font-size:14pt; margin:6px 0;'>"
            "<span style='color:#4CAF50;'>&lt;small&gt;</span>"
            "</div>"
            # Description
            "A small speach bubble used when characters say something to themselves or under their breath."
        )
        self.small_label = SecondaryFrame.add_text_label(layout, small_text, QtCore.Qt.AlignCenter)
        SecondaryFrame.add_image(self, layout, "Packaged_Resources/Images/Bubbles/Small_Speach_Bubble.png", 200)

        pixl_text = (
            f"<div style=\"font-family:'{font_family}'; font-size: 10pt;\">"
            # h2
            "<div style=\"font-weight:bold; font-size:12pt; margin-bottom:15px; color:#FFBF00\">"
            "<br><br>Pixl Speach Bubble"
            "</div>"
            # md code syntax
            "<div style='font-family:Courier New, monospace; font-size:14pt; margin:6px 0;'>"
            "<span style='color:#4CAF50;'>&lt;fairy&gt;</span>"
            "<span style='color:#2196F3;'> and </span>"
            "<span style='color:#4CAF50;'>&lt;fairy2&gt;</span>"
            "</div>"
            # Desciption
            "The Bubble Styling used for all pixl's throughout all of the game. While simillar to the default bubble it has an animated rainbow outline."
        )
        self.pixl_label = SecondaryFrame.add_text_label(layout, pixl_text, QtCore.Qt.AlignCenter)
        SecondaryFrame.add_image(self, layout, "Packaged_Resources/Images/Bubbles/Pixel_Speach_Bubble.png", 400)

        robo_text = (
            f"<div style=\"font-family:'{font_family}'; font-size: 10pt;\">"
            # h2
            "<div style=\"font-weight:bold; font-size:12pt; margin-bottom:15px; color:#FFBF00\">"
            "<br><br>Robo Speach Bubble"
            "</div>"
            # md code syntax
            "<div style='font-family:Courier New, monospace; font-size:14pt; margin:6px 0;'>"
            "<span style='color:#4CAF50;'>&lt;housou&gt;</span>"
            "</div>"
            # Desciption
            "The Bubble Styling used for all robotic based characters and interactions throughout all of the game. It has a more jaged appearence than the default bubble."
        )
        self.robo_label = SecondaryFrame.add_text_label(layout, robo_text, QtCore.Qt.AlignCenter)
        SecondaryFrame.add_image(self, layout, "Packaged_Resources/Images/Bubbles/Robo_Speach_Bubble.png", 400)

        kanban_text = (
            f"<div style=\"font-family:'{font_family}'; font-size: 10pt;\">"
            # h2
            "<div style=\"font-weight:bold; font-size:12pt; margin-bottom:15px; color:#FFBF00\">"
            "<br><br>Signpost Speach Bubble"
            "</div>"
            # md code syntax
            "<div style='font-family:Courier New, monospace; font-size:14pt; margin:6px 0;'>"
            "<span style='color:#4CAF50;'>&lt;kanban&gt;</span>"
            "</div>"
            # Desciption
            "The Bubble Styling used for signposts throughout all of the game. It has a wooden outline and white paper inside."
        )
        self.kanban_label = SecondaryFrame.add_text_label(layout, kanban_text, QtCore.Qt.AlignCenter)
        SecondaryFrame.add_image(self, layout, "Packaged_Resources/Images/Bubbles/Signpost_Bubble.png", 400)

        swoon_text = (
            f"<div style=\"font-family:'{font_family}'; font-size: 10pt;\">"
            # h2
            "<div style=\"font-weight:bold; font-size:12pt; margin-bottom:15px; color:#FFBF00\">"
            "<br><br>Swoon.exe Speach Bubble"
            "</div>"
            # md code syntax
            "<div style='font-family:Courier New, monospace; font-size:14pt; margin:6px 0;'>"
            "<span style='color:#4CAF50;'>&lt;adv&gt;</span>"
            "</div>"
            # Desciption
            "The Bubble Styling used during the Swoon.exe dating segement with Princess Peach and Francis."
        )
        self.swoon_label = SecondaryFrame.add_text_label(layout, swoon_text, QtCore.Qt.AlignCenter)
        SecondaryFrame.add_image(self, layout, "Packaged_Resources/Images/Bubbles/Swoon_Speach_Bubble.png", 400)

        select_text = (
            f"<div style=\"font-family:'{font_family}'; font-size: 10pt;\">"
            # h2
            "<div style=\"font-weight:bold; font-size:12pt; margin-bottom:15px; color:#FFBF00\">"
            "<br><br>Option Dialog Speach Bubble"
            "</div>"
            # md code syntax
            "<div style='font-family:Courier New, monospace; font-size:14pt; margin:6px 0;'>"
            "<span style='color:#4CAF50;'>&lt;select</span> "
            "<span style='color:#E91E63;'>0</span> "
            "<span style='color:#9C27B0;'>0</span> "
            "<span style='color:#FF9800;'>0</span> "
            "<span style='color:#795548;'>0</span>"
            "<span style='color:#4CAF50;'>&gt;</span>"
            "</div>"
            # Desciption
            "The Standard Bubble Styling used for any option dialogs that are triggered in the game.<br><br>"
            "This bubble tags has some extra values associated with it that work as follows:"
            "<ul style='margin-top:5px; margin-bottom:0; padding-left:20px;'>"
            "<li><span style='color:#E91E63;'>0</span> → position on the X axis of the bubble</li>"
            "<li><span style='color:#9C27B0;'>0</span> → position on the Y axis of the bubble</li>"
            "<li><span style='color:#FF9800;'>0</span> → scale on the X axis of the bubble</li>"
            "<li><span style='color:#795548;'>0</span> → scale on the Y axis of the bubble</li>"
            "</ul>"
        )
        self.select_label = SecondaryFrame.add_text_label(layout, select_text, QtCore.Qt.AlignCenter)
        SecondaryFrame.add_image(self, layout, "Packaged_Resources/Images/Bubbles/Selectbox_Bubble.png", 200)

        swoonselect_text = (
            f"<div style=\"font-family:'{font_family}'; font-size: 10pt;\">"
            "<div style=\"font-weight:bold; font-size:12pt; margin-bottom:15px; color:#FFBF00\">"
            "<br><br>Swoon.exe Option Dialog Speach Bubble"
            "</div>"
            # md code syntax
            "<div style='font-family:Courier New, monospace; font-size:14pt; margin:6px 0;'>"
            "<span style='color:#4CAF50;'>&lt;adv_select</span> "
            "<span style='color:#E91E63;'>0</span> "
            "<span style='color:#9C27B0;'>0</span> "
            "<span style='color:#FF9800;'>0</span> "
            "<span style='color:#795548;'>0</span>"
            "<span style='color:#4CAF50;'>&gt;</span>"
            "</div>"
            # Desciption
            "The Bubble Styling used for the option dialogs that are triggered during the Swoon.exe segement with Princess Peach and Francis.<br><br>"
            "This bubble tags has some extra values associated with it that work as follows:"
            "<ul style='margin-top:5px; margin-bottom:0; padding-left:20px;'>"
            "<li><span style='color:#E91E63;'>0</span> → position on the X axis of the bubble</li>"
            "<li><span style='color:#9C27B0;'>0</span> → position on the Y axis of the bubble</li>"
            "<li><span style='color:#FF9800;'>0</span> → scale on the X axis of the bubble</li>"
            "<li><span style='color:#795548;'>0</span> → scale on the Y axis of the bubble</li>"
            "</ul>"
        )
        self.swoonselect_label = SecondaryFrame.add_text_label(layout, swoonselect_text, QtCore.Qt.AlignCenter)
        SecondaryFrame.add_image(self, layout, "Packaged_Resources/Images/Bubbles/Swoon_Select_Bubble.png", 200)

        intermission_text = (
            f"<div style=\"font-family:'{font_family}'; font-size: 10pt;\">"
            "<div style=\"font-weight:bold; font-size:12pt; margin-bottom:15px; color:#FFBF00\">"
            "<br><br>Intermission Speach Bubble"
            "</div>"
            # md code syntax
            "<div style='font-family:Courier New, monospace; font-size:14pt; margin:6px 0;'>"
            "<span style='color:#4CAF50;'>&lt;clear&gt;</span>"
            "</div>"
            # Desciption
            "The Bubble styling used at the game's intro screen for the Dark Prognosticus and Tippi backstory during Mission Intermissions.<br>In game usually nothing displays with a slight exception in the games intro, so in the editor it will always display with that exception."
        )
        self.intermission_label = SecondaryFrame.add_text_label(layout, intermission_text, QtCore.Qt.AlignCenter)
        SecondaryFrame.add_image(self, layout, "Packaged_Resources/Images/Bubbles/Intermission_Bubble.png", 400)

        diary_text = (
            f"<div style=\"font-family:'{font_family}'; font-size: 10pt;\">"
            "<div style=\"font-weight:bold; font-size:12pt; margin-bottom:15px; color:#FFBF00\">"
            "<br><br>Diary Speach Bubble"
            "</div>"
            # md code syntax
            "<div style='font-family:Courier New, monospace; font-size:14pt; margin:6px 0;'>"
            "<span style='color:#4CAF50;'>&lt;diary&gt;</span>"
            "</div>"
            # Desciption
            "The Bubble styling used at the start of each new chapter."
        )
        self.diary_label = SecondaryFrame.add_text_label(layout, diary_text, QtCore.Qt.AlignCenter)
        SecondaryFrame.add_image(self, layout, "Packaged_Resources/Images/Bubbles/Diary_Bubble.png", 400)

        mimi_text = (
            f"<div style=\"font-family:'{font_family}'; font-size: 10pt;\">"
            "<div style=\"font-weight:bold; font-size:12pt; margin-bottom:15px; color:#FFBF00\">"
            "<br><br>Mimi Speach Bubble"
            "</div>"
            # md code syntax
            "<div style='font-family:Courier New, monospace; font-size:14pt; margin:6px 0;'>"
            "<span style='color:#4CAF50;'>&lt;majo&gt;</span>"
            "</div>"
            # Desciption
            "The Bubble Styling used when Mimi transforms into \"Spider-Mimi\"."
        )
        self.mimi_label = SecondaryFrame.add_text_label(layout, mimi_text, QtCore.Qt.AlignCenter)
        SecondaryFrame.add_image(self, layout, "Packaged_Resources/Images/Bubbles/Mimi_Speach_Bubble.png", 400)
        
        #===================================================================
        # Drawing the Window
        #===================================================================
        main_layout = QVBoxLayout()
        
        # Scrollable settings content
        scrollable = SecondaryFrame.make_scrollable(layout, self, width=self.width()-10, height=self.height()-50)
        main_layout.addWidget(scrollable)
        
        # Close button outside scrollable content
        close_layout = QHBoxLayout()
        SecondaryFrame.add_button(close_layout, self, "Close", on_click=self.close, click_sound="menu_about_close", alignment=QtCore.Qt.AlignCenter, min_width=200, font=control_font)
        main_layout.addLayout(close_layout)

        # Applying the main layout
        self.setLayout(main_layout)
        debug.info("Box Type Window layout successfully initialized!")

        # Play sound when About opens
        if should_play_sounds():
            play_sound_by_name("menu_about_open")

    #===================================================================
    # Export as Method for Toolbar Button Actions
    #===================================================================
    @classmethod
    def show_box_types(cls, parent=None):
        debug.debug("Opening Box Type Window from toolbar...")

        # If instance doesn't exist create it (passing parent for positioning)
        if cls._instance is None:
            cls._instance = cls(parent)
            cls._instance.setAttribute(QtCore.Qt.WA_DeleteOnClose)

            # Reset _instance when window is destroyed
            cls._instance.destroyed.connect(lambda: setattr(cls, "_instance", None))

        # Show + bring to front
        cls._instance.show()
        cls._instance.raise_()
        cls._instance.activateWindow()

        debug.info("Box Type Window is now visible.")