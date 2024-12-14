from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

from ..base_classes.base_answers_widget import BaseAnswersWidget


if TYPE_CHECKING:
    from ..learn_widget import LearnWidget


class Lesson1AnswersWidget(BaseAnswersWidget):
    """Widget to manage answer buttons layout and actions."""

    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.buttons: dict[str, QPushButton] = {}

    def display_answers(self, letters, correct_answer, check_answer_callback) -> None:
        """Create the answer buttons and attach click events."""
        for letter in letters:
            button = QPushButton(letter)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda _, opt=letter: check_answer_callback(opt, correct_answer)
            )
            self.layout.addWidget(button)
            self.buttons[letter] = button

    def clear(self) -> None:
        """Clear all buttons."""
        for button in self.buttons.values():
            self.layout.removeWidget(button)
            button.deleteLater()
        self.buttons.clear()

    def disable_answer(self, answer) -> None:
        """Deactivate the button for the incorrect answer."""
        self.buttons[answer].setDisabled(True)
        self.buttons[answer].setStyleSheet("color: gray;")

    def resize_answers_widget(self) -> None:
        for button in self.buttons.values():
            button.setFixedSize(
                self.main_widget.width() // 16, self.main_widget.width() // 16
            )
            font_size = self.main_widget.width() // 40
            font = button.font()
            font.setFamily("Georgia")  # Set the font family to Georgia
            font.setPointSize(font_size)
            button.setFont(font)
            button.setStyleSheet(f"font-size: {font_size}px;")
