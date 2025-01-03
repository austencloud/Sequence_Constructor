from os import name
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsTextItem, QGraphicsItemGroup
from PyQt6.QtGui import QFont, QColor

from base_widgets.base_pictograph.glyphs.tka_glyph.base_glyph import BaseGlyph
from data.constants import BLUE, HEX_BLUE, HEX_RED, RED

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class BeatReversalGlyph(QGraphicsItemGroup, BaseGlyph):
    def __init__(self, pictograph: "BasePictograph"):
        super().__init__(name="Reversals")
        self.pictograph = pictograph
        self.reversal_items: dict[str, QGraphicsTextItem] = {}
        self.create_reversal_symbols()

    def create_reversal_symbols(self):
        # Create reversal symbols for both hands
        red_R = self._create_reversal_text_item(HEX_RED)
        blue_R = self._create_reversal_text_item(HEX_BLUE)

        # Add items to the group
        self.addToGroup(red_R)
        self.addToGroup(blue_R)

        # Add the group to the pictograph
        self.pictograph.addItem(self)

        self.pictograph.blue_reversal_symbol = blue_R
        self.pictograph.red_reversal_symbol = red_R

        # Store references to the reversal items
        self.reversal_items[RED] = red_R
        self.reversal_items[BLUE] = blue_R

        # Initially hide the reversal symbols
        self.setVisible(False)

    def update_reversal_symbols(self):
        # Update the visibility of the reversal symbols based on the pictograph's reversal flags
        blue_visible = self.pictograph.blue_reversal
        red_visible = self.pictograph.red_reversal

        self.reversal_items[BLUE].setVisible(blue_visible)
        self.reversal_items[RED].setVisible(red_visible)

        center_y = self.pictograph.height() / 2

        if blue_visible and red_visible:
            # Both symbols are visible, position them stacked
            red_R = self.reversal_items[RED]
            blue_R = self.reversal_items[BLUE]
            total_height = (
                red_R.boundingRect().height() + blue_R.boundingRect().height()
            )
            red_R_y = -total_height / 2
            blue_R_y = red_R_y + red_R.boundingRect().height()
            red_R.setPos(0, red_R_y)
            blue_R.setPos(0, blue_R_y)
        elif blue_visible:
            # Only blue symbol is visible, center it vertically
            blue_R = self.reversal_items[BLUE]
            blue_R_y = -blue_R.boundingRect().height() / 2
            blue_R.setPos(0, blue_R_y)
        elif red_visible:
            # Only red symbol is visible, center it vertically
            red_R = self.reversal_items[RED]
            red_R_y = -red_R.boundingRect().height() / 2
            red_R.setPos(0, red_R_y)
        # else: both are not visible, do nothing

        # Update the visibility of the group
        self.setVisible(blue_visible or red_visible)

        # Position the group
        x_position = 40  # Adjust as needed
        self.setPos(x_position, center_y)

        self.pictograph.update()

    def _create_reversal_text_item(self, color) -> QGraphicsTextItem:
        text_item = QGraphicsTextItem("R")
        font = QFont("Georgia", 60, QFont.Weight.Bold)
        text_item.setFont(font)
        text_item.setDefaultTextColor(QColor(color))
        return text_item