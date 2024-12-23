import json
import os
from typing import TYPE_CHECKING

from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SpecialPlacementLoader:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self.special_placements: dict[str, dict[str, dict[str, dict[str, int]]]] = {
            "from_layer1": {},
            "from_layer2": {},
            "from_layer3_blue2_red1": {},
            "from_layer3_blue1_red2": {},
        }

    def load_special_placements(
        self, grid_mode: str
    ) -> dict[str, dict[str, dict[str, dict[str, int]]]]:
        for subfolder in [
            "from_layer1",
            "from_layer2",
            "from_layer3_blue2_red1",
            "from_layer3_blue1_red2",
        ]:

            directory = get_images_and_data_path(
                f"data/arrow_placement/{grid_mode}/special/{subfolder}"
            )
            for file_name in os.listdir(directory):
                if file_name.endswith("_placements.json"):
                    with open(
                        os.path.join(directory, file_name), "r", encoding="utf-8"
                    ) as file:
                        data = json.load(file)
                        self.special_placements[subfolder].update(data)
        return self.special_placements

    def refresh_placements(self, grid_mode: str = None) -> None:
        """Refreshes the special placements and updates all pictographs."""
        if not grid_mode:
            grid_mode = self.main_widget.settings_manager.global_settings.get_grid_mode()
        self.main_widget.special_placements = self.load_special_placements(grid_mode)

        for _, pictograph_list in self.main_widget.pictograph_cache.items():
            for _, pictograph in pictograph_list.items():
                pictograph_grid_mode = self.main_widget.grid_mode_checker.get_grid_mode(
                    pictograph.pictograph_dict
                )
                # if pictograph_grid_mode == grid_mode:
                #     pictograph.updater.update_pictograph()
                #     pictograph.update()
