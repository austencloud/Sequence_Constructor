from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout
from typing import TYPE_CHECKING
from Enums.letters import Letter
from .advanced_start_pos_ori_picker import (
    AdvancedStartPosOriPicker,
)
from .advanced_start_pos_picker_pictograph_factory import (
    AdvancedStartPosPickerPictographFactory,
)

from ..components.start_pos_picker.advanced_start_pos_picker_pictograph_frame import (
    AdvancedStartPosPickerPictographFrame,
)
from ..components.start_pos_picker.choose_your_start_pos_label import (
    ChooseYourStartPosLabel,
)


if TYPE_CHECKING:
    from ..manual_builder import (
        ManualBuilderWidget,
    )
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class AdvancedStartPosPicker(QWidget):
    def __init__(self, manual_builder: "ManualBuilderWidget"):
        super().__init__(manual_builder)
        self.manual_builder = manual_builder
        self.main_widget = manual_builder.main_widget
        self.start_pos_picker = self.manual_builder.start_pos_picker
        self.start_pos_cache: dict[str, list[BasePictograph]] = {}
        self.pictograph_frame = AdvancedStartPosPickerPictographFrame(self)
        # self.ori_picker = AdvancedStartPosOriPicker(self)
        self.choose_your_start_pos_label = ChooseYourStartPosLabel(self)
        self.pictograph_factory = AdvancedStartPosPickerPictographFactory(
            self, self.start_pos_cache
        )
        self._setup_layout()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()
        self.layout.addStretch(1)
        self.layout.addWidget(self.choose_your_start_pos_label)
        self.layout.addStretch(1)
        # self.layout.addWidget(self.ori_picker)
        # self.layout.addStretch(1)
        self.layout.addLayout(self.grid_layout)
        self.layout.addStretch(1)

    def display_variations(self, variations: list["BasePictograph"]) -> None:
        alpha_variations = []
        beta_variations = []
        gamma_variations = []

        for variation in variations:
            if variation.letter == Letter.α:
                alpha_variations.append(variation)
            elif variation.letter == Letter.β:
                beta_variations.append(variation)
            elif variation.letter == Letter.Γ:
                gamma_variations.append(variation)
        self.start_pos_cache = {
            "α": alpha_variations,
            "β": beta_variations,
            "Γ": gamma_variations,
        }
        all_variations: list["BasePictograph"] = (
            alpha_variations + beta_variations + gamma_variations
        )

        for i, variation in enumerate(all_variations):
            row = i // 4
            col = i % 4
            self.grid_layout.addWidget(variation.view, row, col)
            variation.view.mousePressEvent = (
                lambda event, v=variation: self.on_variation_selected(v)
            )
            self._resize_variation(variation)
            variation.container.update_borders()

    def init_ui(self):
        variations = self.start_pos_picker.start_pos_manager.get_all_start_positions()
        self.display_variations(variations)

    def _resize_variation(self, variation: "BasePictograph") -> None:
        view_width = int(self.manual_builder.height() // 6)
        variation.view.setFixedSize(view_width, view_width)
        variation.view.view_scale = view_width / variation.view.pictograph.width()
        variation.view.resetTransform()
        variation.view.scale(variation.view.view_scale, variation.view.view_scale)
        variation.container.styled_border_overlay.setFixedSize(
            variation.view.width(), variation.view.height()
        )
        variation.container.styled_border_overlay.setFixedSize(
            variation.view.width(), variation.view.height()
        )

    def on_variation_selected(self, variation: "BasePictograph") -> None:
        self.manual_builder.start_pos_picker.start_pos_manager.add_start_pos_to_sequence(
            variation
        )

    def resize_advanced_start_pos_picker(self) -> None:
        # self.ori_picker.resize_default_ori_picker()
        self.choose_your_start_pos_label.set_stylesheet()
        # set the spacing in the grid using set_spacing
        self.grid_layout.setHorizontalSpacing(20)
        self.grid_layout.setVerticalSpacing(20)