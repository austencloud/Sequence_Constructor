import json
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal

from widgets.sequence_builder.components.option_picker.option_manager import (
    OptionManager,
)
<<<<<<< HEAD
from widgets.sequence_builder.components.start_pos_picker.choose_your_next_option_label import (
    ChooseYourNextOptionLabel,
=======
from widgets.sequence_builder.components.start_pos_picker.choose_your_next_pictograph_label import (
    ChooseYourNextPictographLabel,
>>>>>>> 6fa36c8ff84359dfba82ab7ab201d6bca117a409
)

from .option_picker_scroll_area import OptionPickerScrollArea

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...sequence_builder import SequenceBuilder


class OptionPicker(QWidget):
    option_selected = pyqtSignal(str)  # Signal to emit the selected option

    def __init__(self, sequence_builder: "SequenceBuilder"):
        super().__init__(sequence_builder)
        self.sequence_builder = sequence_builder
        self.main_widget = sequence_builder.main_widget
        self.option_manager = OptionManager(self)
        self.scroll_area = OptionPickerScrollArea(self)
        self.choose_your_next_option_label = ChooseYourNextOptionLabel(self)

        self.setup_layout()
        self.hide()

    def setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.choose_your_next_option_label.show()
        self.layout.addWidget(self.choose_your_next_option_label, 1)
        self.layout.addWidget(self.scroll_area, 10)

    def update_option_picker(self):
        try:
            with open(
                self.main_widget.json_manager.current_sequence_json_handler.current_sequence_json,
                "r",
                encoding="utf-8",
            ) as file:
                sequence = json.load(file)
        except Exception as e:
            print(f"Failed to load sequence: {str(e)}")
            return

        if sequence:
            next_options: dict = self.option_manager.get_next_options()
            self.scroll_area._hide_all_pictographs()
            self.scroll_area._add_and_display_relevant_pictographs(next_options)
        self.choose_your_next_option_label.set_stylesheet()
