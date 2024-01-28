from typing import TYPE_CHECKING

from widgets.pictograph.components.wasd_adjustment_manager.prop_placement_override_manager import (
    PropPlacementOverrideManager,
)

from .arrow_movement_manager import ArrowMovementManager
from .rotation_angle_override_manager import RotationAngleOverrideManager

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class WASD_AdjustmentManager:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.movement_manager = ArrowMovementManager(pictograph)
        self.rotation_angle_override_manager = RotationAngleOverrideManager(self)
        self.prop_placement_override_manager = PropPlacementOverrideManager(self)

    def handle_special_placement_removal(self) -> None:
        if not self.pictograph.selected_arrow:
            return

        letter = self.pictograph.letter
        self.pictograph.arrow_placement_manager.special_positioner.data_updater.remove_special_placement_entry(
            letter, self.pictograph.selected_arrow
        )
        self.pictograph.updater.update_pictograph()
