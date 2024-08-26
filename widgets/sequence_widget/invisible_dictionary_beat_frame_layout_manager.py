from typing import TYPE_CHECKING
from data.beat_frame_layouts import DEFAULT_BEAT_FRAME_LAYOUTS

if TYPE_CHECKING:
    from widgets.sequence_widget.beat_frame.beat_frame import SequenceWidgetBeatFrame


class InvisibleDictionaryBeatFrameLayoutManager:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame"):
        self.beat_frame = beat_frame
        # self.selection_overlay = beat_frame.selection_overlay
        self.settings_manager = beat_frame.main_widget.main_window.settings_manager

    def calculate_layout(self, beat_count: int) -> tuple[int, int]:
        return DEFAULT_BEAT_FRAME_LAYOUTS.get(beat_count, (1, beat_count))

    def get_cols(self):
        # get the columns that currently are visible in the current beat frame by looking at its grid layout
        # only return the number of columns that are actually full
        layout = self.beat_frame.layout
        cols = 0
        for i in range(layout.columnCount()):
            if layout.itemAtPosition(0, i):
                cols += 1
        return cols - 1

    def get_rows(self):
        # get the rows that currently are visible in the current beat frame by looking at its grid layout
        # only return the number of rows that are actually full
        layout = self.beat_frame.layout
        rows = 0
        for i in range(layout.rowCount()):
            if layout.itemAtPosition(i, 1):
                rows += 1
        return rows

    def configure_beat_frame(self, num_beats):
        grow_sequence = self.settings_manager.global_settings.get_grow_sequence()
        if grow_sequence:
            num_filled_beats = self.beat_frame.find_next_available_beat() or 0
            num_beats = num_filled_beats
        columns, rows = self.calculate_layout(num_beats)

        self.rearrange_beats(num_beats, columns, rows)

    def rearrange_beats(self, num_beats, columns, rows):
        while self.beat_frame.layout.count():
            self.beat_frame.layout.takeAt(0).widget().hide()

        self.beat_frame.layout.addWidget(self.beat_frame.start_pos_view, 0, 0, 1, 1)
        self.beat_frame.start_pos_view.show()

        index = 0
        beats = self.beat_frame.beats
        for row in range(rows):
            for col in range(1, columns + 1):
                if index < num_beats:
                    beat_view = beats[index]
                    self.beat_frame.layout.addWidget(beat_view, row, col)
                    beat_view.show()
                    index += 1
                else:
                    if index < len(beats):
                        beats[index].hide()
                        index += 1

        self.beat_frame.adjustSize()
        # selected_beat = self.selection_overlay.selected_beat
        # if selected_beat:
        #     self.selection_overlay.deselect_beat()
        #     self.selection_overlay.select_beat(selected_beat)
        #     self.selection_overlay.update_overlay_position()
