from datetime import datetime
import os
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPainter, QPixmap
from path_helpers import get_my_photos_path
from widgets.image_export_dialog.image_export_dialog import ImageExportDialog
from widgets.image_export_layout_manager import ImageExportLayoutManager
from widgets.sequence_widget.SW_beat_frame.beat import Beat, BeatView
from PyQt6.QtWidgets import QFileDialog

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import (
        SW_BeatFrame,
    )


from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPainter, QPixmap, QFont
from PyQt6.QtWidgets import QFileDialog
import os


class SequenceImageExportManager:
    last_save_directory = None

    def __init__(self, beat_frame: "SW_BeatFrame") -> None:
        self.beat_frame = beat_frame
        self.main_widget = beat_frame.main_widget
        self.indicator_label = beat_frame.sequence_widget.indicator_label
        self.sequence_widget = beat_frame.sequence_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.include_start_pos = self.settings_manager.get_image_export_setting(
            "include_start_position", True
        )
        self.layout_manager = ImageExportLayoutManager(self)

    def exec_dialog(self):
        sequence = (
            self.beat_frame.current_sequence_json_handler.load_current_sequence_json()
        )
        if len(sequence) < 3:
            self.indicator_label.show_message("The sequence is empty.")
            return

        filled_beats = [beat for beat in self.beat_frame.beats if beat.is_filled]
        column_count, row_count = self.layout_manager.calculate_layout(
            len(filled_beats), self.include_start_pos
        )
        for beat in filled_beats:
            beat.scene().clearSelection()

        dialog = ImageExportDialog(self, sequence)
        if dialog.exec():
            options = dialog.get_export_options()
            self.include_start_pos = options.get(
                "include_start_pos", self.include_start_pos
            )
            self.settings_manager.set_image_export_setting(
                "include_start_position", self.include_start_pos
            )

            sequence_image = self.create_sequence_image(
                sequence, self.include_start_pos, options
            )
            self.save_image(sequence_image)
            print("Image created with start position included:", self.include_start_pos)

    def save_image(self, sequence_image: QImage):
        word = self.beat_frame.get_current_word()
        if word == "":
            self.indicator_label.show_message(
                "You must build a sequence to save it as an image."
            )
            return

        version_number = 1
        base_word_folder = get_my_photos_path(f"{word}")

        file_path = os.path.join(base_word_folder, f"{word}_v{version_number}.png")

        os.makedirs(base_word_folder, exist_ok=True)

        while os.path.exists(file_path):
            version_number += 1
            file_path = os.path.join(base_word_folder, f"{word}_v{version_number}.png")

        file_name, _ = QFileDialog.getSaveFileName(
            self.beat_frame,
            "Save Image",
            file_path,
            "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)",
        )

        if not file_name:
            return

        if sequence_image.save(file_name, "PNG"):
            self.indicator_label.show_message(
                f"Image saved as {os.path.basename(file_name)}"
            )
            self.last_save_directory = os.path.dirname(file_name)
        else:
            self.indicator_label.show_message("Failed to save image.")

    def create_sequence_image(
        self, sequence: list[dict], include_start_pos=True, options: dict = None
    ) -> QImage:
        filled_beats = self.process_sequence_to_beats(sequence)
        column_count, row_count = self.layout_manager.calculate_layout(
            len(filled_beats), include_start_pos
        )
        image = self.create_image(column_count, row_count)
        self._draw_beats(
            image, filled_beats, column_count, row_count, include_start_pos
        )
        if options:
            self._add_user_info_to_image(image, options)
        return image

    def process_sequence_to_beats(self, sequence: list[dict]):
        from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import (
            SW_BeatFrame,
        )

        self.temp_beat_frame = SW_BeatFrame(self.sequence_widget)
        filled_beats = []
        for beat_data in sequence[2:]:
            number = sequence.index(beat_data)
            beat_view = self.create_beat_view_from_data(beat_data, number)
            filled_beats.append(beat_view)
        return filled_beats

    def create_beat_view_from_data(self, beat_data, number):
        new_beat_view = BeatView(self.temp_beat_frame)
        beat = Beat(self.temp_beat_frame)
        beat.pictograph_dict = beat_data
        beat.updater.update_pictograph(beat_data)
        new_beat_view.set_beat(beat, number - 1)
        return new_beat_view

    def create_image(self, column_count, row_count) -> QImage:
        self.beat_size = int(self.beat_frame.start_pos_view.beat.width())
        image_width = column_count * self.beat_size
        image_height = row_count * self.beat_size + 50  # Extra height for text
        image = QImage(image_width, image_height, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)
        return image

    def _draw_beats(
        self, image, filled_beats, column_count, row_count, include_start_pos
    ):
        painter = QPainter(image)
        beat_number = 0

        if include_start_pos:
            start_pos_pixmap = self._grab_pixmap(
                self.beat_frame.start_pos_view, self.beat_size, self.beat_size
            )
            painter.drawPixmap(0, 0, start_pos_pixmap)
            start_col = 1
        else:
            start_col = 0

        for row in range(row_count + 1):
            for col in range(start_col, column_count):
                if beat_number < len(filled_beats):
                    beat_view = filled_beats[beat_number]
                    beat_pixmap = self._grab_pixmap(
                        beat_view, self.beat_size, self.beat_size
                    )
                    target_x = col * self.beat_size
                    target_y = row * self.beat_size
                    painter.drawPixmap(target_x, target_y, beat_pixmap)
                    beat_number += 1

        painter.end()

    def _grab_pixmap(self, view: "BeatView", width, height) -> QPixmap:
        return view.grab().scaled(
            width,
            height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    def _add_user_info_to_image(self, image: QImage, options: dict):
        painter = QPainter(image)
        font = QFont("Arial", 12)
        painter.setFont(font)

        user_name = options.get("user_name", "Your Name")
        export_date = options.get("export_date", datetime.now().strftime("%m-%d-%Y"))

        # Adding text to the bottom of the image
        margin = 10
        painter.drawText(
            margin, image.height() - margin - 10, f"Created using the Kinetic Alphabet"
        )
        painter.drawText(margin, image.height() - 2 * margin - 10, user_name)
        painter.drawText(
            image.width() - 100, image.height() - 2 * margin - 10, export_date
        )

        painter.end()
