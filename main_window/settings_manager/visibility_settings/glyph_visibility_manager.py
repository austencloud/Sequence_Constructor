from typing import TYPE_CHECKING

from Enums.letters import Letter


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from main_window.settings_manager.visibility_settings.visibility_settings import (
        VisibilitySettings,
    )


class GlyphVisibilityManager:
    def __init__(self, visibility_settings_handler: "VisibilitySettings") -> None:
        self.visibility_settings_handler = visibility_settings_handler
        self.main_window = visibility_settings_handler.settings_manager.main_window
        self.visibility_states = visibility_settings_handler.get_glyph_visibility()

    def apply_visibility(self, glyph_type, pictograph: "BasePictograph"):
        if glyph_type == "VTG":
            pictograph.vtg_glyph.setVisible(self.visibility_states[glyph_type])
        elif glyph_type == "TKA":
            pictograph.tka_glyph.setVisible(self.visibility_states[glyph_type])
        elif glyph_type == "Elemental":
            pictograph.elemental_glyph.setVisible(self.visibility_states[glyph_type])
        elif glyph_type == "EndPosition":
            pictograph.start_to_end_pos_glyph.setVisible(
                self.visibility_states[glyph_type]
            )

    def apply_current_visibility_settings(self, pictograph: "BasePictograph"):
        for glyph_type in ["VTG", "TKA", "Elemental", "EndPosition"]:
            visibility = self.get_glyph_visibility(glyph_type)
            self.visibility_states[glyph_type] = visibility

            self.apply_visibility(glyph_type, pictograph)

            if pictograph.letter in [Letter.α, Letter.β, Letter.Γ]:
                pictograph.start_to_end_pos_glyph.setVisible(False)

    def should_glyph_be_visible(self, glyph_type: str) -> bool:
        return self.get_glyph_visibility(glyph_type)

    def get_glyph_visibility(self, glyph_type: str) -> bool:
        self.settings_manager = self.main_window.settings_manager
        self.settings = self.visibility_settings_handler.settings
        return self.settings.get("glyph_visibility", {}).get(glyph_type, True)

    def set_glyph_visibility(self, glyph_type: str, visible: bool) -> None:
        if "glyph_visibility" not in self.settings:
            self.settings["glyph_visibility"] = {}
        self.settings["glyph_visibility"][glyph_type] = visible
        self.visibility_settings_handler.set_glyph_visibility(glyph_type, visible)
        self.apply_glyph_visibility()

    def set_visibilty_to_false(self, pictograph: "BasePictograph", glyph_type: str):
        if glyph_type == "TKA":
            pictograph.tka_glyph.setVisible(False)
        elif glyph_type == "VTG":
            pictograph.vtg_glyph.setVisible(False)
        elif glyph_type == "Elemental":
            pictograph.elemental_glyph.setVisible(False)
        elif glyph_type == "EndPosition":
            pictograph.start_to_end_pos_glyph.setVisible(False)

    def apply_glyph_visibility(self) -> None:
        for pictograph_list in self.main_window.main_widget.pictograph_cache.values():
            for pictograph in pictograph_list.values():
                if pictograph.view.isVisible():
                    self.apply_current_visibility_settings(pictograph)

        for (
            beat_view
        ) in (
            self.main_window.main_widget.sequence_widget.beat_frame.beats
        ):
            if beat_view.is_filled:
                self.apply_current_visibility_settings(beat_view.beat)
                beat_view.beat.updater.update_pictograph()

        start_pos = (
            (
                self.main_window.main_widget.sequence_widget.beat_frame.start_pos_view.start_pos
            )
            if hasattr(
                self.main_window.main_widget.sequence_widget.beat_frame.start_pos_view,
                "start_pos",
            )
            else None
        )
        if start_pos:
            if start_pos.view.is_filled:
                self.apply_current_visibility_settings(start_pos)
