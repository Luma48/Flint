from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap, QFont, QFontMetrics
from PyQt5.QtCore import Qt

# Project Imports
from managers.Resource_Manager import get_resource
from managers.Debug_Manager import debug

#===================================================================================================================================
# ParamBox widget
#===================================================================================================================================
class ParamBox(QWidget):
    def __init__(self, text: str, font_family: str, parent=None):
        super().__init__(parent)
        #debug.debug("Creating ParamBox with text: '%s' and font: '%s'", text, font_family)

        # Background and Text labels
        self.bg_label = QLabel(self)
        self.text_label = QLabel(text, self)
        #debug.debug("Initialized background and text labels")

        # Font Settings
        font = QFont(font_family, 10)
        self.text_label.setFont(font)
        self.text_label.setStyleSheet("QLabel { color: white; background: transparent; }")
        self.text_label.setAlignment(Qt.AlignCenter)
        #debug.debug("Font set for text label: family='%s', size=%d", font_family, font.pointSize())

        # Measure font and add padding (width and height)
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance(text) + 20
        text_height = fm.height() + 8
        #debug.debug("Calculated ParamBox size: width=%d, height=%d", text_width, text_height)

        # Setting Background Label Image
        pixmap = QPixmap(get_resource("Packaged_Resources/Images/Bubbles/ParamBox.png"))
        self.bg_label.setPixmap(pixmap)
        self.bg_label.setScaledContents(True)

        # Fixes widget size to fit calculated size + padding, layers both labels in widget
        self.setFixedSize(text_width, text_height)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.text_label.setGeometry(0, 0, self.width(), self.height())
        #debug.debug("ParamBox geometry set: width=%d, height=%d", self.width(), self.height())

    # Manual resizer
    def resizeEvent(self, event):
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.text_label.setGeometry(0, 0, self.width(), self.height())
        #debug.debug("ParamBox resized: width=%d, height=%d", self.width(), self.height())
        super().resizeEvent(event)