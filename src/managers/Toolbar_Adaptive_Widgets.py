from PyQt5.QtWidgets import QWidget, QBoxLayout, QFrame, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Project Imports
from managers.Debug_Manager import debug
from managers.Resource_Manager import load_font

#===================================================================================================================================
# The Class Handlling the Adaptivity of the Labels for Toolbar Elements
#===================================================================================================================================
class AdaptiveLabel(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        debug.debug("Creating AdaptiveLabel with text: '%s'...", text)

        self.label = QLabel(text)
        label_font = QFont(load_font("Packaged_Resources/Fonts/ProgramFont.ttf"), 8)
        self.label.setFont(label_font)
        self.layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.layout.setContentsMargins(5, 0, 5, 0)
        self.layout.addWidget(self.label, alignment=Qt.AlignVCenter)
        self.setLayout(self.layout)
        self.update_orientation(Qt.Horizontal)
        
        debug.debug("Created AdaptiveLabel %s", text)

    def update_orientation(self, toolbar_orientation):
        if toolbar_orientation == Qt.Horizontal:
            self.layout.setDirection(QBoxLayout.LeftToRight)
            self.label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            debug.debug("AdaptiveLabel orientation set to Horizontal for text: '%s'", self.label.text())
        else:
            self.layout.setDirection(QBoxLayout.TopToBottom)
            self.label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            debug.debug("AdaptiveLabel orientation set to Vertical for text: '%s'", self.label.text())

#===================================================================================================================================
# The Class Handlling the Adaptivity of the Separators for Toolbar Elements
#===================================================================================================================================
class AdaptiveSeparator(QWidget):
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(parent)
        debug.debug("Creating AdaptiveSeparator with orientation: %s", "Horizontal" if orientation == Qt.Horizontal else "Vertical")
        
        self.line = QFrame()
        self.layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.layout.setContentsMargins(5, 0, 5, 0)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.line)
        self.setLayout(self.layout)
        self.update_orientation(orientation)

        debug.debug("Created AdaptiveSeparator")
        
    def update_orientation(self, orientation):
        if orientation == Qt.Horizontal:
            self.line.setFrameShape(QFrame.VLine)
            self.line.setFixedHeight(25)
            self.line.setFixedWidth(2)
            self.line.setLineWidth(27)
            self.layout.setDirection(QBoxLayout.LeftToRight)
            debug.debug("AdaptiveSeparator updated to Horizontal orientation")
        else:
            self.line.setFrameShape(QFrame.HLine)
            self.line.setFixedHeight(10)
            self.line.setFixedWidth(100)
            self.line.setLineWidth(1)
            self.layout.setDirection(QBoxLayout.TopToBottom)
            debug.debug("AdaptiveSeparator updated to Vertical orientation")

        self.line.setFrameShadow(QFrame.Sunken)