from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base_classes.base_auto_builder_frame import BaseAutoBuilderFrame


class LengthAdjuster(QWidget):
    def __init__(self, auto_builder_frame: "BaseAutoBuilderFrame"):
        super().__init__()
        self.auto_builder_frame = auto_builder_frame
        self.length = 8
        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)
        self.adjustment_amount = 2
        self.length_label = QLabel("Length:")
        self.length_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.length_buttons_layout = QHBoxLayout()
        self.length_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._create_length_adjuster()

        self.layout.addWidget(self.length_label)
        self.layout.addLayout(self.length_buttons_layout)

    def _create_length_adjuster(self):
        self.minus_button = QPushButton("-")
        self.minus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.minus_button.clicked.connect(self._decrement_length)

        self.length_value_label = QLabel(str(self.length))
        self.length_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.length_value_label.setFixedWidth(40)

        self.plus_button = QPushButton("+")
        self.plus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.plus_button.clicked.connect(self._increment_length)

        self.length_buttons_layout.addWidget(self.minus_button)
        self.length_buttons_layout.addWidget(self.length_value_label)
        self.length_buttons_layout.addWidget(self.plus_button)

    def limit_length(self, state):
        if state:
            self.length = (self.length // 4) * 4
            self.length_value_label.setText(str(self.length))
            self.auto_builder_frame._update_sequence_length(self.length)
            self.adjustment_amount = 4
        else:
            self.length = (self.length // 2) * 2
            self.length_value_label.setText(str(self.length))
            self.auto_builder_frame._update_sequence_length(self.length)
            self.adjustment_amount = 2

    def _increment_length(self):
        if self.length < 64:
            self.length += self.adjustment_amount
            self.length_value_label.setText(str(self.length))
            self.auto_builder_frame._update_sequence_length(self.length)

    def _decrement_length(self):
        if self.length > 4:
            self.length -= self.adjustment_amount
            self.length_value_label.setText(str(self.length))
            self.auto_builder_frame._update_sequence_length(self.length)

    def set_length(self, length):
        """Set the initial length when loading settings."""
        self.length = length
        self.length_value_label.setText(str(self.length))

    def resize_length_adjuster(self):
        font_size = (
            self.auto_builder_frame.sequence_generator_tab.main_widget.width() // 75
        )
        font = self.length_label.font()
        font.setPointSize(font_size)

        self.minus_button.setFont(font)
        self.plus_button.setFont(font)
        self.length_label.setFont(font)
        self.length_value_label.setFont(font)
        self.length_value_label.setFixedWidth(
            self.auto_builder_frame.sequence_generator_tab.main_widget.width() // 25
        )

        self.minus_button.updateGeometry()
        self.plus_button.updateGeometry()
        self.length_label.updateGeometry()

        self.minus_button.repaint()
        self.plus_button.repaint()
        self.length_label.repaint()
