# graph_editor_toggle_tab.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget

class GraphEditorToggleTab(QWidget):
    """Toggle tab widget to expand/collapse the GraphEditor."""
    toggled = pyqtSignal()

    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self._setup_layout()
        self._setup_components()

    def _setup_components(self):
        self.label = QLabel("Editor", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.layout.addWidget(self.label)

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def mousePressEvent(self, event) -> None:
        toggler = self.sequence_widget.toggler
        if toggler:
            toggler.toggle()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._resize_graph_editor_toggler()

    def _resize_graph_editor_toggler(self):
        self.setFixedHeight(self.sequence_widget.height() // 20)
        font_size = self.height() // 3
        font = QFont()
        font.setPointSize(font_size)
        self.label.setFont(font)
        family = "Georgia"
        self.label.setFont(QFont(family, font_size))
        self.setStyleSheet("background-color: white")

    def enterEvent(self, event) -> None:
        self.setStyleSheet("background-color: lightgray; border: 1px solid black;")
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self.setStyleSheet("background-color: white; border: none;")
        super().leaveEvent(event)
