from typing import TYPE_CHECKING

from utilities.word_simplifier import WordSimplifier


if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.beat import (
        BeatView,
    )
    from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )


class BeatFrameGetter:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame"):
        self.beat_frame = beat_frame

    def next_available_beat(self) -> int:
        current_beat = 0
        for beat_view in self.beat_frame.beats:
            if beat_view.is_filled:
                current_beat += 1
            else:
                return current_beat
        return current_beat

    def last_filled_beat(self) -> "BeatView":
        for beat_view in reversed(self.beat_frame.beats):
            if beat_view.is_filled:
                return beat_view
        return self.beat_frame.start_pos_view

    def current_word(self) -> str:
        word = ""
        for beat_view in self.beat_frame.beats:
            if beat_view.is_filled:
                if beat_view.beat.pictograph_dict.get("is_placeholder", False):
                    continue
                word += beat_view.beat.letter.value
        return WordSimplifier.simplify_repeated_word(word)

    def index_of_currently_selected_beat(self) -> int:
        for i, beat in enumerate(self.beat_frame.beats):
            if beat.is_selected:
                return i
        return 0

    def currently_selected_beat(self) -> "BeatView":
        for beat in self.beat_frame.beats:
            if beat.is_selected:
                return beat
        return self.beat_frame.beats[0]

    def beat_number_of_currently_selected_beat(self) -> int:
        return self.currently_selected_beat().number

    def duration_of_currently_selected_beat(self) -> int:
        return self.currently_selected_beat().beat.duration

    def beat_view_by_number(self, beat_number: int) -> "BeatView":
        for beat_view in self.beat_frame.beats:
            if beat_view.number == beat_number:
                return beat_view
        return None
