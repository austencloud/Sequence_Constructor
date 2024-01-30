import os
from typing import TYPE_CHECKING, Union
from Enums import LetterType
from constants import BLUE, RED, Type1, Type4, Type5
from objects.arrow.arrow import Arrow
from utilities.TypeChecking.MotionAttributes import Colors

if TYPE_CHECKING:
    from .special_placement_data_updater import SpecialPlacementDataUpdater


class SpecialPlacementEntryRemover:
    """Handles removal of special placement entries."""

    def __init__(
        self,
        data_updater: "SpecialPlacementDataUpdater",
    ) -> None:
        self.positioner = data_updater.positioner
        self.data_updater = data_updater

    def remove_special_placement_entry(self, letter: str, arrow: Arrow) -> None:
        orientation_key = self.data_updater._get_orientation_key(arrow.motion.start_ori)
        file_path = os.path.join(
            self.positioner.placement_manager.pictograph.main_widget.parent_directory,
            f"{orientation_key}/{letter}_placements.json",
        )
        if os.path.exists(file_path):
            data = self.data_updater.json_handler.load_json_data(file_path)
            if letter in data:
                letter_data = data[letter]
                turns_tuple = (
                    self.positioner.turns_tuple_generator.generate_turns_tuple(letter)
                )
                self._remove_turn_data_entry(
                    letter_data, turns_tuple, arrow, arrow.color
                )

                letter_type = LetterType.get_letter_type(letter)
                mirrored_turns_tuple = self._generate_mirrored_tuple(arrow, letter_type)
                if mirrored_turns_tuple:
                    other_color = self._get_other_color(arrow.color)
                    self._remove_turn_data_entry(
                        letter_data, mirrored_turns_tuple, arrow, other_color
                    )

                self.data_updater.json_handler.write_json_data(data, file_path)
            arrow.pictograph.main_widget.refresh_placements()

    def _get_other_color(self, color: Colors) -> Colors:
        return RED if color == BLUE else BLUE

    def _generate_mirrored_tuple(
        self, arrow: Arrow, letter_type: LetterType
    ) -> Union[str, None]:
        if letter_type == Type1:
            turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(
                arrow.pictograph.letter
            )
            items = turns_tuple.strip("()").split(", ")
            return f"({items[1]}, {items[0]})"
        elif letter_type == Type4:
            turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(
                arrow.pictograph.letter
            )
            prop_rotation = "cw" if "ccw" in turns_tuple else "ccw"
            turns = turns_tuple[turns_tuple.find(",") + 2 :]
            return f"({prop_rotation}, {turns}"
        elif letter_type == Type5:
            turns_tuple = (
                self.data_updater.positioner.turns_tuple_generator.generate_turns_tuple(
                    arrow.pictograph.letter
                )
            )
            items = turns_tuple.strip("()").split(", ")
            return f"({items[0]}, {items[2]}, {items[1]})"
        return None

    def _remove_turn_data_entry(
        self, letter_data: dict, turns_tuple: str, arrow: Arrow, color: str
    ) -> None:
        turn_data = letter_data.get(turns_tuple, {})
        if arrow.motion.lead_state in turn_data:
            del turn_data[arrow.motion.lead_state]
            if not turn_data:
                del letter_data[turns_tuple]
        elif arrow.motion.motion_type in turn_data:
            del turn_data[arrow.motion.motion_type]
            if not turn_data:
                del letter_data[turns_tuple]
        elif color in turn_data:
            del turn_data[color]
            if not turn_data:
                del letter_data[turns_tuple]
