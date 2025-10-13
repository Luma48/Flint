from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,QLineEdit, QPushButton, QTextEdit, QLabel)
from PyQt5.QtGui import QTextCursor, QFont, QColor
from PyQt5.QtCore import Qt

# Project Imports
from managers.Sound_Manager import play_sound_by_name, should_play_sounds
from renderer.ui.bubble_viewer import BubbleViewer

class SearchableTextEdit(QWidget):
    def __init__(self, font: QFont = None, parent=None):
        super().__init__(parent)

        self.matches = []
        self.current_match_index = -1

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Search bar layout
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        search_layout.addWidget(self.search_input)

        self.prev_btn = QPushButton("Previous")
        self.next_btn = QPushButton("Next")

        # Add tooltips for hotkeys
        self.prev_btn.setToolTip("Previous match (Shift+F3)")
        self.next_btn.setToolTip("Next match (F3)")

        search_layout.addWidget(self.prev_btn)
        search_layout.addWidget(self.next_btn)

        # Match counter label
        self.match_label = QLabel("")
        search_layout.addWidget(self.match_label)

        if font:
            # Main editor font
            self.text_editor = QTextEdit()
            self.text_editor.setFont(font)

            # Smaller font for search UI
            small_font = QFont(font)
            small_font.setPointSize(max(8, font.pointSize() - 2))
            self.search_input.setFont(small_font)
            self.prev_btn.setFont(small_font)
            self.next_btn.setFont(small_font)
            self.match_label.setFont(small_font)
        else:
            self.text_editor = QTextEdit()

        self.layout.addLayout(search_layout)
        self.layout.addWidget(self.text_editor)

        # Signals
        self.search_input.textChanged.connect(self.update_matches)
        self.search_input.returnPressed.connect(self.goto_next)
        self.next_btn.clicked.connect(self.goto_next)
        self.prev_btn.clicked.connect(self.goto_previous)

    # =====================================================================
    # Capture F3 / Shift+F3 for navigation
    # =====================================================================
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F3:
            if event.modifiers() & Qt.ShiftModifier:
                self.goto_previous()
            else:
                self.goto_next()
        else:
            super().keyPressEvent(event)

    # =====================================================================
    # Update match positions without changing cursor focus
    # =====================================================================
    def update_matches(self):
        text = self.search_input.text()
        self.matches.clear()
        self.current_match_index = -1

        if not text:
            self.match_label.setText("")
            self.text_editor.setExtraSelections([])
            return

        cursor = self.text_editor.textCursor()
        cursor.movePosition(QTextCursor.Start)
        doc_cursor = self.text_editor.document().find(text, cursor)

        while not doc_cursor.isNull():
            self.matches.append((doc_cursor.selectionStart(), doc_cursor.selectionEnd()))
            doc_cursor = self.text_editor.document().find(text, doc_cursor)

        if self.matches:
            self.current_match_index = 0
            self.highlight_all_matches()

        self.update_match_label()

    # =====================================================================
    # Show 'X of Y' matches
    # =====================================================================
    def update_match_label(self):
        if not self.matches:
            self.match_label.setText("0 matches")
        else:
            self.match_label.setText(
                f"{self.current_match_index+1} of {len(self.matches)}"
            )

    # =====================================================================
    # Highlight all matches in grey (no orange for current match)
    # =====================================================================
    def highlight_all_matches(self):
        extra_selections = []
        search_text = self.search_input.text()

        for (start, end) in self.matches:
            selection = QTextEdit.ExtraSelection()
            cursor = self.text_editor.textCursor()
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.KeepAnchor)
            selection.cursor = cursor

            # All matches use the same color now
            selection.format.setBackground(QColor("lightgray"))

            extra_selections.append(selection)

        self.text_editor.setExtraSelections(extra_selections)

        # Move cursor to the current match
        if self.current_match_index >= 0:
            start, end = self.matches[self.current_match_index]
            cursor = self.text_editor.textCursor()
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.KeepAnchor)
            self.text_editor.setTextCursor(cursor)

        self.update_match_label()

    # =====================================================================
    # Button Actions
    # =====================================================================
    def goto_next(self):
        if not self.matches:
            return
        self.current_match_index = (self.current_match_index + 1) % len(self.matches)
        self.highlight_all_matches()
        if should_play_sounds():
                    play_sound_by_name("menu_message_skip")

    def goto_previous(self):
        if not self.matches:
            return
        self.current_match_index = (self.current_match_index - 1) % len(self.matches)
        self.highlight_all_matches()
        if should_play_sounds():
                    play_sound_by_name("menu_message_skip")

    def toPlainText(self):
        return self.text_editor.toPlainText()

    def setPlainText(self, text):
        self.text_editor.setPlainText(text)


class SearchableBubbleViewer(QWidget):
    def __init__(self, bubble_viewer: BubbleViewer, font: QFont = None, parent=None):
        super().__init__(parent)
        self.bubble_viewer = bubble_viewer
        self.matches = []
        self.current_match_index = -1

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Search bar layout
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by ID (stg1_1_000)...")
        search_layout.addWidget(self.search_input)

        self.prev_btn = QPushButton("Previous")
        self.next_btn = QPushButton("Next")
        self.prev_btn.setToolTip("Previous match (Shift+F3)")
        self.next_btn.setToolTip("Next match (F3)")
        search_layout.addWidget(self.prev_btn)
        search_layout.addWidget(self.next_btn)

        self.match_label = QLabel("")
        search_layout.addWidget(self.match_label)

        if font:
            small_font = QFont(font)
            small_font.setPointSize(max(8, font.pointSize() - 2))
            self.search_input.setFont(small_font)
            self.prev_btn.setFont(small_font)
            self.next_btn.setFont(small_font)
            self.match_label.setFont(small_font)

        self.layout.addLayout(search_layout)
        self.layout.addWidget(self.bubble_viewer)

        # Signals
        self.search_input.textChanged.connect(self.update_matches)
        self.search_input.returnPressed.connect(self.goto_next)
        self.next_btn.clicked.connect(self.goto_next)
        self.prev_btn.clicked.connect(self.goto_previous)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F3:
            if event.modifiers() & Qt.ShiftModifier:
                self.goto_previous()
            else:
                self.goto_next()
        else:
            super().keyPressEvent(event)

    def update_matches(self):
        text = self.search_input.text().strip()
        self.matches.clear()
        self.current_match_index = -1

        if not text:
            self.match_label.setText("")
            return

        for bubble in self.bubble_viewer.get_all_bubbles():
            if text.lower() in bubble.block.stage_npc.lower():
                self.matches.append(bubble)

        # Only update match count; do NOT jump to the first match automatically
        self._update_match_label()

    def _update_match_label(self):
        if not self.matches:
            self.match_label.setText("0 matches")
        else:
            display_index = self.current_match_index + 1 if self.current_match_index >= 0 else 0
            self.match_label.setText(f"{display_index} of {len(self.matches)}")

    def _highlight_current(self):
        if self.current_match_index < 0 or not self.matches:
            return
        bubble = self.matches[self.current_match_index]
        self.bubble_viewer.set_active_bubble(bubble)
        self.bubble_viewer.scroll_to_bubble(bubble)
        self._update_match_label()
        if should_play_sounds():
            play_sound_by_name("menu_cursor_move")

    def goto_next(self):
        if not self.matches:
            return
        self.current_match_index = (self.current_match_index + 1) % len(self.matches)
        self._highlight_current()

    def goto_previous(self):
        if not self.matches:
            return
        self.current_match_index = (self.current_match_index - 1) % len(self.matches)
        self._highlight_current()