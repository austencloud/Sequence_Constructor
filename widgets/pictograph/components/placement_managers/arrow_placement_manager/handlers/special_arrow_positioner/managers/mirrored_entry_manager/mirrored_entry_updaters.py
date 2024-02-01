from Enums import LetterType
from constants import *
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.pictograph.components.placement_managers.arrow_placement_manager.handlers.special_arrow_positioner.managers.mirrored_entry_manager.mirrored_entry_updater import MirroredEntryUpdater
    from widgets.pictograph.components.placement_managers.arrow_placement_manager.handlers.special_arrow_positioner.managers.mirrored_entry_manager.mirrored_entry_manager import (
        SpecialPlacementMirroredEntryManager,
    )


class MirroredEntryUpdaterBase:
    def __init__(self, mirrored_entry_updater: "MirroredEntryUpdater", arrow: Arrow):
        self.mirrored_entry_updater = mirrored_entry_updater
        self.arrow = arrow

    def update_entry(self, letter: str, original_turn_data: dict):
        # Common update logic
        pass


class StandardOrientationUpdater(MirroredEntryUpdaterBase):
    def update_entry(self, letter: str, original_turn_data: dict):
        letter_type = LetterType.get_letter_type(letter)
        mirrored_turns_tuple = (
            self.mirrored_entry_updater.turns_tuple_generator.generate_mirrored_tuple(self.arrow)
        )
        other_ori_key, other_letter_data = self.mirrored_entry_updater._get_keys_for_mixed_start_ori(
            letter, self.mirrored_entry_updater.manager._get_ori_key(self.arrow.motion)
        )

        if letter in ["S", "T"]:
            key = self.arrow.motion.lead_state
        elif (
            letter_type in [Type1, Type5, Type6]
            and self.arrow.motion.motion_type != STATIC
        ):
            key = self.arrow.color
        else:
            key = self.arrow.motion.motion_type

        self.mirrored_entry_updater._update_mirrored_entry_data(
            mirrored_turns_tuple, other_letter_data, key, original_turn_data, self.arrow
        )
        self.mirrored_entry_updater.manager.data_updater.update_specific_entry_in_json(
            letter, other_letter_data, other_ori_key
        )


class MixedOrientationUpdater(MirroredEntryUpdaterBase):
    def update_entry(self, letter: str, original_turn_data: dict):
        mirrored_turns_tuple = (
            self.mirrored_entry_updater.turns_tuple_generator.generate_mirrored_tuple(self.arrow)
        )
        other_ori_key, other_letter_data = self.mirrored_entry_updater._get_keys_for_mixed_start_ori(
            letter, self.mirrored_entry_updater.manager.data_updater._get_ori_key(self.arrow.motion)
        )
        layer = "1" if self.arrow.motion.start_ori in [IN, OUT] else "2"

        if letter in ["S", "T"]:
            attr = self.arrow.motion.lead_state
            key = f"{attr}_from_layer{layer}"
        elif self.arrow.pictograph.check.has_hybrid_motions():
            attr = self.arrow.motion.motion_type
            key = f"{attr}_from_layer{layer}"
        else:
            key = f"{BLUE if self.arrow.color == RED else RED}"

        self.mirrored_entry_updater._update_mirrored_entry_data(
            mirrored_turns_tuple, other_letter_data, key, original_turn_data, self.arrow
        )
        self.mirrored_entry_updater.manager.data_updater.update_specific_entry_in_json(
            letter, other_letter_data, other_ori_key
        )
