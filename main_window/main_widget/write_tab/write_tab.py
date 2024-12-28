from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from .act_browser.act_browser import ActBrowser

if TYPE_CHECKING:
    from ..main_widget import MainWidget


class WriteTab(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.act_browser = ActBrowser(self)
        self.setAcceptDrops(False)
        layout = QHBoxLayout(self)
        layout.addWidget(self.act_browser, 4)
        self.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
