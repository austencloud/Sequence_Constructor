from PyQt6.QtWidgets import QGraphicsItemGroup
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from base_widgets.base_pictograph.pictograph_view import PictographView
from typing import TYPE_CHECKING, Union
from PyQt6.QtCore import Qt, QEvent
from base_widgets.base_pictograph.glyphs.tka_glyph.base_glyph import BaseGlyph

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.visibility_tab.visibility_tab import (
        VisibilityTab,
    )
    from PyQt6.QtSvgWidgets import QGraphicsSvgItem

Glyph = Union["BaseGlyph", "QGraphicsItemGroup", "QGraphicsSvgItem"]


class VisibilityTabPictographView(PictographView):
    def __init__(self, visibility_tab: "VisibilityTab"):
        self.visibility_tab = visibility_tab
        self.main_widget = visibility_tab.main_widget
        self.settings = self.main_widget.settings_manager.visibility

        self.pictograph = self._initialize_example_pictograph()
        super().__init__(self.pictograph)
        for glyph in self._get_all_glyphs():
            glyph.setOpacity(
                1
                if self.settings.glyph_visibility_manager.should_glyph_be_visible(
                    glyph.name
                )
                else 0.1
            )
        self.set_clickable_glyphs()
        self.setMouseTracking(True)
        self.add_hover_effect()

    def add_hover_effect(self):
        def apply_hover_effects(item: "Glyph"):
            item.setCursor(Qt.CursorShape.PointingHandCursor)
            item.hoverEnterEvent = self._create_hover_enter_event(item)
            item.hoverLeaveEvent = self._create_hover_leave_event(item)
            for child in item.childItems():
                apply_hover_effects(child)

        for glyph in self._get_all_glyphs():
            apply_hover_effects(glyph)

    def _create_hover_enter_event(self, glyph: "Glyph"):
        def hoverEnterEvent(event):
            glyph.setOpacity(0.5)

        return hoverEnterEvent

    def _create_hover_leave_event(self, glyph: "Glyph"):
        def hoverLeaveEvent(event):
            visible = self.settings.glyph_visibility_manager.should_glyph_be_visible(
                glyph.name
            )
            if visible:
                glyph.setOpacity(1)
            else:
                glyph.setOpacity(0.1)

        return hoverLeaveEvent

    def _initialize_example_pictograph(self) -> BasePictograph:
        """Create and initialize the example pictograph."""
        example_data = {
            "letter": "A",
            "start_pos": "alpha1",
            "end_pos": "alpha3",
            "blue_motion_type": "pro",
            "red_motion_type": "pro",
        }
        pictograph = BasePictograph(self.main_widget)
        pictograph_dict = self.main_widget.pictograph_dict_loader.find_pictograph_dict(
            example_data
        )
        pictograph.red_reversal = True
        pictograph.blue_reversal = True
        pictograph.updater.update_pictograph(pictograph_dict)

        pictograph.tka_glyph.setVisible(True)
        pictograph.vtg_glyph.setVisible(True)
        pictograph.elemental_glyph.setVisible(True)
        pictograph.start_to_end_pos_glyph.setVisible(True)
        pictograph.reversal_glyph.setVisible(True)

        return pictograph

    def _get_all_glyphs(self) -> list[Glyph]:
        """Return a list of all glyphs in the pictograph."""
        return [
            self.pictograph.tka_glyph,
            self.pictograph.vtg_glyph,
            self.pictograph.elemental_glyph,
            self.pictograph.start_to_end_pos_glyph,
            self.pictograph.reversal_glyph,
        ]

    def set_clickable_glyphs(self):
        """Enable glyphs to be clickable and toggle visibility."""
        for glyph in self._get_all_glyphs():
            glyph.mousePressEvent = self._create_mouse_press_event(glyph)

    def _create_mouse_press_event(self, glyph: "Glyph"):
        def mousePressEvent(event):
            self._toggle_glyph_visibility(glyph)
            if self.settings.glyph_visibility_manager.should_glyph_be_visible(
                glyph.name
            ):
                glyph.setOpacity(1)
            else:
                glyph.setOpacity(0.15)

        return mousePressEvent

    def _toggle_glyph_visibility(self, glyph: BaseGlyph):
        """Toggle glyph visibility and synchronize with checkboxes."""
        manager = self.settings.glyph_visibility_manager
        current_visibility = manager.should_glyph_be_visible(glyph.name)
        self.settings.set_glyph_visibility(glyph.name, not current_visibility)
        self.visibility_tab.checkbox_widget.update_checkboxes()

    def resizeEvent(self, event: QEvent):
        tab_width = (
            self.visibility_tab.width() - self.visibility_tab.checkbox_widget.width()
        )
        size = int(tab_width * 0.8)
        self.setFixedSize(size, size)
        super().resizeEvent(event)
