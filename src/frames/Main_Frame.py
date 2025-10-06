from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTextEdit,
    QLabel, QDockWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSettings, Qt

# Project Imports
from managers.Toolbar_Manager import build_toolbar
from managers.Resource_Manager import get_external_resource, load_font
from managers.Sound_Manager import play_bgm_track
from managers.Search_Text_Manager import SearchableTextEdit
from managers.Debug_Manager import debug

from renderer.parsing.spm_parser import parse_spm_text
from renderer.ui.bubble_viewer import BubbleViewer
from renderer.ui.bubble_widget import BubbleWidget

#===================================================================================================================================
# Main Window
#===================================================================================================================================
class MainFrame(QMainWindow):

    def __init__(self):
        super().__init__()

        self._window_title = "Flint V1.0 by Luma48"
        self._init_window()
        self._init_text_editor()
        self._init_bubble_viewer()
        self._init_status_label()
        self._init_toolbar()
        self._init_bgm()

        # Add docks to main window
        self.addDockWidget(Qt.LeftDockWidgetArea, self.text_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.bubble_dock)

        self.current_file_path = None

        # Refresh bubble view from text editor
        self.refresh_view()

        debug.info("MainFrame initialized successfully!")

    # =====================================================================
    # Window setup
    # =====================================================================
    def _init_window(self):
        debug.debug("Initializing window settings...")
        self.setWindowTitle(self._window_title)
        screen_geometry = QApplication.desktop().availableGeometry()
        width = int(screen_geometry.width() * 0.75)
        height = int(screen_geometry.height() * 0.9)
        x = (screen_geometry.width() - width) // 2
        y = (screen_geometry.height() - height) // 2
        self.setGeometry(x, y, width, height)
        debug.info("Window settings initialized successfully!")

    # =====================================================================
    # Status bar
    # =====================================================================
    def _init_status_label(self):
        self.lbl_status = QLabel('<span style="font-weight:bold; font-size:12pt;">status bar ¯\\_(ツ)_/¯</span>')
        self.statusBar().addWidget(self.lbl_status)
        debug.info("Status label initialized.")

    # =====================================================================
    # Toolbar
    # =====================================================================
    def _init_toolbar(self):
        self.toolbar, self.adaptive_widgets = build_toolbar(self, self.text_editor.text_editor, self.lbl_status)
        self.addToolBar(self.toolbar)
        self.toolbar.orientationChanged.connect(self._on_toolbar_orientation_changed)
        self._update_adaptive_widgets(self.toolbar.orientation())

    def _on_toolbar_orientation_changed(self, orientation):
        for widget in self.adaptive_widgets:
            widget.update_orientation(orientation)

    def _update_adaptive_widgets(self, orientation):
        for widget in self.adaptive_widgets:
            widget.update_orientation(orientation)

    # =====================================================================
    # Background Music
    # =====================================================================
    def _init_bgm(self):
        settings = QSettings(get_external_resource("Settings.ini"), QSettings.IniFormat)
        last_track = settings.value("bgm_track", "", type=str)
        if last_track:
            play_bgm_track("Audio/BGM", last_track)

    # =====================================================================
    # Text Editor Dock (with searchbar)
    # =====================================================================
    def _init_text_editor(self):
        self.font_family = load_font("Packaged_Resources/Fonts/ProgramFont.ttf")
        custom_font = QFont(self.font_family, 12)
        
        self.text_editor = SearchableTextEdit(font=custom_font)
        self.text_editor.text_editor.setReadOnly(False)

        self.text_dock = QDockWidget("Raw Text View", self)
        self.text_dock.setWidget(self.text_editor)
        self.text_dock.setFloating(False)
        self.text_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        debug.info("Text editor dock initialized with custom font.")

    # =====================================================================
    # Bubble Viewer Dock
    # =====================================================================
    def _init_bubble_viewer(self):
        self.bubble_viewer = BubbleViewer([], self.font_family, self)
        self.bubble_dock = QDockWidget("Bubbles View", self)
        self.bubble_dock.setWidget(self.bubble_viewer)
        self.bubble_dock.setFloating(False)
        self.bubble_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        debug.info("Bubble viewer dock initialized.")

    # =====================================================================
    # Refresh bubble viewer
    # =====================================================================
    def refresh_view(self, changed_keys=None):
        debug.debug("Refreshing bubble viewer from text editor...")
        self._update_bubbles_from_current_doc()
        debug.debug("View successfully refreshed!")

    def _update_bubbles_from_current_doc(self):
        text = self.text_editor.toPlainText()
        blocks = parse_spm_text(text)
        self._clear_bubble_viewer()
        layout = self.bubble_viewer.widget().layout()
        widgets = [BubbleWidget(b, self.font_family, self.bubble_viewer) for b in blocks]
        for w in widgets:
            layout.addWidget(w)
        layout.addStretch(1)
        if widgets:
            self.bubble_viewer.set_active_bubble(widgets[0], play_sound=False)

    def _clear_bubble_viewer(self):
        layout = self.bubble_viewer.widget().layout()
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            w = item.widget()
            if w:
                w.setParent(None)
            else:
                layout.removeItem(item)

    # =====================================================================
    # Window title
    # =====================================================================
    def update_window_title(self):
        if hasattr(self, 'current_file_path') and self.current_file_path:
            self.setWindowTitle(f"{self._window_title} - {self.current_file_path}")
        else:
            self.setWindowTitle(self._window_title)

    # =====================================================================
    # Close event
    # =====================================================================
    def closeEvent(self, event):
        QApplication.quit()
        super().closeEvent(event)