from typing import TYPE_CHECKING, List

from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGridLayout,
    QGraphicsView,
    QFrame,
)


if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.sequence.sequence import Sequence


class SequenceBeats(QFrame):
    def __init__(
        self, main_widget: "MainWidget", pictograph: "Pictograph", sequence: "Sequence"
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.pictograph = pictograph
        self.sequence = sequence
        self.beats: List[QGraphicsView] = []

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        for j in range(4):
            for i in range(4):
                view = QGraphicsView()
                scene = QGraphicsScene()
                view.setScene(scene)
                view.setSceneRect(0, 0, 100, 100)
                rect = QRectF(0, 0, 50, 50)
                color = QColor(255, 0, 0)
                scene.addRect(rect, color)
                self.layout.addWidget(view, j, i)
                self.beats.append(view)

    def update_size(self) -> None:
        self.setFixedHeight(
            int(self.main_widget.height() - self.sequence.button_frame.height())
        )
        beat_height = int(((self.height() / 4)))
        beat_width = int(beat_height * 75 / 90)

        self.sequence.setFixedWidth(beat_width * 4)

        for beat in self.beats:
            beat.setFixedHeight(beat_height)
            beat.setFixedWidth(beat_width)
