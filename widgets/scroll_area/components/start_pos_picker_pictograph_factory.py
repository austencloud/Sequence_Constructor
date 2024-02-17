from typing import TYPE_CHECKING
from Enums.Enums import LetterType, Letter

from Enums.Enums import LetterType


from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.sequence_builder.components.start_position_picker.start_pos_picker import (
        StartPosPicker,
    )
    from widgets.sequence_builder.components.option_picker.option_picker_scroll_area import (
        OptionPickerScrollArea,
    )


class StartPosPickerPictographFactory:
    def __init__(
        self,
        start_pos_picker: "StartPosPicker",
        start_pos_cache: dict[str, Pictograph],
    ) -> None:
        self.start_pos_picker = start_pos_picker
        self.start_pos_cache = start_pos_cache

    def get_or_create_pictograph(
        self, pictograph_key: str, pictograph_dict=None
    ) -> Pictograph:
        letter_str = pictograph_key.split("_")[0]
        letter = Letter.get_letter(letter_str)

        if pictograph_key in self.start_pos_cache.get(letter, {}):
            return self.start_pos_cache[letter][pictograph_key]

        if pictograph_dict is not None:
            pictograph = self.create_pictograph()
            pictograph.updater.update_pictograph(pictograph_dict)

            if letter not in self.start_pos_cache:
                self.start_pos_cache[letter] = {}
            self.start_pos_cache[letter][pictograph_key] = pictograph
            self.start_pos_picker.main_widget.all_pictographs[letter][
                pictograph_key
            ] = pictograph
            letter_type = LetterType.get_letter_type(letter)
            for letter_type in LetterType:
                if letter in letter_type.letters:
                    letter_type = letter_type
                    break

            return pictograph

        raise ValueError("Pictograph dict is required for creating a new pictograph.")

    def remove_deselected_letter_pictographs(self, deselected_letter) -> None:
        keys_to_remove = [
            key
            for key in self.start_pos_cache
            if key.startswith(deselected_letter + "_")
        ]
        for key in keys_to_remove:
            pictograph = self.start_pos_cache.pop(key)
            pictograph.view.setParent(None)

    def get_pictograph(self, pictograph_key) -> Pictograph:
        return self.start_pos_cache[pictograph_key]

    def create_pictograph(self) -> Pictograph:
        pictograph = Pictograph(
            self.start_pos_picker.main_widget,
        )
        return pictograph