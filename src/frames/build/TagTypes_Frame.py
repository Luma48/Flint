from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
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
class TagTypes(QWidget):
    # Class level reference
    _instance = None

    # Regular icon resources
    tag_icons = {
        "SHAKE": ("Icon_Shake.png", "Shake Icon"),
        "WAVE": ("Icon_Wave.png", "Wave Icon"),
        "DYNAMIC": ("Icon_Dynamic.png", "Dynamic Icon"),
        "WAIT": ("Icon_Wait.png", "Wait Icon"),
    }

    def __init__(self, parent=None):
        debug.debug("Initializing Tag Types Window...")
        
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
        self.setWindowTitle("Tag Types")
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
        SecondaryFrame.add_image(self, layout, "Packaged_Resources/Images/Editor/TagType.png", 200)

        # Title label
        title_text = (
            f"<span style=\"font-family:'{font_family}'; font-weight:bold; font-size:16pt;\">"
            "Super Paper Mario<br>"
            "Tag Types"
            "</span>"
        )
        self.title_label = SecondaryFrame.add_text_label(layout, title_text, QtCore.Qt.AlignCenter)

        behaviour_flow = (
            f"<div style=\"font-family:'{font_family}'; font-size: 10pt;\">"
            "<div style=\"font-weight:bold; font-size:12pt; margin-bottom:15px; color:#FFBF00\">"
            "<br><br>Text Behavior & Flow"
            "</div>"
            "<ul style='margin-top:5px; margin-bottom:0; padding-left:20px;'>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;k&gt;</span> → Pauses page transition until the 2 Button is pressed.</li>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;keyyon&gt;</span> → Pauses page transition until the A Button is pressed (tippi tattles).</li>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;p&gt;</span> → Defines and automatically transistions to the next page.</li>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;o&gt;</span> → Defines an option dialog to be opened after the end of the bubble (it needs to have one that follows or the game will crash).</li>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;shake&gt;&lt;/shake&gt;</span> → Enclosed text shakes erratically.</li>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;wave&gt;&lt;/wave&gt;</span> → Enclosed text moves sinusoidally.</li>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;dynamic 3&gt;&lt;/dynamic&gt;</span> → Enclosed text scales down quickly into view.</li>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;wait </span><span style=\"color:#2196F3; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">int</span><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&gt;</span> → Temporarily pause the text flow for the specified time in ms.</li>"
            "</ul>"
            "</div><br>"
        )
        self.behaviour_flow = SecondaryFrame.add_text_label(layout, behaviour_flow, QtCore.Qt.AlignCenter)

        appearence_formatting = (
            f"<div style=\"font-family:'{font_family}'; font-size: 10pt;\">"
            "<div style=\"font-weight:bold; font-size:12pt; margin-bottom:15px; color:#FFBF00\">"
            "<br><br>Appearance & Formatting"
            "</div>"
            "<ul style='margin-top:5px; margin-bottom:0; padding-left:20px;'>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;center&gt;&lt;/center&gt;</span> → Enclosed text is centered.</li>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;col </span><span style=\"color:#2196F3; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">ffffff</span><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&gt;&lt;/col&gt;</span> → Enclosed text changes color using hex values to define said color.</li>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;scale </span><span style=\"color:#2196F3; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">float</span><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&gt;&lt;/scale&gt;</span> → Enclosed text is scaled up or down using a floating point value.</li>"
            "</ul>"
            "</div><br>"
        )
        self.appearence_formatting = SecondaryFrame.add_text_label(layout, appearence_formatting, QtCore.Qt.AlignCenter)

        grammer_content = (
            f"<div style=\"font-family:'{font_family}'; font-size: 10pt;\">"
            "<div style=\"font-weight:bold; font-size:12pt; margin-bottom:15px; color:#FFBF00\">"
            "<br><br>Grammer & Content"
            "</div>"
            "<ul style='margin-top:5px; margin-bottom:0; padding-left:20px;'>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;AN&gt;</span> → Displays “a” or “an” depending on context.</li>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;ITEM&gt;</span> →Displays the current items name (used in the shop).</li>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;AN_ITEM&gt;</span> → Combines &lt;AN&gt; and &lt;ITEM&gt; functionality.</li>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;NUM&gt;</span> → Displays the players number of coins (used in the shop).</li>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;S&gt;</span> →Displays “s” or nothing depending on context.</li>"
            "</ul>"
            "</div><br>"
        )
        self.grammer_content = SecondaryFrame.add_text_label(layout, grammer_content, QtCore.Qt.AlignCenter)

        misc = (
            f"<div style=\"font-family:'{font_family}'; font-size: 10pt;\">"
            "<div style=\"font-weight:bold; font-size:12pt; margin-bottom:15px; color:#FFBF00\">"
            "<br><br>Misc"
            "</div>"
            "<ul style='margin-top:5px; margin-bottom:0; padding-left:20px;'>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;se 1&gt;</span><span style=\"color:#2196F3; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\"> and </span><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;se 2&gt;</span> → Defines the sound type to either a Typewriter or a Pencil.</li>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;ITEM&gt;</span> →Displays the current items name (used in the shop).</li>"
            "<li><span style=\"color:#4CAF50; font-family:'Courier New', monospace; font-size:16pt; margin:6px 0;\">&lt;dkey&gt;&lt;/dkey&gt;</span> → Allows an input to skip the &lt;wait&gt; time. It always encapsulates &lt;wait&gt; tags.</li>"
            "</ul>"
            "</div><br>"
        )
        self.misc = SecondaryFrame.add_text_label(layout, misc, QtCore.Qt.AlignCenter)
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
        debug.info("Tag Type Window layout successfully initialized!")

        # Play sound when About opens
        if should_play_sounds():
            play_sound_by_name("menu_about_open")

    #===================================================================
    # Export as Method for Toolbar Button Actions
    #===================================================================
    @classmethod
    def show_tag_types(cls, parent=None):
        debug.debug("Opening Tag Type Window from toolbar...")

        # If instance doesn't exist create it
        if cls._instance is None:
            cls._instance = cls(parent)
            cls._instance.setAttribute(QtCore.Qt.WA_DeleteOnClose)

            # Reset _instance when window is destroyed
            cls._instance.destroyed.connect(lambda: setattr(cls, "_instance", None))

        # Show + bring to front
        cls._instance.show()
        cls._instance.raise_()
        cls._instance.activateWindow()

        debug.info("Tag Type Window is now visible.")