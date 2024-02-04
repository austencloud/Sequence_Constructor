from typing import TYPE_CHECKING
from Enums import LetterType
from objects.arrow.arrow import Arrow
from .mirrored_entry_data_prep import MirroredEntryDataPrep
from .mirrored_entry_pictograph_section_updater import MirroredEntryPictographSectionUpdater
from .mirrored_entry_rot_angle_manager import MirroredEntryRotAngleManager
from .mirrored_entry_creator import MirroredEntryCreator
from .mirrored_entry_updater import MirroredEntryUpdater

if TYPE_CHECKING:
    from ..special_placement_data_updater import SpecialPlacementDataUpdater


class SpecialPlacementMirroredEntryManager:
    def __init__(self, data_updater: "SpecialPlacementDataUpdater") -> None:
        self.data_updater = data_updater
        self.turns_tuple_generator = (
            data_updater.positioner.placement_manager.pictograph.main_widget.turns_tuple_generator
        )
        self.mirrored_entry_creator = MirroredEntryCreator(self)
        self.mirrored_entry_updater = MirroredEntryUpdater(self)
        self.rot_angle_manager = MirroredEntryRotAngleManager(self)
        self.section_updater = MirroredEntryPictographSectionUpdater(self)
        self.data_prep = MirroredEntryDataPrep(self)

    def update_mirrored_entry_in_json(self, arrow: "Arrow") -> None:
        if self.data_prep.is_new_entry_needed(arrow):
            self.mirrored_entry_creator.create_entry(arrow)
        else:
            self.mirrored_entry_updater.update_entry(arrow)
        self.section_updater.update_pictographs_in_section(
            LetterType.get_letter_type(arrow.pictograph.letter)
        )



# class SpecialPlacementMirroredEntryManager:
#     def __init__(self, data_updater: "SpecialPlacementDataUpdater") -> None:
#         self.data_updater = data_updater
#         self.turns_tuple_generator = (
#             data_updater.positioner.placement_manager.pictograph.main_widget.turns_tuple_generator
#         )
#         self.mirrored_entry_creator = MirroredEntryCreator(self)
#         self.mirrored_entry_updater = MirroredEntryUpdater(self)

#     def update_mirrored_entry_in_json(self, arrow: "Arrow") -> None:
#         letter_type = LetterType.get_letter_type(arrow.pictograph.letter)

#         mirrored_turns_tuple = self.turns_tuple_generator.generate_mirrored_tuple(arrow)

#         if mirrored_turns_tuple:
#             if self._is_new_entry_needed(arrow):
#                 self.mirrored_entry_creator.create_entry(arrow.pictograph.letter, arrow)
#             else:
#                 self.mirrored_entry_updater.update_entry(arrow.pictograph.letter, arrow)

#         self.update_pictographs_in_section(letter_type)

#     def _is_new_entry_needed(self, arrow: "Arrow") -> bool:
#         ori_key = self.data_updater._get_ori_key(arrow.motion)
#         return (
#             arrow.pictograph.letter
#             not in self.data_updater.positioner.placement_manager.pictograph.main_widget.special_placements.get(
#                 ori_key, {}
#             )
#         )

#     def update_rotation_angle_in_mirrored_entry(
#         self, letter: str, arrow: Arrow, updated_turn_data: dict
#     ) -> None:
#         self.rot_angle_override_manager = (
#             self.data_updater.positioner.placement_manager.pictograph.wasd_manager.rotation_angle_override_manager
#         )

#         ori_key = self.data_updater._get_ori_key(arrow.motion)

#         if self._should_handle_rotation_angle(arrow):
#             rotation_angle_override = self._check_for_rotation_angle_override(
#                 updated_turn_data
#             )
#             if rotation_angle_override is not None:
#                 other_ori_key, other_letter_data = self._get_keys_for_mixed_start_ori(
#                     letter, ori_key
#                 )
#                 mirrored_turns_tuple = (
#                     self.turns_tuple_generator.generate_mirrored_tuple(arrow)
#                 )
#                 self.rot_angle_override_manager.handle_mirrored_rotation_angle_override(
#                     other_letter_data,
#                     rotation_angle_override,
#                     mirrored_turns_tuple,
#                 )
#                 self.data_updater.update_specific_entry_in_json(
#                     letter, other_letter_data, other_ori_key
#                 )

#     def remove_rotation_angle_in_mirrored_entry(
#         self, letter: str, arrow: Arrow, hybrid_key: str
#     ) -> None:
#         ori_key = self.data_updater._get_ori_key(arrow.motion)

#         if arrow.pictograph.check.starts_from_mixed_orientation():
#             other_ori_key, other_letter_data = self._get_keys_for_mixed_start_ori(
#                 letter, ori_key
#             )
#             mirrored_turns_tuple = self.turns_tuple_generator.generate_mirrored_tuple(
#                 arrow
#             )


#             if hybrid_key in other_letter_data.get(mirrored_turns_tuple):
#                 del other_letter_data[mirrored_turns_tuple][hybrid_key]

#             self.data_updater.update_specific_entry_in_json(
#                 letter, other_letter_data, other_ori_key
#             )

#     def _get_keys_for_mixed_start_ori(self, letter, ori_key) -> tuple[str, dict]:
#         if (
#             self.data_updater.positioner.pictograph.check.starts_from_mixed_orientation()
#         ):
#             other_ori_key = self.data_updater.get_other_layer3_ori_key(ori_key)
#             other_letter_data = self._get_letter_data(other_ori_key, letter)
#             return other_ori_key, other_letter_data
#         return ori_key, self._get_letter_data(ori_key, letter)

#     def _fetch_letter_data_and_original_turn_data(
#         self, ori_key, letter, arrow
#     ) -> tuple[dict, dict]:
#         letter_data = self._get_letter_data(ori_key, letter)
#         original_turns_tuple = self._generate_turns_tuple(arrow)
#         return letter_data, letter_data.get(original_turns_tuple, {})

#     def _should_handle_rotation_angle(self, arrow: Arrow) -> bool:
#         return arrow.motion.motion_type in [STATIC, DASH]

#     def _check_for_rotation_angle_override(self, turn_data: dict) -> Optional[int]:
#         for key in turn_data:
#             if "rot_angle" in key:
#                 return turn_data[key]
#         return None

#     def update_pictographs_in_section(self, letter_type: LetterType) -> None:
#         section = self.data_updater.positioner.pictograph.scroll_area.sections_manager.get_section(
#             letter_type
#         )
#         for pictograph in section.pictographs.values():
#             pictograph.arrow_placement_manager.update_arrow_placements()

#     def _get_letter_data(self, ori_key: str, letter: str) -> dict:
#         return self.data_updater.positioner.placement_manager.pictograph.main_widget.special_placements.get(
#             ori_key, {}
#         ).get(
#             letter, {}
#         )

#     def _generate_turns_tuple(self, arrow: "Arrow") -> str:
#         return self.turns_tuple_generator.generate_turns_tuple(arrow.pictograph)