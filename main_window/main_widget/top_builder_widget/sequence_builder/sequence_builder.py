from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.sequence_generator import (
    SequenceGeneratorWidget,
)
from main_window.main_widget.top_builder_widget.sequence_builder.manual_builder import (
    ManualBuilderWidget,
)

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.top_builder_widget import (
        TopBuilderWidget,
    )
    from main_window.main_widget.main_widget import MainWidget


class SequenceBuilder(QTabWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget

        # Create instances of ManualBuilder and AutoBuilder
        self.manual_builder = ManualBuilderWidget(self)
        # self.sequence_generator_tab = SequenceGeneratorTab(self)

        # Add tabs for both builders
        self.addTab(self.manual_builder, "Manual")
        # self.addTab(self.sequence_generator_tab, "Auto")

        # Set initial tab to manual builder
        self.load_last_used_builder()

        # resize on tab change
        self.currentChanged.connect(self.on_tab_change)
        self.tabBar().setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def load_last_used_builder(self):
        """Set the last used builder as the current tab."""
        last_used_builder = (
            self.main_widget.settings_manager.builder_settings.get_last_used_builder()
        )

        if last_used_builder == "manual":
            self.setCurrentWidget(self.manual_builder)
        else:
            # self.setCurrentWidget(self.sequence_generator_tab)
            last_used_auto_builder = (
                self.main_widget.settings_manager.builder_settings.auto_builder.get_current_auto_builder()
            )
            # self.sequence_generator_tab.load_last_used_auto_builder(
            #     last_used_auto_builder
            # )

    def on_tab_change(self):
        """Save the currently selected tab."""
        if self.currentWidget() == self.manual_builder:
            self.main_widget.settings_manager.builder_settings.set_last_used_builder(
                "manual"
            )
        # elif self.currentWidget() == self.sequence_generator_tab:
        #     self.main_widget.settings_manager.builder_settings.set_last_used_builder(
        #         "auto"
        #     )

        self.resize_sequence_builder()

    def resize_sequence_builder(self):
        self.manual_builder.resize_manual_builder()
        # self.sequence_generator_tab.resize_auto_builder()

    def resizeEvent(self, event):
        self.resize_sequence_builder()
        super().resizeEvent(event)
