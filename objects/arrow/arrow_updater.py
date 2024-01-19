from typing import TYPE_CHECKING
from PyQt6.QtCore import QPointF
if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow

class ArrowUpdater:
    def __init__(self, arrow: "Arrow"):
        self.arrow = arrow

    def update_arrow(self, arrow_dict=None) -> None:
        if arrow_dict:
            self.arrow.attr_manager.update_attributes(arrow_dict)
            if not self.arrow.is_ghost and self.arrow.ghost:
                self.arrow.ghost.attr_manager.update_attributes(arrow_dict)

        if not self.arrow.is_ghost:
            self.arrow.ghost.transform = self.arrow.transform
        self.arrow.svg_manager.update_arrow_svg()
        self.arrow.mirror_manager.update_mirror()
        self.arrow.svg_manager.update_color()
        self.arrow.location_calculator.update_location()
        self.arrow.rot_angle_calculator.update_rotation()

