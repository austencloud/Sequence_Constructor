from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtWidgets import QLabel, QApplication
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox


class ThumbnailImageLabel(QLabel):
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__()
        self.thumbnail_box = thumbnail_box

        self.setStyleSheet("border: 3px solid black;")
        self.installEventFilter(self)
        self.mousePressEvent = self.thumbnail_clicked
        self.thumbnails = thumbnail_box.thumbnails
        self.current_index = thumbnail_box.current_index
        self.metadata_extractor = thumbnail_box.metadata_extractor
        self.browser = thumbnail_box.browser
        self.is_selected = False

        self.setScaledContents(False)  # Ensure the image scales with label size
        self.update_thumbnail()

    def update_thumbnail(self):
        if self.thumbnails and 0 <= self.current_index < len(self.thumbnails):
            pixmap = QPixmap(self.thumbnails[self.current_index])
            self.set_pixmap_to_fit(pixmap)
        else:
            self.setText("No image available")

    def set_pixmap_to_fit(self, pixmap: QPixmap):
        # Scale pixmap to fit within the current label dimensions
        scaled_pixmap = pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setPixmap(scaled_pixmap)

    def thumbnail_clicked(self, event):
        metadata = self.metadata_extractor.extract_metadata_from_file(
            self.thumbnails[0]
        )
        self.browser.dictionary_widget.selection_handler.thumbnail_clicked(
            self,
            QPixmap(self.thumbnails[self.current_index]),
            metadata,
            self.thumbnails,
            self.current_index,
        )

    def set_selected(self, selected: bool):
        self.is_selected = selected
        if selected:
            self.setStyleSheet("border: 3px solid blue;")
        else:
            self.setStyleSheet("border: 3px solid black;")

    def set_pixmap(self, image_path):
        self.setPixmap(QPixmap(image_path))
        self.update()
        QApplication.processEvents()
        self.update_thumbnail()

    def eventFilter(self, obj, event: QEvent):
        if obj == self and event.type() == QEvent.Type.Enter:
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.setStyleSheet("border: 3px solid gold;")
        elif obj == self and event.type() == QEvent.Type.Leave:
            self.setStyleSheet(
                "border: 3px solid black;"
                if not self.is_selected
                else "border: 3px solid blue;"
            )
        return super().eventFilter(obj, event)