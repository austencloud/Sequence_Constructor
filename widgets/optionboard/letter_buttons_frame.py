# import the necessary things
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QPainter, QFont, QColor
from PyQt6.QtSvg import QSvgRenderer
from config.numerical_constants import GRAPHBOARD_SCALE
from utilities.pictograph_selector_dialog import PictographSelectorDialog
from data.letter_types import letter_types
from config.string_constants import LETTER_SVG_DIR


class LetterButtonsFrame(QFrame):
    def __init__(self, main_widget):
        super().__init__()
        self.main_window = main_widget.main_window
        self.letter_buttons_layout = QVBoxLayout()
        self.letter_buttons_layout.addStretch(1)
        self.letter_buttons_layout.setSpacing(int(20 * GRAPHBOARD_SCALE))
        self.letter_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        letter_rows = [
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
            # ['W-', 'X-'],
            # ['Y-', 'Z-'],
            # ['Σ-', 'Δ-'],
            # ['θ-', 'Ω-'],
            # Type 4 - Dash
            # ['Φ', 'Ψ', 'Λ'],
            # Type 5 - Dual-Dash
            # ['Φ-', 'Ψ-', 'Λ-'],
            # Type 6 - Static
            ["α", "β", "Γ"],
        ]

        for row in letter_rows:
            row_layout = QHBoxLayout()
            for letter in row:
                for letter_type in letter_types:
                    if letter in letter_types[letter_type]:
                        break
                icon_path = f"{LETTER_SVG_DIR}/{letter_type}/{letter}.svg"
                renderer = QSvgRenderer(icon_path)

                pixmap = QPixmap(renderer.defaultSize())
                pixmap.fill(QColor(Qt.GlobalColor.white))
                painter = QPainter(pixmap)
                renderer.render(painter)
                painter.end()
                button = QPushButton(QIcon(pixmap), "", self.main_window)
                font = QFont()
                font.setPointSize(int(20 * GRAPHBOARD_SCALE))
                button.setFont(font)
                button.setFixedSize(
                    int(120 * GRAPHBOARD_SCALE), int(120 * GRAPHBOARD_SCALE)
                )
                button.clicked.connect(
                    lambda _, l=letter: PictographSelectorDialog(main_widget, l)
                )
                row_layout.addWidget(button)
            self.letter_buttons_layout.addLayout(row_layout)
            self.letter_buttons_layout.addStretch(
                1
            )  # Add a stretch to the bottom of the layout

        self.main_window.sequence_layout.addLayout(self.letter_buttons_layout)
