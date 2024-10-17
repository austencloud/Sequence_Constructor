from PyQt6.QtGui import QImage
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from .height_determiner import HeightDeterminer
from .beat_drawer import BeatDrawer
from .user_info_drawer import UserInfoDrawer
from .word_drawer import WordDrawer
from .difficulty_level_drawer import DifficultyLevelDrawer

if TYPE_CHECKING:
    from ..image_export_manager import ImageExportManager


class ImageCreator:
    """Class responsible for creating sequence images."""

    BASE_MARGIN = 50

    def __init__(self, export_manager: "ImageExportManager"):
        self.export_manager = export_manager
        self.beat_frame = export_manager.beat_frame
        self.layout_manager = export_manager.layout_handler
        self.beat_size = self.beat_frame.start_pos_view.beat.width()
        self.beat_factory = export_manager.beat_factory
        self.beat_scale = 1
        self._setup_drawers()

    def _setup_drawers(self):
        """Set up drawer instances."""
        self.beat_drawer = BeatDrawer(self)
        self.word_drawer = WordDrawer(self)
        self.user_info_drawer = UserInfoDrawer(self)
        self.difficulty_level_drawer = DifficultyLevelDrawer(self)

    def create_sequence_image(
        self, sequence: list[dict], include_start_pos=True, options: dict = None
    ) -> QImage:
        """Create an image of the sequence."""
        filled_beats = self.beat_factory.process_sequence_to_beats(sequence)
        column_count, row_count = self.layout_manager.calculate_layout(
            len(filled_beats), include_start_pos
        )
        num_filled_beats = len(filled_beats)
        if options:
            additional_height_top, additional_height_bottom = (
                HeightDeterminer.determine_additional_heights(
                    options, num_filled_beats, self.beat_scale
                )
            )
            add_beat_numbers = options.get("add_beat_numbers")
        else:
            additional_height_top, additional_height_bottom = 0, 0
            add_beat_numbers = True

        image = self._create_image(
            column_count, row_count, additional_height_top + additional_height_bottom
        )

        self.beat_drawer.draw_beats(
            image,
            filled_beats,
            column_count,
            row_count,
            include_start_pos,
            additional_height_top,
            add_beat_numbers,
        )

        if options:
            if options.get("add_info"):
                self.user_info_drawer.draw_user_info(image, options, num_filled_beats)

            if options.get("add_word"):
                word = self.beat_frame.get.current_word()
                self.word_drawer.draw_word(
                    image, word, num_filled_beats, additional_height_top
                )

            if options.get("add_difficulty_level"):
                difficulty_level = self.export_manager.main_widget.sequence_level_evaluator.get_sequence_difficulty_level(
                    self.export_manager.beat_frame.json_manager.loader_saver.load_current_sequence_json()
                )
                self.difficulty_level_drawer.draw_difficulty_level(
                    image, difficulty_level, additional_height_top
                )
            if options.get("add_beat_numbers"):
                for beat_view in filled_beats:
                    beat_view.beat_number_item.setVisible(True)

            else:
                for beat_view in filled_beats:
                    beat_view.beat_number_item.setVisible(False)
        return image

    def _create_image(self, column_count, row_count, additional_height=0) -> QImage:
        """Create a new QImage with the given dimensions."""
        image_width = int((column_count * self.beat_size * self.beat_scale))
        image_height = int(
            (row_count * self.beat_size * self.beat_scale) + additional_height
        )
        image = QImage(image_width, image_height, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)
        return image
