import os
import json
import os
import xml.etree.ElementTree as ET
import json
import re
from PyQt5.QtGui import QImage, QPainter, QPainterPath, QTransform
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QMenu, QDialog, QFormLayout, QSpinBox, QDialogButtonBox
from PyQt5.QtCore import Qt, pyqtSignal
from svg.path import Line, CubicBezier, QuadraticBezier, Arc, Close
from arrow import Arrow
from staff import Staff
from grid import Grid
from lxml import etree
from copy import deepcopy


class Arrow_Handler:
    arrowMoved = pyqtSignal()

    def __init__(self, graphboard_scene, graphboard):
        self.graphboard_scene = graphboard_scene
        self.graphboard = graphboard

    def move_arrow_quadrant_up(self):
        self.selected_arrow = self.graphboard.get_selected_items()[0]
        print(self.selected_arrow)
        if self.selected_arrow.quadrant == 'se':
            self.selected_arrow.quadrant = 'ne'
        elif self.selected_arrow.quadrant == 'sw':
            self.selected_arrow.quadrant = 'nw'
        # Update the arrow's position and orientation on the graphboard
        print(self.selected_arrow.quadrant)
    def move_arrow_quadrant_left(self):
        self.selected_arrow = self.graphboard.get_selected_items()[0]
        if self.selected_arrow.quadrant == 'ne':
            self.selected_arrow.quadrant = 'nw'
        elif self.selected_arrow.quadrant == 'se':
            self.selected_arrow.quadrant = 'sw'
        # Update the arrow's position and orientation on the graphboard
        print(self.selected_arrow.quadrant)

    def move_arrow_quadrant_down(self):
        self.selected_arrow = self.graphboard.get_selected_items()[0]
        if self.selected_arrow.quadrant == 'ne':
            self.selected_arrow.quadrant = 'se'
        elif self.selected_arrow.quadrant == 'nw':
            self.selected_arrow.quadrant = 'sw'
        # Update the arrow's position and orientation on the graphboard
        print(self.selected_arrow.quadrant)

    def move_arrow_quadrant_right(self):
        self.selected_arrow = self.graphboard.get_selected_items()[0]
        if self.selected_arrow.quadrant == 'nw':
            self.selected_arrow.quadrant = 'ne'
        elif self.selected_arrow.quadrant == 'sw':
            self.selected_arrow.quadrant = 'se'
        # Update the arrow's position and orientation on the graphboard
        print(self.selected_arrow.quadrant)

    def rotateArrow(self, direction, items):
        for item in items:
            print(item.get_attributes())
            old_svg = f"images/arrows/{item.color}_{item.type}_{item.rotation}_{item.quadrant}.svg"
            print(old_svg)
            quadrants = ['ne', 'se', 'sw', 'nw']
            current_quadrant_index = quadrants.index(item.quadrant)
            if direction == "right":
                new_quadrant_index = (current_quadrant_index + 1) % 4
            else:  # direction == "left"
                new_quadrant_index = (current_quadrant_index - 1) % 4
            new_quadrant = quadrants[new_quadrant_index]
            new_svg = item.svg_file.replace(item.quadrant, new_quadrant)

            new_renderer = QSvgRenderer(new_svg)
            if new_renderer.isValid():
                item.setSharedRenderer(new_renderer)
                item.svg_file = new_svg
                item.update_locations()
                item.update_quadrant()
                pos = self.graphboard.get_quadrant_center(new_quadrant) - item.boundingRect().center()
                item.setPos(pos)
            else:
                print("Failed to load SVG file:", new_svg)

        self.graphboard.arrowMoved.emit()

    def mirrorArrow(self, items):
        for item in items:
            current_svg = item.svg_file

            if item.rotation == "l":
                new_svg = current_svg.replace("_l_", "_r_").replace("\\l\\", "\\r\\")
                item.rotation = "r"
            elif item.rotation == "r":
                new_svg = current_svg.replace("_r_", "_l_").replace("\\r\\", "\\l\\")
                item.rotation = "l"
            else:
                print("Unexpected svg_file:", current_svg)
                continue

            new_renderer = QSvgRenderer(new_svg)
            if new_renderer.isValid():
                item.setSharedRenderer(new_renderer)
                item.svg_file = new_svg
                item.update_locations()
                item.quadrant = item.quadrant.replace('.svg', '')
                item.update_quadrant()
                pos = self.graphboard.get_quadrant_center(item.quadrant) - item.boundingRect().center()
                item.setPos(pos)
            else:
                print("Failed to load SVG file:", new_svg)
        self.graphboard.arrowMoved.emit()

    def delete_arrow(self, items):
        for item in items:
            self.graphboard.scene().removeItem(item)
        self.graphboard.arrowMoved.emit()
        self.graphboard.attributesChanged.emit()

    def bringForward(self, items):
        for item in items:
            z = item.zValue()
            item.setZValue(z + 1)

    def swapColors(self, _):
        arrow_items = [item for item in self.graphboard_scene.items() if isinstance(item, Arrow)]
        if len(arrow_items) >= 1:
            for item in arrow_items:
                current_svg = item.svg_file
                base_name = os.path.basename(current_svg)
                color, type_, rotation, quadrant = base_name.split('_')[:4]
                if color == "red":
                    new_color = "blue"
                elif color == "blue":
                    new_color = "red"
                else:
                    print("Unexpected color:", color)
                    continue
                new_svg = current_svg.replace(color, new_color)
                new_renderer = QSvgRenderer(new_svg)
                if new_renderer.isValid():
                    item.setSharedRenderer(new_renderer)
                    item.svg_file = new_svg
                    item.color = new_color
                else:
                    print("Failed to load SVG file:", new_svg)
        else:
            print("Cannot swap colors with no arrows on the graphboard.")
            
        self.graphboard.arrowMoved.emit()

    def selectAll(self):
        for item in self.graphboard.items():
            #if item is an arrow
            if isinstance(item, Arrow):
                item.setSelected(True)
    
    def deselectAll(self):
        for item in self.graphboard.selectedItems():
            item.setSelected(False)

    def connect_to_graphboard(self, graphboard):
        self.graphboard = graphboard
        self.selected_items_len = len(graphboard.get_selected_items())
        print(f"selected_items_len: {self.selected_items_len}")
        


class Key_Press_Handler:
    def __init__(self, arrow_handler, graphboard=None):
        self.arrow_handler = arrow_handler
        print("Key_Press_Handler init")

    def handleKeyPressEvent(self, event):
        self.selected_items = self.graphboard.get_selected_items()
        if event.key() == Qt.Key_Delete:

            self.arrow_handler.delete_arrow(self.selected_items)

        print(self.selected_items) 
        if event.key() == Qt.Key_W:
            self.arrow_handler.move_arrow_quadrant_up()
            print("W")
        elif event.key() == Qt.Key_A:
            self.arrow_handler.move_arrow_quadrant_left()
        elif event.key() == Qt.Key_S:
            self.arrow_handler.move_arrow_quadrant_down()
        elif event.key() == Qt.Key_D:
            self.arrow_handler.move_arrow_quadrant_right()

    def connect_to_graphboard(self, graphboard):
        self.graphboard = graphboard
        print("Key_Press_Handler connected to graphboard")


class Json_Handler:
    def __init__(self, graphboard_scene):
        self.graphboard_scene = graphboard_scene

    def updatePositionInJson(self, red_position, blue_position):
        with open('pictographs.json', 'r') as file:
            data = json.load(file)
        current_attributes = []
        for item in self.graphboard_scene.items():
            if isinstance(item, Arrow):
                current_attributes.append(item.get_attributes())
        current_attributes = sorted(current_attributes, key=lambda x: x['color'])

        print("Current attributes:", current_attributes)

        for letter, combinations in data.items():
            for i, combination_set in enumerate(combinations):
                arrow_attributes = [d for d in combination_set if 'color' in d]
                combination_attributes = sorted(arrow_attributes, key=lambda x: x['color'])

                if combination_attributes == current_attributes:
                    new_optimal_red = {'x': red_position.x(), 'y': red_position.y()}
                    new_optimal_blue = {'x': blue_position.x(), 'y': blue_position.y()}
                    new_optimal_positions = {
                        "optimal_red_location": new_optimal_red,
                        "optimal_blue_location": new_optimal_blue
                    }

                    optimal_positions = next((d for d in combination_set if 'optimal_red_location' in d and 'optimal_blue_location' in d), None)
                    if optimal_positions is not None:
                        optimal_positions.update(new_optimal_positions)
                        print(f"Updated optimal positions for letter {letter}")
                    else:
                        combination_set.append(new_optimal_positions)
                        print(f"Added optimal positions for letter {letter}")
        with open('pictographs.json', 'w') as file:
            json.dump(data, file, indent=4)


class Exporter:
    def __init__(self, graphboard, graphboard_scene, staff_manager, grid):
        self.graphboard_scene = graphboard_scene
        self.graphboard = graphboard
        self.staff_manager = staff_manager
        self.grid = grid

    def exportAsPng(self):
        selectedItems = self.graphboard_scene.get_selected_items()
        image = QImage(self.graphboard.size(), QImage.Format_ARGB32)
        painter = QPainter(image)

        for item in selectedItems:
            item.setSelected(False)

        self.graphboard.render(painter)
        painter.end()
        image.save("export.png")

        for item in selectedItems:
            item.setSelected(True)

    def get_fill_color(self, svg_file):
        svg = etree.parse(svg_file)
        fill_color = None

        # Try to get fill color from style element
        style_element = svg.getroot().find('.//{http://www.w3.org/2000/svg}style')
        if style_element is not None:
            style_text = style_element.text
            color_match = re.search(r'fill:\s*(#[0-9a-fA-F]+)', style_text)
            if color_match:
                fill_color = color_match.group(1)

        # If fill color was not found in style element, try to get it from path or rect elements
        if fill_color is None:
            for element in svg.getroot().iterfind('.//{http://www.w3.org/2000/svg}*'):
                if 'fill' in element.attrib:
                    fill_color = element.attrib['fill']
                    break

        return fill_color

    def exportAsSvg(self):
        print("Exporting")
        svg = etree.Element('svg', nsmap={None: 'http://www.w3.org/2000/svg'})
        svg.set('width', '750')
        svg.set('height', '900')
        svg.set('viewBox', '0 0 750 900')

        # Create groups for staves, arrows, and the grid
        staves_group = etree.Element('g', id='staves')
        arrows_group = etree.Element('g', id='arrows')
        grid_group = etree.Element('g', id='grid')

        for item in self.graphboard_scene.items():
            if isinstance(item, Grid):
                grid_svg = etree.parse(item.svg_file)
                circle_elements = grid_svg.getroot().findall('.//{http://www.w3.org/2000/svg}circle')

                for circle_element in circle_elements:
                    # Adjust the cx and cy attributes to move the circle 25 pixels to the right and down
                    cx = float(circle_element.get('cx')) + 50
                    cy = float(circle_element.get('cy')) + 50
                    circle_element.set('cx', str(cx))
                    circle_element.set('cy', str(cy))

                    # Append the circle to the grid group
                    grid_group.append(circle_element)

                print("Finished exporting" + item.svg_file)

            elif isinstance(item, Arrow):
                arrow_svg = etree.parse(item.svg_file)
                path_elements = arrow_svg.getroot().findall('.//{http://www.w3.org/2000/svg}path')
                fill_color = self.get_fill_color(item.svg_file)
                transform = item.transform()

                for path_element in path_elements:
                    path_element.set('transform', f'matrix({transform.m11()}, {transform.m12()}, {transform.m21()}, {transform.m22()}, {item.x()}, {item.y()})')
                    if fill_color is not None:
                        path_element.set('fill', fill_color)

                    # Append the path to the arrows group
                    arrows_group.append(path_element)

                print("Finished exporting" + item.svg_file)

            elif isinstance(item, Staff):
                staff_svg = etree.parse(item.svg_file)
                rect_elements = staff_svg.getroot().findall('.//{http://www.w3.org/2000/svg}rect')
                fill_color = self.get_fill_color(item.svg_file)
                position = item.mapToScene(item.pos())  # Convert the position to scene coordinates
                parent_transform = item.parentItem().transform() if item.parentItem() else QTransform()
                transform = parent_transform * item.transform()

                # Scale the position to match the SVG's viewBox
                svg_width = 750
                svg_height = 900
                scene_rect = self.graphboard_scene.sceneRect()
                x_scale = svg_width / scene_rect.width()
                y_scale = svg_height / scene_rect.height()
                position.setX(position.x() * x_scale)
                position.setY(position.y() * y_scale)

                for rect_element in rect_elements:
                    rect_element_copy = deepcopy(rect_element)  # Create a deep copy of the element
                    rect_element_copy.set('transform', f'matrix({transform.m11()}, {transform.m12()}, {transform.m21()}, {transform.m22()}, {position.x()}, {position.y()})')
                    if fill_color is not None:
                        rect_element_copy.set('fill', fill_color)

                    # Append the rect to the staves group
                    staves_group.append(rect_element_copy)

                print("Finished exporting" + item.svg_file)

        # Add comments and append the groups to the SVG root element
        svg.append(etree.Comment(' STAVES '))
        svg.append(staves_group)
        svg.append(etree.Comment(' ARROWS '))
        svg.append(arrows_group)
        svg.append(etree.Comment(' GRID '))
        svg.append(grid_group)

        # Convert the SVG element to a string
        svg_string = etree.tostring(svg, pretty_print=True).decode()

        # Add blank lines between elements
        svg_string = svg_string.replace('>\n<', '>\n\n<')

        with open('output.svg', 'w') as file:
            file.write(svg_string)


class Svg_Handler:
    @staticmethod
    def parse_svg_file(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        for element in root.iter('{http://www.w3.org/2000/svg}path'):
            print('tag:', element.tag)
            print('attributes:', element.attrib)
            return element.attrib.get('d')

    @staticmethod
    def compare_svg_paths(file_path_1, file_path_2):
        tree_1 = ET.parse(file_path_1)
        root_1 = tree_1.getroot()

        tree_2 = ET.parse(file_path_2)
        root_2 = tree_2.getroot()

        path_data_1 = None
        for element in root_1.iter('{http://www.w3.org/2000/svg}path'):
            path_data_1 = element.attrib.get('d')
            break 

        path_data_2 = None
        for element in root_2.iter('{http://www.w3.org/2000/svg}path'):
            path_data_2 = element.attrib.get('d')
            break

        if path_data_1 == path_data_2:
            print('The SVG paths are identical.')
        else:
            print('The SVG paths are different.')

    @staticmethod
    def svg_path_to_qpainterpath(svg_path):
        qpainter_path = QPainterPath()
        for segment in svg_path:
            if isinstance(segment, Line):
                qpainter_path.lineTo(segment.end.real, segment.end.imag)
            elif isinstance(segment, CubicBezier):
                qpainter_path.cubicTo(segment.control1.real, segment.control1.imag,
                                    segment.control2.real, segment.control2.imag,
                                    segment.end.real, segment.end.imag)
            elif isinstance(segment, QuadraticBezier):
                qpainter_path.quadTo(segment.control.real, segment.control.imag,
                                    segment.end.real, segment.end.imag)
            elif isinstance(segment, Arc):
                # QPainterPath doesn't support arcs, so we need to approximate the arc with cubic beziers
                # This is a complex task and might require a separate function
                pass
            elif isinstance(segment, Close):
                qpainter_path.closeSubpath()
        return qpainter_path

    @staticmethod
    def get_main_element_id(svg_file):
        tree = ET.parse(svg_file)
        root = tree.getroot()

        # Get the first element with an 'id' attribute
        for element in root.iter():
            if 'id' in element.attrib:
                return element.attrib['id']
        return None
    
    @staticmethod
    def point_in_svg(point, svg_file):
        svg_path = Svg_Handler.parse_svg_file(svg_file)
        qpainter_path = Svg_Handler.svg_path_to_qpainterpath(svg_path)
        return qpainter_path.contains(point)
    
class Context_Menu_Handler:
    def __init__(self, scene):
        self.scene = scene

    def create_context_menu(self, event, selected_items):
        menu = QMenu()
        if len(selected_items) == 2:
            menu.addAction("Align horizontally", self.align_horizontally)
            menu.addAction("Align vertically", self.align_vertically)
        menu.addAction("Move", self.show_move_dialog)
        menu.addAction("Delete", self.handlers.delete_arrow)
        menu.exec_(event.screenPos())

    def show_move_dialog(self):
        dialog = QDialog()
        layout = QFormLayout()

        # Create the input fields
        self.up_input = QSpinBox()
        self.down_input = QSpinBox()
        self.left_input = QSpinBox()
        self.right_input = QSpinBox()

        # Add the input fields to the dialog
        layout.addRow("Up:", self.up_input)
        layout.addRow("Down:", self.down_input)
        layout.addRow("Left:", self.left_input)
        layout.addRow("Right:", self.right_input)

        # Create the buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # Connect the buttons to their slots
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        # Add the buttons to the dialog
        layout.addRow(buttons)

        dialog.setLayout(layout)

        # Show the dialog and wait for the user to click a button
        result = dialog.exec_()

        # If the user clicked the OK button, move the arrows
        if result == QDialog.Accepted:
            self.move_arrows()

    def move_arrows(self):
        items = self.scene.selectedItems()
        for item in items:
            item.moveBy(self.right_input.value() - self.left_input.value(), self.down_input.value() - self.up_input.value())

    def align_horizontally(self):
        items = self.scene().selectedItems()
        average_y = sum(item.y() for item in items) / len(items)
        for item in items:
            item.setY(average_y)

    def align_vertically(self):
        items = self.scene().selectedItems()
        average_x = sum(item.x() for item in items) / len(items)
        for item in items:
            item.setX(average_x)
