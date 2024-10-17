from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

from ..widgets.continuous_rotation_toggle import ContinuousRotationToggle
from ..widgets.length_adjuster import LengthAdjuster
from ..widgets.level_selector import LevelSelector
from ..widgets.turn_intensity_adjuster import TurnIntensityAdjuster

if TYPE_CHECKING:
    from ..sequence_generator import SequenceGeneratorWidget


class BaseAutoBuilderFrame(QFrame):
    def __init__(
        self, sequence_generator_tab: "SequenceGeneratorWidget", builder_type: str
    ) -> None:
        super().__init__(sequence_generator_tab)
        self.sequence_generator_tab = sequence_generator_tab
        self.builder_type = builder_type
        self.auto_builder_settings = (
            sequence_generator_tab.main_widget.main_window.settings_manager.builder_settings.auto_builder
        )

        # Create Layout
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # Modular widgets
        self.level_selector = LevelSelector(self)
        self.length_adjuster = LengthAdjuster(self)
        self.turn_intensity_adjuster = TurnIntensityAdjuster(self)
        self.continuous_rotation_toggle = ContinuousRotationToggle(self)

        self.create_sequence_button = QPushButton("Create Sequence")
        self.create_sequence_button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Add Widgets to Layout
        self.layout.addStretch(1)
        self.layout.addWidget(self.level_selector)
        self.layout.addStretch(1)
        self.layout.addWidget(self.length_adjuster)
        self.layout.addStretch(1)
        self.layout.addWidget(self.turn_intensity_adjuster)
        self.layout.addStretch(1)
        self.layout.addWidget(self.continuous_rotation_toggle)
        self.layout.addStretch(1)

        self.layout.addWidget(
            self.create_sequence_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

    def apply_settings(self):
        """Apply settings to modular widgets."""
        level = self.auto_builder_settings.get_auto_builder_setting(
            "sequence_level", self.builder_type
        )
        length = self.auto_builder_settings.get_auto_builder_setting(
            "sequence_length", self.builder_type
        )
        intensity = self.auto_builder_settings.get_auto_builder_setting(
            "max_turn_intensity", self.builder_type
        )
        continuous_rotation = self.auto_builder_settings.get_auto_builder_setting(
            "continuous_rotation", self.builder_type
        )

        self.level_selector.set_level(level)
        self.length_adjuster.set_length(length)
        self.turn_intensity_adjuster.set_intensity(intensity)
        self.continuous_rotation_toggle.set_state(continuous_rotation)
        self.continuous_rotation_toggle.update_mode_label_styles()

    def _resize_auto_builder_frame(self):
        """Resize the auto builder frame based on the parent widget size."""
        self._resize_widgets()
        self._resize_create_sequence_button()

    def _resize_widgets(self):
        self.continuous_rotation_toggle.resize_continuous_rotation_toggle()
        self.level_selector.resize_level_selector()
        self.length_adjuster.resize_length_adjuster()
        self.turn_intensity_adjuster.resize_max_turn_intensity_adjuster()

    def _resize_create_sequence_button(self):
        font_size = self.sequence_generator_tab.main_widget.width() // 50
        self.create_sequence_button.setStyleSheet(f"font-size: {font_size}px;")
        self.create_sequence_button.updateGeometry()
        self.create_sequence_button.repaint()

        self.create_sequence_button.setFixedWidth(
            self.sequence_generator_tab.main_widget.width() // 3
        )
        self.create_sequence_button.setFixedHeight(
            self.sequence_generator_tab.main_widget.height() // 10
        )

    def _update_sequence_length(self, length: int):
        self.auto_builder_settings.set_auto_builder_setting(
            "sequence_length", length, self.builder_type
        )

    def _update_sequence_level(self, level: int):
        self.auto_builder_settings.set_auto_builder_setting(
            "sequence_level", level, self.builder_type
        )

    def _update_max_turn_intensity(self, intensity: int):
        self.auto_builder_settings.set_auto_builder_setting(
            "max_turn_intensity", intensity, self.builder_type
        )

    def _update_continuous_rotation(self, state: bool):
        self.auto_builder_settings.set_auto_builder_setting(
            "continuous_rotation", state, self.builder_type
        )
