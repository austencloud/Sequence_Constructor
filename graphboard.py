from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QApplication, QGraphicsRectItem, QAction, QMenu
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QPointF, QTimer
from PyQt5.QtWidgets import QGraphicsItem, QToolTip
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor, QTransform, QImage
from staff import Staff
from grid import Grid
from arrow import Arrow
import os
from handlers import Arrow_Manipulator




class Graphboard(QGraphicsView):
    arrowMoved = pyqtSignal()
    attributesChanged = pyqtSignal()

    def __init__(self, graphboard_scene, grid, info_tracker, staff_manager, svg_handler, ui_setup, parent=None):
        super().__init__(graphboard_scene, parent)
        self.setAcceptDrops(True)
        self.dragging = None
        self.grid = grid
        self.staff_manager = staff_manager
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setInteractive(True)
        self.graphboard_scene = graphboard_scene
        self.graphboard_scene.setBackgroundBrush(Qt.white) 
        self.info_tracker = info_tracker
        self.svg_handler = svg_handler
        self.ui_setup = ui_setup
        self.renderer = QSvgRenderer()
        self.arrowMoved.connect(self.update_staffs_and_check_beta)
        self.attributesChanged.connect(self.update_staffs_and_check_beta)
    
        # Create a dictionary to store the SVG renderers for each letter
        self.letter_renderers = {}

        # Load the SVG files for all the letters and store the renderers in the dictionary
        for letter in 'ABCDEFGHIJKLMNOPQRSTUV':
            renderer = QSvgRenderer(f'images/letters/{letter}.svg')
            self.letter_renderers[letter] = renderer


        # Create a new QGraphicsSvgItem for the letter and add it to the scene
        self.letter_item = QGraphicsSvgItem()
        self.graphboard_scene.addItem(self.letter_item)
        self.arrow_manipulator = Arrow_Manipulator(self.graphboard_scene, self)
        self.setFixedSize(750, 900)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.graphboard_scene.addItem(self.grid)
        self.drag = Quadrant_Preview_Drag(self, self.dragging)

    def mousePressEvent(self, event):
        self.dragStartPosition = event.pos()
        self.setFocus()
        items = self.items(event.pos())
        if items and items[0].flags() & QGraphicsItem.ItemIsMovable:
            if event.button() == Qt.LeftButton and event.modifiers() == Qt.ControlModifier:
                items[0].setSelected(not items[0].isSelected())
            elif not items[0].isSelected():
                for item in self.scene().selectedItems():
                    item.setSelected(False)
                items[0].setSelected(True)
            self.dragging = items[0]
            self.dragOffset = self.mapToScene(event.pos()) - self.dragging.pos()
            
        else:
            for item in self.scene().selectedItems():
                item.setSelected(False)
            self.dragging = None


        if items:
            print(f"Clicked on an object of type {type(items[0])}")
            print(f"Object top-left position: {items[0].scenePos()}")
            print(f"Object center: {items[0].scenePos() + items[0].boundingRect().center()}")
            if hasattr(items[0], 'svg_file'):
                print(f"Object svg: {items[0].svg_file}")

        if event.button() == Qt.LeftButton and not items:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.pos() - self.dragStartPosition).manhattanLength() < QApplication.startDragDistance():
            return
        if self.dragging:
            new_pos = self.mapToScene(event.pos()) - self.dragOffset
            movement = new_pos - self.dragging.pos()

            for item in self.scene().selectedItems():
                if isinstance(item, Arrow):
                    item.setPos(item.pos() + movement)

                if isinstance(item, Arrow):
                    center_pos = item.pos() + item.boundingRect().center()

                    quadrant = self.drag.get_graphboard_quadrants(center_pos)

                    item.quadrant = quadrant
                    base_name = os.path.basename(item.svg_file)

                    if base_name.startswith('red_anti'):
                        new_svg = f'images\\arrows\\red_anti_{item.rotation}_{quadrant}.svg'
                    elif base_name.startswith('red_iso'):
                        new_svg = f'images\\arrows\\red_iso_{item.rotation}_{quadrant}.svg'
                    elif base_name.startswith('blue_anti'):
                        new_svg = f'images\\arrows\\blue_anti_{item.rotation}_{quadrant}.svg'
                    elif base_name.startswith('blue_iso'):
                        new_svg = f'images\\arrows\\blue_iso_{item.rotation}_{quadrant}.svg'
                    else:
                        print(f"Unexpected svg_file: {item.svg_file}")
                        new_svg = item.svg_file 
                
                    new_renderer = QSvgRenderer(new_svg)
                    if new_renderer.isValid():
                        item.setSharedRenderer(new_renderer)
                        item.svg_file = new_svg
                        item.update_locations()
                self.arrowMoved.emit()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
        item = self.itemAt(event.pos())
        if isinstance(item, Arrow):
            item.in_graphboard = True
        super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        self.last_known_pos = event.pos() 
        if event.mimeData().hasFormat('text/plain'):
            dropped_svg = event.mimeData().text()
            base_name = os.path.basename(dropped_svg)
            color, type_, rotation, quadrant = base_name.split('_')[:4]
            for item in self.scene().items():
                if isinstance(item, Arrow):
                    if item.color == color:
                        event.ignore()
                        QToolTip.showText(QCursor.pos(), "Cannot add another arrow of the same color.")
                        return
            event.accept()
            QToolTip.hideText() 
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        item = self.itemAt(self.last_known_pos)
        if isinstance(item, Arrow):
            item.in_graphboard = False
        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        self.setFocus()
        if event.mimeData().hasFormat('text/plain'):
            event.setDropAction(Qt.CopyAction)
            event.accept()
            dropped_svg = event.mimeData().text()

            self.arrow_item = Arrow(dropped_svg, self, self.info_tracker, self.svg_handler,  self.arrow_manipulator)
            self.arrow_item.setFlag(QGraphicsSvgItem.ItemIsFocusable, True)
            self.scene().addItem(self.arrow_item)
            pos = self.mapToScene(event.pos()) - self.arrow_item.boundingRect().center()
            self.arrow_item.setPos(pos)

            for item in self.scene().items():
                if isinstance(item, Arrow):
                    item.setSelected(False)
            self.arrow_item.setSelected(True)
            end_location = self.arrow_item.end_location
            self.staff_manager.show_staff(end_location + "_staff_" + self.arrow_item.color)
        else:
            event.ignore()

        # Adjust the y-coordinate of the arrow's position to account for the new position of the grid
        adjusted_arrow_pos = self.arrow_item.pos() + QPointF(0, 75)
        quadrant = self.drag.get_graphboard_quadrants(adjusted_arrow_pos)
        self.arrow_item.quadrant = quadrant
        self.drag.update_arrow_svg(self.arrow_item, quadrant)  # Update the arrow's SVG file
        self.arrow_item.attributesChanged.emit()
        self.arrowMoved.emit()

    def contextMenuEvent(self, event):
        clicked_item = self.itemAt(self.mapToScene(event.pos()).toPoint())
        selected_items = self.get_selected_items()
        if isinstance(clicked_item, Arrow):
            arrow_menu = QMenu(self)

            delete_action = QAction('Delete', self)
            delete_action.triggered.connect(lambda: self.arrow_manipulator.delete_arrow(selected_items))
            arrow_menu.addAction(delete_action)

            rotate_right_action = QAction('Rotate Right', self)
            rotate_right_action.triggered.connect(lambda: self.arrow_manipulator.rotateArrow("right", selected_items))
            arrow_menu.addAction(rotate_right_action)

            rotate_left_action = QAction('Rotate Left', self)
            rotate_left_action.triggered.connect(lambda: self.arrow_manipulator.rotateArrow("left", selected_items))
            arrow_menu.addAction(rotate_left_action)

            mirror_action = QAction('Mirror', self)
            mirror_action.triggered.connect(lambda: self.arrow_manipulator.mirrorArrow(selected_items))
            arrow_menu.addAction(mirror_action)

            bring_forward_action = QAction('Bring Forward', self)
            bring_forward_action.triggered.connect(lambda: self.arrow_manipulator.bringForward(selected_items))
            arrow_menu.addAction(bring_forward_action)
            arrow_menu.exec_(event.globalPos())

        elif isinstance(clicked_item, Staff):
            staff_menu = QMenu(self)

            delete_action = QAction('Delete', self)
            delete_action.triggered.connect(lambda: self.arrow_manipulator.delete_arrow(selected_items))
            staff_menu.addAction(delete_action)

            rotate_right_action = QAction('Rotate Right', self)
            rotate_right_action.triggered.connect(lambda: self.arrow_manipulator.rotateArrow("right", selected_items))
            staff_menu.addAction(rotate_right_action)

            rotate_left_action = QAction('Rotate Left', self)
            rotate_left_action.triggered.connect(lambda: self.arrow_manipulator.rotateArrow("left", selected_items))
            staff_menu.addAction(rotate_left_action)
            staff_menu.exec_(event.globalPos())

        else: 
            graphboard_menu = QMenu(self)

            swap_colors_action = QAction('Swap Colors', self)
            swap_colors_action.triggered.connect(lambda: self.arrow_manipulator.swapColors(self.get_selected_items()))
            graphboard_menu.addAction(swap_colors_action)

            select_all_action = QAction('Select All', self)
            select_all_action.triggered.connect(self.arrow_manipulator.selectAll)
            graphboard_menu.addAction(select_all_action)

            add_to_sequence_action = QAction('Add to Sequence', self)
            self.sequence_manager = self.ui_setup.get_sequence_manager()
            add_to_sequence_action.triggered.connect(lambda _: self.sequence_manager.add_to_sequence(self))
            graphboard_menu.addAction(add_to_sequence_action)

            export_as_png_action = QAction('Export to PNG', self)
            export_as_png_action.triggered.connect(self.handlers.exporter.exportAsPng)
            graphboard_menu.addAction(export_as_png_action)

            export_as_svg_action = QAction('Export to SVG', self)
            export_as_svg_action.triggered.connect(self.handlers.exporter.exportAsSvg)
            graphboard_menu.addAction(export_as_svg_action)

            graphboard_menu.exec_(event.globalPos())

    def print_item_types(self):
        for item in self.scene().items():
            print(type(item))

    def clear_selection(self):
        for item in self.scene().selectedItems():
            item.setSelected(False)

    def get_bounding_box(self):
        # return all QGraphicsItem objects that represent bounding boxes in the scene
        bounding_boxes = []
        for item in self.scene().items():
            if isinstance(item, QGraphicsRectItem):  # or whatever class represents your bounding boxes
                bounding_boxes.append(item)
        return bounding_boxes

    def get_state(self):
        state = {
            'arrows': [],
            'staffs': [],
            'grid': None
        }
        for item in self.scene().items():
            if isinstance(item, Arrow):
                state['arrows'].append({
                    'color': item.color,
                    'position': item.pos(),
                    'quadrant': item.quadrant,
                    'rotation': item.rotation,
                    'svg_file': item.svg_file
                })
            elif isinstance(item, Staff):
                state['staffs'].append({
                    'position': item.pos(),
                    'color': item.color,
                    'svg_file': item.svg_file
                })
            elif isinstance(item, Grid):
                state['grid'] = {
                    'position': item.pos(),
                    'svg_file': item.svg_file
                }
        return state
    
    def set_handlers(self, handlers):
        self.handlers = handlers

    def set_info_tracker(self, info_tracker):
        self.info_tracker = info_tracker
    
    def get_quadrant_center(self, quadrant):
        centers = {
            'ne': QPointF(550, 175),
            'se': QPointF(550, 550),
            'sw': QPointF(175, 550),
            'nw': QPointF(175, 175),
        }
        return centers.get(quadrant, QPointF(0, 0))
    
    def selectAllItems(self):
        for item in self.scene().items():
            item.setSelected(True)

    def getExpandedQuadrantCenter(self, quadrant):
        centers = {
            'ne1': QPointF(525, 175),
            'ne2': QPointF(575, 100),
            'se1': QPointF(525, 525),
            'se2': QPointF(575, 600),
            'sw1': QPointF(175, 525),
            'sw2': QPointF(150, 600),
            'nw1': QPointF(175, 175),
            'nw2': QPointF(150, 100),
        }
        return centers.get(quadrant, QPointF(0, 0))
    
    def getCurrentArrowPositions(self):
        red_position = None
        blue_position = None

        for item in self.scene().items():
            if isinstance(item, Arrow):
                # Calculate the center of the arrow
                center = item.pos() + item.boundingRect().center()
                if item.color == 'red':
                    red_position = center
                elif item.color == 'blue':
                    blue_position = center
        print(red_position, blue_position)
        return red_position, blue_position


    def get_selected_items(self):
        return self.graphboard_scene.selectedItems()
    
    def select_all_arrows(self):
        for item in self.graphboard_scene.items():
            if isinstance(item, Arrow):
                item.setSelected(True)

    def update_staffs_and_check_beta(self):
        self.staff_manager.remove_beta_staves()
        self.staff_manager.update_graphboard_staffs(self.scene())
        self.staff_manager.check_and_replace_staves()

    def remove_non_beta_staves(self):
        self.staff_manager.remove_non_beta_staves()

    def set_info_tracker(self, info_tracker):
        self.info_tracker = info_tracker

    def get_attributes(self):
        attributes = {}
        base_name = os.path.basename(self.svg_file)
        parts = base_name.split('_')

        attributes['color'] = parts[0]
        attributes['type'] = parts[1]
        attributes['rotation'] = 'Clockwise' if parts[2] == 'r' else 'Anti-clockwise'
        attributes['quadrant'] = parts[3].split('.')[0]

        return attributes
    
    def resizeEvent(self, event):
        self.setSceneRect(QRectF(self.rect()))
        super().resizeEvent(event)

    def deleteAllArrows(self):
        for item in self.scene().items():
            if isinstance(item, Arrow):
                self.scene().removeItem(item)
                del item
        self.arrowMoved.emit()
        if self.info_tracker is not None:
            self.info_tracker.update()

        self.staff_manager.hide_all()

    def clear(self):
        for item in self.scene().items():
            if isinstance(item, Arrow) or isinstance(item, Staff):
                self.scene().removeItem(item)
                del item
        self.arrowMoved.emit()
        if self.info_tracker is not None:
            self.info_tracker.update()

    def keyPressEvent(self, event):
        key = event.key()
        dx = dy = 0
        if key == Qt.Key_Up:
            dy = -15
        elif key == Qt.Key_Down:
            dy = 15
        elif key == Qt.Key_Left:
            dx = -15
        elif key == Qt.Key_Right:
            dx = 15
        else:
            super().keyPressEvent(event)
            return

        for item in self.scene().selectedItems():
            if isinstance(item, Arrow):
                item.moveBy(dx, dy)
                self.arrowMoved.emit()




class Quadrant_Preview_Drag(QDrag):
    def __init__(self, source, arrow_item, *args, **kwargs):
        super().__init__(source, *args, **kwargs)
        self.arrow_item = arrow_item
        self.timer = QTimer()
        self.timer.timeout.connect(self.updatePixmap)

    def exec_(self, *args, **kwargs):
        self.timer.start(100)
        result = super().exec_(*args, **kwargs)
        self.timer.stop()
        return result

    def updatePixmap(self):
        mouse_pos = self.source().mapFromGlobal(self.source().cursor().pos())

        quadrant, base_name = self.get_graphboard_quadrants(mouse_pos)
        self.update_arrow_svg(self.arrow_item, quadrant)


        new_svg = f'images\\arrows\\red\\r\\anti\\red_anti_r_{quadrant}.svg'

        new_renderer = QSvgRenderer(new_svg)
        #delete the old svg from the screen
        self.arrow_item.setSharedRenderer(new_renderer)

        if new_renderer.isValid():
            pixmap = QPixmap(self.pixmap().size())
            painter = QPainter(pixmap)
            new_renderer.render(painter)
            painter.end()
            self.setPixmap(pixmap)

    def get_graphboard_quadrants(self, mouse_pos):
        mime_data = self.mimeData()
        if mime_data is not None:
            base_name = os.path.basename(mime_data.text())
        else:
            base_name = ""
        # Adjust the y-coordinate of the mouse position to account for the new position of the grid
        adjusted_mouse_y = mouse_pos.y() + 75
        if adjusted_mouse_y < self.source().sceneRect().height() / 2:
            if mouse_pos.x() < self.source().sceneRect().width() / 2:
                quadrant = 'nw'
            else:
                quadrant = 'ne'
        else:
            if mouse_pos.x() < self.source().sceneRect().width() / 2:
                quadrant = 'sw'
            else:
                quadrant = 'se'
        return quadrant

    
    def update_arrow_svg(self, arrow, quadrant):
        base_name = os.path.basename(arrow.svg_file)

        if base_name.startswith('red_anti'):
            new_svg = f'images\\arrows\\red_anti_{arrow.rotation}_{quadrant}.svg'
        elif base_name.startswith('red_iso'):
            new_svg = f'images\\arrows\\red_iso_{arrow.rotation}_{quadrant}.svg'
        elif base_name.startswith('blue_anti'):
            new_svg = f'images\\arrows\\blue_anti_{arrow.rotation}_{quadrant}.svg'
        elif base_name.startswith('blue_iso'):
            new_svg = f'images\\arrows\\blue_iso_{arrow.rotation}_{quadrant}.svg'
        else:
            print(f"Unexpected svg_file: {arrow.svg_file}")
            new_svg = arrow.svg_file 

        new_renderer = QSvgRenderer(new_svg)
        if new_renderer.isValid():
            arrow.setSharedRenderer(new_renderer)
            arrow.svg_file = new_svg
            arrow.update_locations()
