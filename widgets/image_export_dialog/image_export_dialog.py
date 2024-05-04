from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from widgets.image_export_dialog.export_control_panel import ExportDialogControlPanel
from widgets.image_export_dialog.export_dialog_preview import ExportDialogPreviewPanel

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.sequence_image_export_manager import (
        SequenceImageExportManager,
    )


class ImageExportDialog(QDialog):
    def __init__(self, export_manager: "SequenceImageExportManager"):
        super().__init__(export_manager.main_widget)
        self.export_manager = export_manager
        self.main_widget = export_manager.main_widget
        self.setWindowTitle("Export Image Options")
        self.setModal(True)

        # Calculate initial size based on main widget
        main_width = self.main_widget.width()
        main_height = self.main_widget.height()
        self.resize(
            main_width // 2, main_height // 2
        )  # Set initial size to 50% of main widget

        # Layout setup
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.preview_panel = ExportDialogPreviewPanel(self)
        self.preview_panel_label = QLabel(self)
        self.preview_panel_label.setText("Preview:")
        #make the font bigger, center it in the label
        self.preview_panel_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_panel_label.setStyleSheet("font-size: 20px")
        self.preview_panel_layout = QVBoxLayout()
        self.preview_panel_layout.addWidget(self.preview_panel_label)
        self.preview_panel_layout.addWidget(self.preview_panel)
        self.button_panel = ExportDialogControlPanel(self)
        self.button_panel.optionChanged.connect(self.update_preview_based_on_options)
        self.button_panel.include_start_pos_check.setChecked(
            export_manager.include_start_pos
        )

        # Add components to layout
        self.layout.addLayout(self.preview_panel_layout, 1)
        self.layout.addWidget(self.button_panel, 1)

        self.button_panel.include_start_pos_check.toggled.connect(
            self.update_export_setting_and_layout
        )
        self.update_preview_based_on_options()

    def update_export_setting_and_layout(self):
        new_value = self.button_panel.include_start_pos_check.isChecked()
        self.export_manager.include_start_pos = new_value  # Update the manager's state
        self.export_manager.settings_manager.set_image_export_setting(
            "include_start_position", new_value
        )
        self.update_preview_based_on_options()  # Redraw preview with the new layout settings

    def update_preview_based_on_options(self):
        include_start_pos = self.button_panel.include_start_pos_check.isChecked()
        self.preview_panel.update_preview_with_start_pos(include_start_pos)
        # resize it appropriately

    def update_preview_based_on_options(self):
        include_start_pos = self.button_panel.include_start_pos_check.isChecked()
        self.preview_panel.update_preview_with_start_pos(include_start_pos)

    def get_export_options(self):
        return {
            "include_start_pos": self.button_panel.include_start_pos_check.isChecked(),
            "user_name": self.button_panel.add_name_field.text(),
            "export_date": self.button_panel.add_date_field.text(),
        }

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.preview_panel.update_preview()
