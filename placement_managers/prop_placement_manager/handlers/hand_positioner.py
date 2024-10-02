from typing import TYPE_CHECKING
from objects.prop.prop import Prop
from .big_prop_positioner import BigPropPositioner
from .prop_classifier import PropClassifier
from .reposition_beta_props_by_letter_manager import RepositionBetaByLetterHandler
from .small_prop_positioner import SmallPropPositioner
from .swap_beta_handler import SwapBetaHandler

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from placement_managers.prop_placement_manager.handlers.beta_prop_positioner import (
        BetaPropPositioner,
    )

    from ..prop_placement_manager import PropPlacementManager


class HandPositioner:
    def __init__(self, beta_prop_positioner: "BetaPropPositioner") -> None:
        self.beta_prop_positioner = beta_prop_positioner
        self.pictograph = beta_prop_positioner.pictograph

    def reposition_beta_hands(self) -> None:
        red_hand = self.pictograph.red_prop
        blue_hand = self.pictograph.blue_prop
        self.move_hand(red_hand, "right")
        self.move_hand(blue_hand, "left")

    def move_hand(self, prop: Prop, direction: str) -> None:
        offset_calculator = (
            self.beta_prop_positioner.prop_placement_manager.beta_offset_calculator
        )
        offset = offset_calculator.calculate_new_position_with_offset(
            prop.pos(), direction
        )
        prop.setPos(offset)