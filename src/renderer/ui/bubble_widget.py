from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextBrowser
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

# Project Imports
from renderer.models.bubble_block import BubbleBlock
from renderer.utils.text_renderer import render_text_with_tags
from renderer.utils.bubble_assets import bubble_image_path
from renderer.ui.param_box import ParamBox
from managers.Resource_Manager import get_resource
from managers.Sound_Manager import play_sound_by_name, should_play_sounds

#===================================================================================================================================
# Bubble Widget
#===================================================================================================================================
class BubbleWidget(QWidget):
    def __init__(self, block: BubbleBlock, font_family: str, viewer, parent=None):
        super().__init__(parent)
        self.block = block
        self.viewer = viewer
        self.current_page = 0
        self.cursor_visible = False
        self.cursor_frame_index = 0

        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 18)
        outer.setSpacing(6)

        # =====================================================================
        # Meta row (aka the Paramboxes data)
        # =====================================================================
        meta_row = QHBoxLayout()
        meta_row.setSpacing(8)
        meta_row.addStretch(1)
        meta_row.addWidget(ParamBox(block.stage_npc, font_family))

        type_display_map = {
            "none": "Normal",
            "housou": "Robo",
            "fairy": "Tippi",
            "fairy2": "Pixl",
            "diary": "Diary",
            "system": "System",
            "select": "Select",
            "kanban": "Signpost",
            "majo": "Mimi",
            "adv": "Swoon.exe",
            "adv_select": "Swoon.exe Select",
            "clear": "Intermission",
            "small": "Small",
        }
        bubble_type_text = type_display_map.get(block.bubble_type, block.bubble_type)
        meta_row.addWidget(ParamBox(bubble_type_text, font_family))

        x, y, w, h = block.position
        pos_text = f"{x} {y} {w} {h}" if any((x, y, w, h)) else "auto"
        meta_row.addWidget(ParamBox(pos_text, font_family))

        bubble_sound_text = block.bubble_sound.capitalize()
        meta_row.addWidget(ParamBox(bubble_sound_text, font_family))
        meta_row.addStretch(1)
        outer.addLayout(meta_row)

        # =====================================================================
        # Bubble background
        # =====================================================================
        bubble_img = bubble_image_path(block.bubble_type)
        pixmap = QPixmap(bubble_img)
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(pixmap)

        if block.bubble_type in ("select", "adv_select"):
            self.bg_label.setFixedSize(pixmap.size())
            self.bg_label.setScaledContents(False)
        else:
            self.bg_label.setScaledContents(True)
            if w > 0 and h > 0:
                self.bg_label.setFixedSize(w, h)
            else:
                self.bg_label.setFixedSize(pixmap.size())

        outer.addWidget(self.bg_label, alignment=Qt.AlignHCenter)

        # =====================================================================
        # Text Label inside bubble -> use QTextBrowser to support icons
        # =====================================================================
        self.text_label = QTextBrowser(self.bg_label)
        self.text_label.setOpenExternalLinks(False)
        self.text_label.setFrameStyle(0)
        self.text_label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_label.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_label.setFont(QFont(font_family, 12))

        if block.bubble_type in ("system", "majo", "adv", "adv_select", "clear"):
            self.text_label.setStyleSheet("QTextBrowser { color: white; background: transparent; }")
        else:
            self.text_label.setStyleSheet("QTextBrowser { color: black; background: transparent; }")

        # Margins for text
        self.margin_x = max(40, int(self.bg_label.width() * 0.02))
        self.margin_y_top = max(25, int(self.bg_label.height() * 0.18))
        self.margin_y_bottom = max(20, int(self.bg_label.height() * 0.04))
        self.text_label.setGeometry(
            self.margin_x,
            self.margin_y_top,
            self.bg_label.width() - (2 * self.margin_x),
            self.bg_label.height() - (self.margin_y_top + self.margin_y_bottom),
        )

        # =====================================================================
        # Page Counter
        # =====================================================================
        self.page_counter = QLabel(self.bg_label)
        self.page_counter.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.page_counter.setFont(QFont(font_family, 9))
        self.page_counter.setStyleSheet("QLabel { color: gray; background: transparent; }")

        # =====================================================================
        # Cursor Animation
        # =====================================================================
        self.cursor_label = QLabel(self.bg_label)
        self.cursor_frames = [
            QPixmap(get_resource("Packaged_Resources/Images/Icons/Crusor_1.png")),
            QPixmap(get_resource("Packaged_Resources/Images/Icons/Crusor_2.png")),
            QPixmap(get_resource("Packaged_Resources/Images/Icons/Crusor_3.png")),
            QPixmap(get_resource("Packaged_Resources/Images/Icons/Crusor_4.png")),
            QPixmap(get_resource("Packaged_Resources/Images/Icons/Crusor_5.png")),
        ]
        self.cursor_label.setPixmap(self.cursor_frames[0])
        self.cursor_label.setScaledContents(True)
        self.cursor_label.setGeometry(self.bg_label.width() - 36 - 2, 6, 32, 32)
        self.cursor_label.hide()

        self.cursor_timer = QTimer(self)
        self.cursor_timer.timeout.connect(self._animate_cursor)
        self.cursor_timer.start(150)

        self.setFocusPolicy(Qt.StrongFocus)
        self._render_page()

    # =====================================================================
    # Highlighting for search
    # =====================================================================
    def get_text(self) -> str:
        return "\n".join(self.block.pages) if self.block.pages else ""

    def set_highlight(self, active: bool):
        if active:
            self.setStyleSheet("QWidget { border: 3px solid yellow; }")
        else:
            self.setStyleSheet("")

    # =====================================================================
    # Page rendering
    # =====================================================================
    def _render_page(self):
        raw_text = self.block.pages[self.current_page] if self.block.pages else ""
        if self.block.bubble_type in ("select", "adv_select"):
            options = raw_text.split("\n")
            html_lines = [f"• {opt.strip()}" for opt in options if opt.strip()]
            processed = "<br>".join(html_lines)
        else:
            raw_text = raw_text.replace("\n", "<br>")
            processed = render_text_with_tags(raw_text, 20)
        line_spacing = 1.3
        html_text = f'<div style="line-height: {line_spacing};">{processed}</div>'
        self.text_label.setHtml(html_text)

        if len(self.block.pages) > 1:
            self.page_counter.setText(f"{self.current_page + 1}/{len(self.block.pages)}")
            self.page_counter.show()
            self._position_page_counter()
        else:
            self.page_counter.hide()

    # =====================================================================
    # Input Handling
    # =====================================================================
    def mousePressEvent(self, event):
        if self.viewer:
            self.viewer.set_active_bubble(self)
        if event.button() == Qt.LeftButton and self.current_page < len(self.block.pages) - 1:
            self.current_page += 1
            self._render_page()
            if should_play_sounds():
                play_sound_by_name("menu_message_skip")
        elif event.button() == Qt.RightButton and self.current_page > 0:
            self.current_page -= 1
            self._render_page()
            if should_play_sounds():
                play_sound_by_name("menu_message_skip")

    def resizeEvent(self, event):
        self.text_label.setGeometry(
            self.margin_x,
            self.margin_y_top,
            self.bg_label.width() - (2 * self.margin_x),
            self.bg_label.height() - (self.margin_y_top + self.margin_y_bottom),
        )
        self._position_page_counter()
        super().resizeEvent(event)

    def showEvent(self, event):
        self._position_page_counter()
        super().showEvent(event)

    def _position_page_counter(self):
        if not self.page_counter.isVisible():
            return
        fm = self.page_counter.fontMetrics()
        w = fm.horizontalAdvance(self.page_counter.text()) + 8
        h = fm.height() + 2
        x = self.bg_label.width() - self.margin_x - w
        y = self.bg_label.height() - self.margin_y_bottom - h - 2
        self.page_counter.setGeometry(x, y, w, h)

    def _animate_cursor(self):
        if self.cursor_visible:
            self.cursor_frame_index = (self.cursor_frame_index + 1) % len(self.cursor_frames)
            self.cursor_label.setPixmap(self.cursor_frames[self.cursor_frame_index])

    def set_cursor_visible(self, visible: bool):
        self.cursor_visible = visible
        self.cursor_label.setVisible(visible)
