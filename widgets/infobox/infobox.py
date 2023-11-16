from PyQt6.QtWidgets import QFrame
from widgets.infobox.infobox_buttons import InfoBoxButtons
from widgets.infobox.infobox_labels import InfoBoxLabels
from widgets.infobox.infobox_widgets import InfoBoxWidgets
from widgets.infobox.infobox_layouts import InfoBoxLayouts
from widgets.graphboard.graphboard import GraphBoard



class InfoBox(QFrame):
    def __init__(self, main_widget, graphboard: "GraphBoard") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = self.main_widget.main_window
        self.graphboard = graphboard
        self.labels = InfoBoxLabels(self, graphboard)
        self.widgets = InfoBoxWidgets(self, graphboard)
        self.layouts = InfoBoxLayouts(self, graphboard)
        self.buttons = InfoBoxButtons(self, graphboard)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.setFixedSize(int(self.main_window.width() * 0.20), int(self.main_window.width() * 0.20))
        self.buttons.setup_buttons()
        self.labels.setup_labels()
        self.widgets.setup_widgets()
        self.layouts.setup_layouts()

    def update(self) -> None:
        self.widgets.update_attribute_widgets()
        if len(self.graphboard.staffs) == 2:
            self.labels.update_type_and_position_label()
