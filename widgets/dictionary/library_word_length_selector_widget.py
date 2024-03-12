import os
import json
from typing import TYPE_CHECKING
from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtGui import QStandardItem, QDragEnterEvent, QDropEvent
from Enums.letters import Letter, LetterConditions
from widgets.dictionary.dictionary_sequence_populator import DictionarySequencePopulator
from widgets.dictionary.dictionary_sort_manager import DictionarySortManager
from .dictionary_favorites_manager import DictionaryFavoritesTree
from .dictionary_search_sort_bar import DictionarySearchSortBar
from .dictionary_sequence_length_manager import DictionarySortByLengthHandler
from .dictionary_words_tree import DictionaryWordsTree

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QTreeView,
    QHBoxLayout,
    QPushButton,
)

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.dictionary.dictionary import Dictionary


class LibraryWordLengthSelectorWidget(QWidget):
    def __init__(self, dictionary: "Dictionary") -> None:
        super().__init__(dictionary)
        self.dictionary = dictionary
        self.main_widget = dictionary.main_widget
        self.sort_manager = dictionary.sort_manager
        self.setup_ui()

    def setup_ui(self) -> None:
        self.layout = QHBoxLayout()
        word_lengths = [2, 3, 4, 5, 6, 7, 8]
        visibility_settings = (
            self.main_widget.main_window.settings_manager.get_word_length_visibility()
        )
        for length in word_lengths:
            button = QPushButton(f"{length} letters")
            button.setCheckable(True)
            button.setChecked(visibility_settings.get(length, False))
            button.toggled.connect(
                lambda checked, length=length: self.toggle_word_length_visibility(
                    length, checked
                )
            )
            self.layout.addWidget(button)

        self.setLayout(self.layout)

    def toggle_word_length_visibility(self, length, visible):
        visibility_settings = (
            self.main_widget.main_window.settings_manager.get_word_length_visibility()
        )
        visibility_settings[str(length)] = visible
        self.main_widget.main_window.settings_manager.set_word_length_visibility(
            visibility_settings
        )
        self.sort_manager.filter_sequences_by_length()