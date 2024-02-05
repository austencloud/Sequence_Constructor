from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtGui import QPen
from typing import TYPE_CHECKING

from utilities.TypeChecking.TypeChecking import VtgDirections

if TYPE_CHECKING:
    from ..glyph import Glyph


class Dot:
    def __init__(self, glyph: "Glyph") -> None:
        self.glyph = glyph
        self.same_dot_item = None
        self.opp_dot_item = None

    def add_dots(self, same_dot_path: str, opp_dot_path: str):
        self.same_dot_item = self.create_dot(same_dot_path, "Same")
        if self.same_dot_item:
            self.glyph.addToGroup(self.same_dot_item)

        self.opp_dot_item = self.create_dot(opp_dot_path, "Opp")
        if self.opp_dot_item:
            self.glyph.addToGroup(self.opp_dot_item)

    def create_dot(self, dot_path: str, label: str) -> QGraphicsSvgItem:
        renderer = QSvgRenderer(dot_path)
        if renderer.isValid():
            dot_item = QGraphicsSvgItem()
            dot_item.setSharedRenderer(renderer)
            dot_item.setToolTip(f"Outline for Dot {label}")
            return dot_item
        return None

    def position_dots(self, dir: VtgDirections):
        padding = 5
        letter_scene_rect = self.glyph.letter.letter_item.sceneBoundingRect()
        letter_scene_center = letter_scene_rect.center()

        if self.same_dot_item:
            same_dot_height = self.same_dot_item.boundingRect().height()
            same_dot_center = QPointF(
                letter_scene_center.x(),
                letter_scene_rect.top() - same_dot_height / 2 - padding,
            )
            self.same_dot_item.setPos(
                same_dot_center - self.same_dot_item.boundingRect().center()
            )

        if self.opp_dot_item:
            opp_dot_height = self.opp_dot_item.boundingRect().height()
            opp_dot_center = QPointF(
                letter_scene_center.x(),
                letter_scene_rect.bottom() + opp_dot_height / 2 + padding,
            )
            self.opp_dot_item.setPos(
                opp_dot_center - self.opp_dot_item.boundingRect().center()
            )

        if dir == VtgDirections.SAME:
            self.same_dot_item.show()
            self.opp_dot_item.hide()
        elif dir == VtgDirections.OPP:
            self.same_dot_item.hide()
            self.opp_dot_item.show()
        else:
            self.same_dot_item.hide()
            self.opp_dot_item.hide()