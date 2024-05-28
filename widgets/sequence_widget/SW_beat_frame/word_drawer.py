from typing import TYPE_CHECKING
from PyQt6.QtGui import QPainter, QFont, QFontMetrics, QImage
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.image_creator import ImageCreator
    from widgets.sequence_widget.SW_beat_frame.image_drawer import ImageDrawer


class WordDrawer:
    def __init__(self, image_creator: "ImageCreator"):
        self.image_creator = image_creator
        self.word_font = QFont("Georgia", 175, QFont.Weight.DemiBold, False)

    def draw_word(self, image: QImage, word: str, num_filled_beats: int) -> None:
        margin = 50
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        font = self.word_font
        if num_filled_beats == 1 or num_filled_beats == 2:
            font = self._create_font(
                font.family(),
                int(font.pointSize() // 1.5),
                font.weight(),
                font.italic(),
            )
            margin = 15

        metrics = QFontMetrics(font)
        text_width = metrics.horizontalAdvance(word)

        while text_width > image.width() - 2 * margin:
            font_size = font.pointSize() - 1
            font = self._create_font(
                font.family(), font_size, font.weight(), font.italic()
            )
            metrics = QFontMetrics(font)
            text_width = metrics.horizontalAdvance(word)
            if font_size <= 10:
                break

        self._draw_text(painter, image, word, font, margin, "top")
        painter.end()

    def _create_font(self, family: str, size: int, weight: int, italic: bool) -> QFont:
        font = QFont(family, size, weight)
        font.setItalic(italic)
        return font

    def _draw_text(
        self,
        painter: QPainter,
        image: QImage,
        text: str,
        font: QFont,
        margin: int,
        position: str,
        text_width: int = None,
    ) -> None:
        painter.setFont(font)
        if not text_width:
            metrics = QFontMetrics(font)
            text_width = metrics.horizontalAdvance(text)
            text_height = metrics.ascent()
        else:
            metrics = QFontMetrics(font)
            text_height = metrics.ascent()

        if position == "top":
            x = (image.width() - text_width) // 2
            y = text_height

        painter.drawText(x, y, text)
