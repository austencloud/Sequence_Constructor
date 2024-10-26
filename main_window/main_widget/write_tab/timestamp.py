# timestamp_label.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLineEdit, QSizePolicy
from PyQt6.QtCore import Qt

from main_window.main_widget.write_tab.editable_label import EditableLabel

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.timestamp_frame import TimestampFrame


class Timestamp(EditableLabel):
    def __init__(self, timestamp_frame: "TimestampFrame", label_text="0:00"):
        super().__init__(timestamp_frame, label_text)
        self.timestamp_frame = timestamp_frame
        self.write_tab = timestamp_frame.write_tab
        self.setContentsMargins(0, 0, 0, 0)
        self.label.setContentsMargins(0, 0, 0, 0)
        self.edit.setContentsMargins(0, 0, 0, 0)

        self.label.setStyleSheet(
            "border-top: 1px solid black; border-bottom: 1px solid black; padding: 0px; margin: 0px;"
        )
        self.edit.setStyleSheet(
            "border-top: 1px solid black; border-bottom: 1px solid black; padding: 0px; margin: 0px;"
        )

        # Set alignment to top-left
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.edit.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.label.setMargin(0)
        # self.edit.setMargin(0)

    def _show_edit(self, event):
        """Show the QLineEdit for editing with the current timestamp pre-filled."""
        self.edit.setText(self.label.text())  # Pre-fill with current timestamp
        self.label.setVisible(False)
        self.edit.setVisible(True)
        self.edit.setFocus()
        self.edit.selectAll()
        self.edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # transparent background
        self.edit.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def _hide_edit(self):
        """Ensure timestamp format on hiding the editor."""
        new_text = self.edit.text()

        self.label.setText(new_text if new_text else self.label.text())
        self.label.setVisible(True)
        self.edit.setVisible(False)

    def set_text(self, text: str):
        """Set the text ensuring it's formatted as a timestamp."""
        self.label.setText(text)

    def resize_timestamp(self):
        desired_height = self.timestamp_frame.write_tab.beat_scroll_area.act_beat_frame.beat_size
        self.setFixedHeight(desired_height)
        self.label.setFixedHeight(desired_height)
        self.edit.setFixedHeight(desired_height)
        self.label.setFixedWidth(self.timestamp_frame.width())
        self.edit.setFixedWidth(self.timestamp_frame.width())
        self.setFixedWidth(self.timestamp_frame.width())
        # Adjust font size if necessary
        font_size = int(desired_height * 0.1)  # For example, 60% of the height
        font = self.label.font()
        font.setPointSize(font_size)
        font.setBold(True)
        self.label.setFont(font)
        self.edit.setFont(font)
