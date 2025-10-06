from typing import List
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea
)

# Project Imports
from managers.Debug_Manager import debug
from renderer.ui.bubble_widget import BubbleWidget, BubbleBlock
from managers.Sound_Manager import play_sound_by_name, should_play_sounds

#===================================================================================================================================
# Bubble Viewer
#===================================================================================================================================
class BubbleViewer(QScrollArea):
    def __init__(self, blocks: List[BubbleBlock], font_family: str, parent=None):
        super().__init__(parent)
        debug.debug("Initializing BubbleViewer with %d blocks", len(blocks))
        self.setWidgetResizable(True)
        self.active_bubble = None

        container = QWidget()
        lay = QVBoxLayout(container)
        lay.setContentsMargins(12, 12, 24, 24)
        lay.setSpacing(18)

        self.bubble_widgets: List[BubbleWidget] = []
        for index, b in blocks:
            widget = BubbleWidget(b, font_family, self)
            lay.addWidget(widget)
            self.bubble_widgets.append(widget)
            debug.info("Added BubbleWidget %d: '%s'", index, b.stage_npc)

        lay.addStretch(1)
        self.setWidget(container)

        if self.bubble_widgets:
            debug.info("Setting first bubble as active")
            self.set_active_bubble(self.bubble_widgets[0], play_sound=False)

    def set_active_bubble(self, bubble: BubbleWidget, play_sound: bool = True):
        if self.active_bubble is bubble:
            debug.info("Bubble '%s' is already active, skipping", bubble.block.stage_npc)
            return
        if self.active_bubble:
            debug.debug("Deactivating previous bubble: '%s'", self.active_bubble.block.stage_npc)
            self.active_bubble.set_cursor_visible(False)
        self.active_bubble = bubble
        self.active_bubble.set_cursor_visible(True)
        debug.info("Active bubble set to: '%s'", bubble.block.stage_npc)
        if play_sound and should_play_sounds():
            play_sound_by_name("menu_cursor_move")