from typing import TYPE_CHECKING
from Enums.Enums import LetterType, Letter
from Enums.Enums import LetterType
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.construct_tab.option_picker.option_picker_pictograph_view import (
    OptionPickerPictographView,
)

if TYPE_CHECKING:
    from .option_picker_scroll_area import OptionPickerScrollArea


class OptionPickerPictographFactory:
    def __init__(
        self,
        scroll_area: "OptionPickerScrollArea",
        pictograph_cache: dict[str, BasePictograph],
    ) -> None:
        self.scroll_area = scroll_area
        self.option_picker = scroll_area.option_picker
        self.pictograph_cache = pictograph_cache

    def get_or_create_pictograph(
        self, pictograph_key: str, pictograph_dict=None
    ) -> BasePictograph:
        letter_str = pictograph_key.split("_")[0]
        letter = Letter.get_letter(letter_str)

        if pictograph_key in self.pictograph_cache.get(letter, {}):
            return self.pictograph_cache[letter][pictograph_key]

        if pictograph_dict is not None:
            pictograph = self.create_pictograph()
            pictograph.updater.update_pictograph(pictograph_dict)
            pictograph.view.update_borders()
            if letter not in self.pictograph_cache:
                self.pictograph_cache[letter] = {}
            self.pictograph_cache[letter][pictograph_key] = pictograph
            self.scroll_area.main_widget.pictograph_cache[letter][
                pictograph_key
            ] = pictograph
            letter_type = LetterType.get_letter_type(letter)
            for letter_type in LetterType:
                if letter in letter_type.letters:
                    letter_type = letter_type
                    break

            section = self.scroll_area.section_manager.get_section(letter_type)
            section.pictographs[pictograph_key] = pictograph

            return pictograph

        raise ValueError("Pictograph dict is required for creating a new pictograph.")

    def remove_deselected_letter_pictographs(self, deselected_letter) -> None:
        keys_to_remove = [
            key
            for key in self.scroll_area.pictograph_cache
            if key.startswith(deselected_letter + "_")
        ]
        for key in keys_to_remove:
            pictograph = self.scroll_area.pictograph_cache.pop(key)
            pictograph.view.setParent(None)

    def get_pictograph(self, pictograph_key) -> BasePictograph:
        return self.scroll_area.pictograph_cache[pictograph_key]

    def create_pictograph(self) -> BasePictograph:
        pictograph = BasePictograph(self.scroll_area.main_widget)
        pictograph.view = OptionPickerPictographView(pictograph, self.option_picker)
        # pictograph.view.update_borders()
        return pictograph
