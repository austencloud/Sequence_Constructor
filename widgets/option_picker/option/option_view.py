from PyQt6.QtWidgets import QGraphicsView, QPushButton
from PyQt6.QtCore import Qt
from settings.string_constants import CLOCKWISE, COUNTER_CLOCKWISE, ICON_DIR
from typing import TYPE_CHECKING
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon

from widgets.graph_editor.pictograph.pictograph_view import PictographView

if TYPE_CHECKING:
    from widgets.option_picker.option.option import Option


class OptionView(PictographView):
    def __init__(self, option: "Option") -> None:
        super().__init__(option)
        self.option = option

        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setScene(self.option)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.wheelEvent = lambda event: None
        

    def init_buttons(self) -> None:
        self.rotate_cw_button = self.create_button(
            f"{ICON_DIR}rotate_cw.png",
            lambda: self.option.rotate_pictograph(CLOCKWISE),
        )
        self.rotate_ccw_button = self.create_button(
            f"{ICON_DIR}rotate_ccw.png",
            lambda: self.option.rotate_pictograph(COUNTER_CLOCKWISE),
        )

    def create_button(self, icon_path, action) -> QPushButton:
        button = QPushButton(QIcon(icon_path), "", self)
        button.clicked.connect(action)
        return button

    def configure_button_size_and_position(self, button: QPushButton, size) -> None:
        button.setFixedSize(size, size)
        icon_size = int(size * 0.8)
        button.setIconSize(QSize(icon_size, icon_size))

        # Custom positioning logic if needed
        if button == self.rotate_cw_button:
            button.move(self.width() - size, 0)
        elif button == self.rotate_ccw_button:
            button.move(0, 0)

    def update_OptionView_size(self) -> None:
        view_width = int((self.option.option_picker.width() / 4) - self.option.option_picker.spacing)
        
        self.setFixedWidth(view_width)
        self.setFixedHeight(int(view_width * 90/75))
        
        self.view_scale = view_width / self.option.width()
        
    
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)


        button_size = int(self.width() / 7)
        self.configure_button_size_and_position(self.rotate_cw_button, button_size)
        self.configure_button_size_and_position(self.rotate_ccw_button, button_size)
