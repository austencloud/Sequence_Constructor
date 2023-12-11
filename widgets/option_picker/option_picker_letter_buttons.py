from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QFont
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtSvg import QSvgRenderer
from data.letter_engine_data import letter_types
from settings.string_constants import LETTER_SVG_DIR
from typing import TYPE_CHECKING, List

from utilities.TypeChecking.Letters import Letters

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.option_picker.option_picker import OptionPickerWidget


class OptionPickerLetterButtons(QFrame):
    def __init__(
        self, main_widget: "MainWidget", option_picker: "OptionPickerWidget"
    ) -> None:
        super().__init__()
        self.main_widget = main_widget

        self.option_picker = option_picker
        self.init_letter_buttons_layout()

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def init_letter_buttons_layout(self) -> None:
        letter_buttons_layout = QVBoxLayout()
        letter_buttons_layout.setSpacing(int(0))
        self.setContentsMargins(0, 0, 0, 0)
        letter_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.row_layouts: List[
            QHBoxLayout
        ] = []  # Add this line to initialize the list of row layouts

        self.letter_rows = [
            # Type 1 - Dual-Shift
            ["A", "B", "C"],
            ["D", "E", "F"],
            ["G", "H", "I"],
            ["J", "K", "L"],
            ["M", "N", "O"],
            ["P", "Q", "R"],
            ["S", "T", "U", "V"],
            # Type 2 - Shift
            ["W", "X", "Y", "Z"],
            ["Σ", "Δ", "θ", "Ω"],
            # Type 3 - Cross-Shift
            ["W-", "X-", "Y-", "Z-"],
            ["Σ-", "Δ-", "θ-", "Ω-"],
            # Type 4 - Dash
            ["Φ", "Ψ", "Λ"],
            # Type 5 - Dual-Dash
            ["Φ-", "Ψ-", "Λ-"],
            # Type 6 - Static
            ["α", "β", "Γ"],
        ]

        for row in self.letter_rows:
            row_layout = QHBoxLayout()
            self.row_layouts.append(
                row_layout
            )  # Add this line to add the row layout to the list

            for letter in row:
                letter_type = self.get_letter_type(letter)
                icon_path = self.get_icon_path(letter_type, letter)
                button = self.create_button(icon_path)
                row_layout.addWidget(button)

            letter_buttons_layout.addLayout(row_layout)

        self.letter_buttons_layout = letter_buttons_layout
        self.setLayout(letter_buttons_layout)

    def get_letter_type(self, letter: str) -> str:
        for letter_type in letter_types:
            if letter in letter_types[letter_type]:
                return letter_type
        return ""

    def get_icon_path(self, letter_type: str, letter: Letters) -> str:
        return f"{LETTER_SVG_DIR}/{letter_type}/{letter}.svg"

    def create_button(self, icon_path: str) -> QPushButton:
        renderer = QSvgRenderer(icon_path)
        pixmap = QPixmap(renderer.defaultSize())
        pixmap.fill(QColor(Qt.GlobalColor.transparent))
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        button = QPushButton(QIcon(pixmap), "", self.main_widget)

        button.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                border: none;
                border-radius: 0px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #e6f0ff;
            }
            QPushButton:pressed {
                background-color: #cce0ff;
            }
            """
        )
        button.setFlat(True)
        font = QFont()
        font.setPointSize(int(20))
        button.setFont(font)
        return button

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.update_letter_buttons_size()

    def update_letter_buttons_size(self) -> None:
        button_row_count = len(self.letter_rows)
        available_height = int(self.main_widget.width() * 0.6 * button_row_count)
        button_size = int(available_height / button_row_count)
        if button_size > self.height() / button_row_count:
            button_size = int(self.height() / button_row_count)
        icon_size = int(button_size * 0.9)

        # Set button size and icon size
        for (
            row_layout
        ) in self.row_layouts:  # Change this line to iterate over the row layouts
            for i in range(row_layout.count()):
                button: QPushButton = row_layout.itemAt(i).widget()
                if button:
                    button.resize(button_size, button_size)
                    button.setIconSize(QSize(icon_size, icon_size))
