from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QEvent
from .visibility_button import VisibilityButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..visibility_tab import VisibilityTab


class VisibilityButtonsWidget(QWidget):
    glyph_buttons: dict[str, VisibilityButton] = {}
    non_radial_button: VisibilityButton = None
    glyph_names = ["TKA", "Reversals", "VTG", "Elemental", "Positions"]
    grid_name = "Non-radial points"

    def __init__(self, visibility_tab: "VisibilityTab"):
        super().__init__()
        self.visibility_tab = visibility_tab
        self.toggler = visibility_tab.toggler

        self._create_buttons()
        self._setup_layout()
        self.update_buttons()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addStretch(4)
        for button in self.glyph_buttons.values():
            self.layout.addWidget(button)
            self.layout.addStretch(1)
        if self.non_radial_button:
            self.layout.addWidget(self.non_radial_button)
            self.layout.addStretch(1)
        self.layout.addStretch(3)

    def _create_buttons(self):
        for name in self.glyph_names:
            button = VisibilityButton(name, self)
            self.glyph_buttons[name] = button
        self.non_radial_button = VisibilityButton(self.grid_name, self)

    def update_buttons(self):
        """Synchronize buttons with the current visibility settings."""
        settings = self.visibility_tab.main_widget.settings_manager.visibility
        for name, button in self.glyph_buttons.items():
            button.is_toggled = settings.get_glyph_visibility(name)
            button._apply_styles()
        if self.non_radial_button:
            self.non_radial_button.is_toggled = settings.get_non_radial_visibility()
            self.non_radial_button._apply_styles()
            
    def resizeEvent(self, event: QEvent):
        width = self.visibility_tab.width()
        font_size = width // 40
        font = QFont()
        font.setPointSize(font_size)

        for button in self.glyph_buttons.values():
            button.setFont(font)

        if self.non_radial_button:
            self.non_radial_button.setFont(font)

        super().resizeEvent(event)
