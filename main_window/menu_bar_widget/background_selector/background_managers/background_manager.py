from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class BackgroundManager(QObject):
    update_required = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.gradient_shift = 0
        self.color_shift = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_background)
        self.timer.start(50)
# In your background manager's animate_background method

    def animate_background(self):
        self.update_required.emit()
        pass

    def paint_background(self, widget, painter):
        pass

    def start_animation(self):
        if not self.timer.isActive():
            self.timer.start(50)

    def stop_animation(self):
        if self.timer.isActive():
            self.timer.stop()
