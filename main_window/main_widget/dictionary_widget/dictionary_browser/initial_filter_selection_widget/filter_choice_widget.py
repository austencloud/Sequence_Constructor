from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QSizePolicy,
    QSpacerItem,
)
from PyQt6.QtGui import QFont, QResizeEvent
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_browser.initial_filter_selection_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class FilterChoiceWidget(QWidget):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget)
        self.initial_selection_widget = initial_selection_widget
        self.buttons: dict[str, QPushButton] = {}
        self.button_labels: dict[str, QLabel] = {}
        self.browser = initial_selection_widget.browser
        self.main_widget = initial_selection_widget.browser.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a descriptive label at the top
        main_layout.addStretch(2)
        self.description_label = QLabel("Choose a filter:")
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.description_label)
        # add stretch
        main_layout.addStretch(1)
        # Create a grid layout for the filter options
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(50)
        grid_layout.setVerticalSpacing(30)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Define filter options and their descriptions
        filter_options = [
            (
                "Starting Letter",
                "Display sequences that start with a specific letter.",
                self.initial_selection_widget.show_starting_letter_section,
            ),
            (
                "Contains Letter",
                "Display sequences that contain specific letters.",
                self.initial_selection_widget.show_contains_letter_section,
            ),
            (
                "Sequence Length",
                "Display sequences by length.",
                self.initial_selection_widget.show_length_section,
            ),
            (
                "Level",
                "Display sequences by difficulty level.",
                self.initial_selection_widget.show_level_section,
            ),
            (
                "Starting Position",
                "Display sequences by starting position.",
                self.initial_selection_widget.show_starting_position_section,
            ),
            (
                "Author",
                "Display sequences by author.",
                self.initial_selection_widget.show_author_section,
            ),
        ]

        # Add buttons and descriptions to the grid layout
        for index, (label, description, handler) in enumerate(filter_options):
            button = QPushButton(label)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(handler)
            self.buttons[label] = button

            description_label = QLabel(description)
            description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.button_labels[label] = description_label

            # Create a vertical layout for each button and its description
            vbox = QVBoxLayout()
            vbox.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
            vbox.addWidget(description_label, alignment=Qt.AlignmentFlag.AlignCenter)

            row = index // 3  # Keep grid rows even
            col = index % 3  # Calculate column number

            grid_layout.addLayout(vbox, row, col)

        main_layout.addLayout(grid_layout)
        # Add "Show All" button and description at the bottom
        show_all_sequences_button = QPushButton("Show all")
        show_all_sequences_button.setCursor(Qt.CursorShape.PointingHandCursor)
        show_all_sequences_button.clicked.connect(
            self.initial_selection_widget.browser.show_all_sequences
        )
        self.buttons["Show all sequences"] = show_all_sequences_button

        show_all_description_label = QLabel("Display every sequence in the dictionary.")
        show_all_description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_labels["Show all sequences"] = show_all_description_label

        # Create a vertical layout for the "Show all" button and its description
        show_all_vbox = QVBoxLayout()
        show_all_vbox.addWidget(
            show_all_sequences_button, alignment=Qt.AlignmentFlag.AlignCenter
        )
        show_all_vbox.addWidget(
            show_all_description_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        grid_layout.addLayout(show_all_vbox, 3, 1)  # Centered in the grid

        main_layout.addStretch(2)
        self.setLayout(main_layout)

    def get_current_filter(self):
        return self.browser.current_filter

    def resize_filter_choice_widget(self):
        self._resize_buttons_labels()
        self._resize_buttons()
        self._resize_description_label()
        self._resize_all_labels_in_children()

    def _resize_all_labels_in_children(self):
        for filter_choice_section in self.initial_selection_widget.sections:
            # get all the labels that are children of those widgets
            for label in filter_choice_section.findChildren(QLabel):
                # add to the stylesheet to make it the correct font color
                font_color = self.settings_manager.global_settings.get_current_font_color()
                label.setStyleSheet(f"color: {font_color};")

    def _resize_description_label(self):
        font_color = self.settings_manager.global_settings.get_current_font_color()
        font_size = self.main_widget.width() // 30
        font_family = "Monotype Corsiva"
        self.description_label.setStyleSheet(
            f"font-size: {font_size}px; color: {font_color}; font-family: {font_family};"
        )

    def _resize_buttons(self):
        button_font = QFont()
        button_font.setPointSize(self.main_widget.width() // 80)
        for button in self.buttons.values():
            button.setFixedWidth(self.main_widget.width() // 7)
            button.setFixedHeight(self.main_widget.height() // 10)
            button.setFont(button_font)

    def _resize_buttons_labels(self):
        font_size = self.main_widget.width() // 150
        font_color = self.settings_manager.global_settings.get_current_font_color()
        for button_label in self.button_labels.values():
            button_label.setStyleSheet(
                f"font-size: {font_size}px; color: {font_color};"
            )

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self.resize_filter_choice_widget()
        return super().resizeEvent(a0)
