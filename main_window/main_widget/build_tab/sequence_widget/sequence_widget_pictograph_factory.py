from typing import TYPE_CHECKING
from Enums.Enums import LetterType


from Enums.letters import Letter
from data.constants import (
    FLOAT,
)

from main_window.main_widget.build_tab.sequence_widget.beat_frame.beat import Beat
from main_window.main_widget.build_tab.sequence_widget.beat_frame.start_pos_beat import (
    StartPositionBeat,
)


if TYPE_CHECKING:
    from main_window.main_widget.build_tab.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )


class BeatFactory:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame") -> None:
        self.pictograph_cache = beat_frame.main_widget.pictograph_cache
        self.beat_frame = beat_frame
        self.main_widget = beat_frame.main_widget

    def create_start_pos_beat(
        self, pictograph_key: str, pictograph_dict=None
    ) -> StartPositionBeat:
        letter_str = pictograph_key.split("_")[0]
        letter = Letter.get_letter(letter_str)

        if pictograph_dict is not None:
            start_pos_beat = StartPositionBeat(self.beat_frame)
            start_pos_beat.updater.update_pictograph(pictograph_dict)

            if letter not in self.pictograph_cache:
                self.pictograph_cache[letter] = {}
            self.pictograph_cache[letter][pictograph_key] = start_pos_beat
            letter_type = LetterType.get_letter_type(letter)
            for letter_type in LetterType:
                if letter in letter_type.letters:
                    letter_type = letter_type
                    break

            return start_pos_beat

        raise ValueError("Pictograph dict is required for creating a new pictograph.")

    def create_new_beat_and_add_to_sequence(
        self,
        pictograph_dict: dict,
        override_grow_sequence=False,
        update_word=True,
        update_level=True,
        reversal_info=None,
    ) -> None:
        new_beat = Beat(self.beat_frame, duration=pictograph_dict.get("duration", 1))
        new_beat.updater.update_pictograph(pictograph_dict)
        if reversal_info:
            new_beat.blue_reversal = reversal_info.get("blue_reversal", False)
            new_beat.red_reversal = reversal_info.get("red_reversal", False)
        self.beat_frame.beat_adder.add_beat_to_sequence(
            new_beat,
            override_grow_sequence=override_grow_sequence,
            update_word=update_word,
            update_level=update_level,
        )
        for motion in new_beat.motions.values():
            if motion.motion_type == FLOAT:
                letter = self.main_widget.letter_determiner.determine_letter(motion)
                new_beat.letter = letter
                new_beat.tka_glyph.update_tka_glyph()
        self.main_widget.sequence_properties_manager.update_sequence_properties()