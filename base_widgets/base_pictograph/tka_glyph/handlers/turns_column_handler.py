from PyQt6.QtWidgets import QGraphicsItemGroup
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from typing import TYPE_CHECKING, Union

from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from base_widgets.base_pictograph.components.tka_glyph.tka_glyph import TKA_Glyph


class TurnsColumnHandler(QGraphicsItemGroup):
    def __init__(self, glyph: "TKA_Glyph") -> None:
        super().__init__()
        self.glyph = glyph
        self.top_number_item = None
        self.bottom_number_item = None
        self.svg_path_prefix = get_images_and_data_path("images/numbers/")
        self.blank_svg_path = get_images_and_data_path("images/blank.svg")
        self.number_svg_cache = {}

    def load_number_svg(self, number: Union[int, float, str]) -> QGraphicsSvgItem:
        if number == "fl":  # Handle the float case
            svg_path = get_images_and_data_path("images/numbers/float.svg")
        else:
            svg_path = (
                self.blank_svg_path
                if number == 0
                else f"{self.svg_path_prefix}{number}.svg"
            )

        if svg_path not in self.number_svg_cache:
            renderer = QSvgRenderer(svg_path)
            if renderer.isValid():
                self.number_svg_cache[svg_path] = renderer
            else:
                return None
        else:
            renderer = self.number_svg_cache[svg_path]

        number_item = QGraphicsSvgItem()
        number_item.setSharedRenderer(renderer)
        return number_item

    def set_number(self, number: Union[int, float, str], is_top: bool) -> None:
        new_item = self.load_number_svg(number)
        old_item = self.top_number_item if is_top else self.bottom_number_item

        if old_item:
            self.removeFromGroup(old_item)
            old_item.hide()

        if new_item:
            self.addToGroup(new_item)
            new_item.show()
            if is_top:
                self.top_number_item = new_item
            else:
                self.bottom_number_item = new_item

    def position_turns(self) -> None:
        reference_rect = (
            self.glyph.dash_handler.dash_item.sceneBoundingRect()
            if self.glyph.dash_handler.dash_item
            else self.glyph.letter_handler.letter_item.sceneBoundingRect()
        )
        letter_scene_rect = self.glyph.letter_handler.letter_item.sceneBoundingRect()

        base_pos_x = reference_rect.right() + 15

        high_pos_y = letter_scene_rect.top() - 5
        low_pos_y = (
            letter_scene_rect.bottom()
            - (
                self.bottom_number_item.boundingRect().height()
                if self.bottom_number_item
                else 0
            )
            + 5
        )

        if self.top_number_item:
            self.top_number_item.setPos(base_pos_x, high_pos_y)

        if self.bottom_number_item:
            adjusted_low_pos_y = low_pos_y if self.top_number_item else high_pos_y + 20
            self.bottom_number_item.setPos(base_pos_x, adjusted_low_pos_y)

    def update_turns(
        self, top_turn: Union[int, float, str], bottom_turn: Union[int, float, str]
    ) -> None:
        self.set_number(top_turn, is_top=True)
        self.set_number(bottom_turn, is_top=False)
        self.position_turns()
