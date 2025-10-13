from PyQt5.QtWidgets import QDialog, QVBoxLayout
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
class About(QDialog):
    def __init__(self, parent=None):
        debug.debug("Initializing About Window...")
        super().__init__(parent)

        #===================================================================
        # Basic Window Params
        #===================================================================
        self.setWindowTitle("About Flint")
        SecondaryFrame.set_fixed_size(self, parent, 0.5, 0.7)

        # Main layout
        layout = QVBoxLayout()

        # Custom font
        font_family = load_font("Packaged_Resources/Fonts/ProgramFont.ttf")
        control_font = QFont(font_family, 8)
    
        #===================================================================
        # Window Body
        #===================================================================
        # Add image
        SecondaryFrame.add_image(self, layout, "Packaged_Resources/Images/Editor/About.png", 200)

        # Title label
        title_text = (
            f"<span style=\"font-family:'{font_family}'; font-weight:bold; font-size:16pt;\">"
            "Flint V1.3"
            "</span>"
        )
        self.title_label = SecondaryFrame.add_text_label(layout, title_text, QtCore.Qt.AlignCenter)

        # Developer label
        dev_text = (
            f"<span style=\"font-family:'{font_family}'; font-weight:bold; font-size:10pt;\">"
            "Developed by <span style='color:#FFA500;'>Luma48</span><br>"
            '<a href="https://github.com/Luma48/Flint">Github: https://github.com/Luma48/Flint</a><br>'
            '<a href="https://www.youtube.com/watch?v=vpHN_rumHqc&t=1s">YouTube: Flint Trailer</a>'
            "</span>"
        )
        self.dev_label = SecondaryFrame.add_text_label(layout, dev_text, QtCore.Qt.AlignCenter)

        # Project description
        project_text = (
            f"<span style=\"font-family:'{font_family}'; font-weight:bold; font-size:10pt;\">"
            "A part of the <span style='color:#FF0000;'>CragonSuit</span><br> for <span style='color:#FF0000;'>Super Paper Mario Modding.</span>"
            "</span>"
        )
        self.project_label = SecondaryFrame.add_text_label(layout, project_text, QtCore.Qt.AlignCenter)

        # Artwork credit
        art_text = (
            f"<span style=\"font-family:'{font_family}'; font-weight:bold; font-size:10pt;\">"
            "Special thanks to <span style='color:#2196F3;'>SandalChannel</span> for all the amazing Luma artwork and Linux bug testing.<br>The final result wouldn't be possible without them!<br>"
            '<a href="https://www.youtube.com/@SandalChannel">Visit: SandalChannel on YouTube</a>'
            "</span>"
        )
        self.art_label = SecondaryFrame.add_text_label(layout, art_text, QtCore.Qt.AlignCenter)

        #===================================================================
        # Close/Open Buttons
        #===================================================================
        SecondaryFrame.add_button(layout, self, "Close", on_click=self.close, click_sound="menu_about_close", alignment=QtCore.Qt.AlignCenter, min_width=200, font=control_font)
        
        #===================================================================
        # Drawing the Window
        #===================================================================
        self.setLayout(layout)
        debug.info("About Window layout successfully initialized!")

        # Play sound when About opens
        if should_play_sounds():
            play_sound_by_name("menu_about_open")

    #===================================================================
    # Export as Method for Toolbar Button Actions
    #===================================================================
    @classmethod
    def show_about(cls, parent=None):
        debug.debug("Opening About Window from toolbar...")
        about = cls(parent)
        about.exec_()
        debug.info("About Window Closed!")