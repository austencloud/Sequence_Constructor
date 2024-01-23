import json
import os
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtGui import QResizeEvent
from utilities.TypeChecking.letter_lists import all_letters
from utilities.TypeChecking.TypeChecking import Letters, TYPE_CHECKING, Dict, List
from constants import DIAMOND, STAFF
from widgets.pictograph.pictograph import Pictograph
from ..image_cache_manager import ImageCacheManager
from ..main_tab_widget.main_tab_widget import MainTabWidget
from .main_widget_layout_manager import MainWidgetLayoutManager
from .letter_loader import LetterLoader
from ..sequence_widget.sequence_widget import MainSequenceWidget

if TYPE_CHECKING:
    from main import MainWindow


class MainWidget(QWidget):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self._setup_default_modes()
        self._setup_letters()
        self._setup_components()
        self._setup_layouts()
        self.load_special_placements()

    def load_special_placements(self) -> Dict:
        """Loads the special placements for arrows."""
        directory = "data/arrow_placement/special/"
        self.special_placements = {}
        for file_name in os.listdir(directory):
            if file_name.endswith("_placements.json"):
                with open(os.path.join(directory, file_name), "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.special_placements.update(data)
        return self.special_placements

    def refresh_placements(self):
        """Refreshes the special placements and updates all pictographs."""
        # Reload the special placements
        self.load_special_placements()

        # Iterate over all pictographs and update them
        for letter, pictographs in self.all_pictographs.items():
            for pictograph_key, pictograph in pictographs.items():
                pictograph.updater.update_pictograph()
                
    def _setup_components(self) -> None:
        self.main_sequence_widget = MainSequenceWidget(self)
        self.main_tab_widget = MainTabWidget(self)
        self.image_cache_manager = ImageCacheManager(self)

    def _setup_layouts(self) -> None:
        self.layout_manager = MainWidgetLayoutManager(self)
        self.layout_manager.configure_layouts()

    def _setup_default_modes(self) -> None:
        self.prop_type = STAFF
        self.grid_mode = DIAMOND

    def _setup_letters(self) -> None:
        self.all_pictographs: Dict[Letters, Dict[str, Pictograph]] = {
            letter: {} for letter in all_letters
        }
        self.letter_loader = LetterLoader(self)
        self.letters: Dict[Letters, List[Dict]] = self.letter_loader.load_all_letters()

    ### EVENT HANDLERS ###

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.main_sequence_widget.resize_sequence_widget()
        self.main_tab_widget.codex.resize_codex()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.main_window.window_manager.set_dimensions()

    layout: QHBoxLayout
