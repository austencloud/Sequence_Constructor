from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSizePolicy, QApplication, QMenu
from PyQt6.QtCore import Qt, QEvent, QTimer
from PyQt6.QtGui import QMouseEvent, QCursor, QKeyEvent, QAction, QContextMenuEvent

from base_widgets.base_pictograph.bordered_pictograph_view import BorderedPictographView
from base_widgets.base_pictograph.pictograph_context_menu_handler import (
    PictographContextMenuHandler,
)
from base_widgets.base_pictograph.pictograph_view_key_event_handler import (
    PictographViewKeyEventHandler,
)


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from main_window.main_widget.construct_tab.option_picker.option_picker import (
        OptionPicker,
    )


class OptionPickerPictographView(BorderedPictographView):
    original_style: str

    def __init__(
        self, pictograph: "BasePictograph", option_picker: "OptionPicker"
    ) -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph
        self.pictograph.view = self
        self.option_picker = option_picker
        self.original_style = ""
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.grabGesture(Qt.GestureType.TapGesture)
        self.grabGesture(Qt.GestureType.TapAndHoldGesture)

        # self.mouse_event_handler = PictographViewMouseEventHandler(self)
        self.context_menu_handler = PictographContextMenuHandler(self)
        self.key_event_handler = PictographViewKeyEventHandler(self)

        self._gestureInProgress = False
        self._ignoreMouseEvents = False
        self._ignoreNextMousePress = False
        self._touchTimeout = QTimer(self)
        self._touchTimeout.setSingleShot(True)
        self._touchTimeout.timeout.connect(self._resetTouchState)
        self._touchTimeout.setInterval(100)

    ### EVENTS ###

    def contextMenuEvent(self, event: QEvent) -> None:
        """
        Optionally, add more actions specific to OptionPickerPictographView.
        Then call the base class to include the "Copy Dictionary" action.
        """
        if isinstance(event, QContextMenuEvent):
            context_menu = QMenu(self)

            # Add any specific actions for OptionPicker here

            # Add a separator
            context_menu.addSeparator()

            # Call the base class to add "Copy Dictionary"
            copy_action = QAction("Copy Dictionary", self)
            copy_action.triggered.connect(self.copy_pictograph_dict)
            context_menu.addAction(copy_action)

            # Execute the menu
            context_menu.exec(QCursor.pos())
        else:
            super().contextMenuEvent(event)

    def set_enabled(self, enabled: bool) -> None:
        self._ignoreMouseEvents = not enabled

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if not self.key_event_handler.handle_key_press(event):
            super().keyPressEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        settings_manager = self.pictograph.main_widget.main_window.settings_manager
        current_prop_type = settings_manager.global_settings.get_prop_type()

        if (
            self.pictograph.prop_type != current_prop_type
            and self.pictograph.__class__.__name__ != "GE_BlankPictograph"
        ):
            settings_manager.global_settings.prop_type_changer.replace_props(
                current_prop_type, self.pictograph
            )
        if not self.pictograph.quiz_mode:
            settings_manager.visibility.glyph_visibility_manager.apply_current_visibility_settings(
                self.pictograph
            )

    def _resetTouchState(self) -> None:
        self._ignoreNextMousePress = False

    def mousePressEvent(self, event: QMouseEvent) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if self._ignoreMouseEvents or self._ignoreNextMousePress:
            event.ignore()
            return
        elif event.button() == Qt.MouseButton.LeftButton:
            self.pictograph.main_widget.construct_tab.option_picker.construct_tab.option_click_handler.on_option_clicked(
                self.pictograph
            )
        QApplication.restoreOverrideCursor()

    def enterEvent(self, event: QEvent) -> None:
        from main_window.main_widget.sequence_widget.graph_editor.pictograph_container.GE_pictograph_container import (
            GraphEditorPictographContainer,
        )

        if isinstance(self.parent(), GraphEditorPictographContainer):
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        else:
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pictograph.view.set_gold_border()

    def leaveEvent(self, event: QEvent) -> None:
        self.setStyleSheet("")
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.pictograph.view.reset_border()

    def resizeEvent(self, event):
        """Trigger fitInView whenever the widget is resized."""
        super().resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        size = self.calculate_view_size()
        self.pictograph.view.update_border_widths()
        self.setMinimumWidth(size)
        self.setMaximumWidth(size)
        self.setMinimumHeight(size)
        self.setMaximumHeight(size)
        self.view_scale = size / self.pictograph.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def calculate_view_size(self) -> int:
        spacing = self.option_picker.scroll_area.spacing

        calculated_width = int(
            (self.pictograph.main_widget.construct_tab.width() / 8) - spacing
        )

        view_width = (
            calculated_width
            if calculated_width
            < self.pictograph.main_widget.construct_tab.height() // 8
            else self.pictograph.main_widget.construct_tab.height() // 8
        )

        outer_border_width = max(1, int(view_width * 0.015))
        inner_border_width = max(1, int(view_width * 0.015))

        view_width = view_width - (outer_border_width) - (inner_border_width) - spacing

        return view_width
