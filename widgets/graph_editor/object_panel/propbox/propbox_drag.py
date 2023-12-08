from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from objects.prop import Prop
from objects.arrow import StaticArrow
from utilities.TypeChecking.TypeChecking import *
from typing import TYPE_CHECKING
from settings.string_constants import (
    IN,
    OUT,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    NORTH,
    SOUTH,
    WEST,
    EAST,
    COLOR,
    MOTION_TYPE,
    STATIC,
    ROTATION_DIRECTION,
    ARROW_LOCATION,
    START_LOCATION,
    END_LOCATION,
    TURNS,
)
from widgets.graph_editor.object_panel.objectbox_drag import ObjectBoxDrag


if TYPE_CHECKING:
    from main import MainWindow
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.graph_editor.object_panel.propbox.propbox import PropBox


class PropBoxDrag(ObjectBoxDrag):
    def __init__(
        self, main_window: "MainWindow", pictograph: "Pictograph", propbox: "PropBox"
    ) -> None:
        super().__init__(main_window, pictograph, propbox)
        self.attributes: PropAttributesDicts = {}
        self.propbox = propbox
        self.objectbox = propbox
        self.static_arrow = None

    def match_target_prop(self, target_prop: "Prop") -> None:
        self.target_prop = target_prop
        self.static_arrow = target_prop.static_arrow
        drag_angle = self._get_prop_drag_rotation_angle(target_prop)
        super().match_target_object(target_prop, drag_angle)
        self.set_attributes(target_prop)

    def set_attributes(self, target_prop: "Prop") -> None:
        self.color: Colors = target_prop.color
        self.prop_type: PropTypes = target_prop.prop_type
        self.prop_location: Locations = target_prop.prop_location
        self.layer: Layers = target_prop.layer
        self.orientation: Orientations = target_prop.orientation

        self.ghost_prop = self.pictograph.ghost_props[self.color]
        self.ghost_prop.target_prop = target_prop

    def place_prop_on_pictograph(self) -> None:
        self.placed_prop = Prop(self.pictograph, self.ghost_prop.get_attributes())

        self.placed_prop.arrow = self.ghost_prop.arrow
        self.placed_prop.arrow.arrow_location = self.prop_location
        self.placed_prop.arrow.motion.start_location = self.prop_location
        self.placed_prop.arrow.motion.end_location = self.prop_location

        self.pictograph.add_motion(
            self.placed_prop.arrow,
            self.placed_prop,
            STATIC,
            self.orientation,
            self.layer,
        )
        self.placed_prop.motion.arrow_location = self.prop_location
        self.placed_prop.motion.start_location = self.prop_location
        self.placed_prop.motion.end_location = self.prop_location

        self.ghost_prop.arrow.prop = self.placed_prop
        self.pictograph.addItem(self.placed_prop)
        self.pictograph.props.append(self.placed_prop)

        self.pictograph.removeItem(self.ghost_prop)
        self.pictograph.props.remove(self.ghost_prop)
        self.pictograph.update_pictograph()
        self.pictograph.clearSelection()

        self.placed_prop.ghost_prop = self.ghost_prop
        self.placed_prop.update_appearance()
        self.placed_prop.show()
        self.placed_prop.setSelected(True)

    ### UPDATERS ###

    def _update_prop_preview_for_new_location(self, new_location: Locations) -> None:
        self.prop_location = new_location

        self._update_ghost_prop_for_new_location(new_location)

        if not self.static_arrow:
            self._create_static_arrow()
        self._update_static_arrow()

        self.current_rotation_angle = self._get_prop_drag_rotation_angle(self)
        rotated_pixmap = self.create_pixmap_with_rotation(self.current_rotation_angle)

        if self.current_rotation_angle in [90, 270]:
            new_size = QSize(rotated_pixmap.width(), rotated_pixmap.height())
        else:
            new_size = rotated_pixmap.size()

        self.setFixedSize(new_size)
        self.preview.setFixedSize(new_size)
        self.preview.setPixmap(rotated_pixmap)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if self.ghost_prop not in self.pictograph.props:
            self.pictograph.props.append(self.ghost_prop)
        if self.ghost_prop not in self.pictograph.items():
            self.pictograph.addItem(self.ghost_prop)

        # remove the old motion from the pcitograph before adding the new one
        for motion in self.pictograph.motions[:]:
            if motion.color == self.color:
                self.pictograph.motions.remove(motion)

        self.pictograph.add_motion(
            self.ghost_prop.arrow, self.ghost_prop, STATIC, IN, 1
        )

        self.pictograph.update_pictograph()
        self.move_to_cursor(self.propbox.view.mapFromGlobal(self.pos()))

    def _update_ghost_prop_for_new_location(self, new_location) -> None:
        self.ghost_prop.prop_type = self.prop_type
        self.ghost_prop.color = self.color
        self.ghost_prop.prop_location = new_location
        self.ghost_prop.orientation = self.orientation
        self.ghost_prop.layer = self.layer

        self.ghost_prop.motion.arrow_location = self.prop_location
        self.ghost_prop.motion.start_location = self.prop_location
        self.ghost_prop.motion.end_location = self.prop_location

        self.ghost_prop.arrow = self.static_arrow
        self.ghost_prop.arrow.arrow_location = self.prop_location
        self.ghost_prop.arrow.motion.start_location = self.prop_location
        self.ghost_prop.arrow.motion.end_location = self.prop_location

        ghost_svg = self.ghost_prop.get_svg_file(self.prop_type)
        self.ghost_prop.update_svg(ghost_svg)
        self.ghost_prop.update_color()
        self.ghost_prop.update_axis(new_location)
        self.ghost_prop.update_rotation()

    ### EVENT HANDLERS ###

    def handle_mouse_move(self, event_pos: QPoint) -> None:
        if self.preview:
            self.move_to_cursor(event_pos)
            if self.is_over_pictograph(event_pos):
                if not self.has_entered_pictograph_once:
                    self.has_entered_pictograph_once = True
                    self.remove_same_color_objects()
                    self._create_static_arrow()
                    self.pictograph.add_motion(
                        self.ghost_prop.arrow,
                        self.ghost_prop,
                        STATIC,
                        self.orientation,
                        self.layer,
                    )

                pos_in_main_window = self.propbox.view.mapToGlobal(event_pos)
                view_pos_in_pictograph = self.pictograph.view.mapFromGlobal(
                    pos_in_main_window
                )
                scene_pos = self.pictograph.view.mapToScene(view_pos_in_pictograph)
                new_location = self.pictograph.get_closest_handpoint(scene_pos)

                if self.previous_drag_location != new_location and new_location:
                    self.previous_drag_location = new_location
                    self.ghost_prop.arrow.arrow_location = new_location
                    self.ghost_prop.arrow.motion.start_location = new_location
                    self.ghost_prop.arrow.motion.end_location = new_location
                    self.ghost_prop.motion.arrow_location = new_location
                    self.ghost_prop.motion.start_location = new_location
                    self.ghost_prop.motion.end_location = new_location
                    self._update_prop_preview_for_new_location(new_location)
                    self.ghost_prop.update_attributes(self.attributes)
                    self.pictograph.update_pictograph()

    def handle_mouse_release(self) -> None:
        if self.has_entered_pictograph_once:
            self.place_prop_on_pictograph()
        self.deleteLater()
        self.pictograph.update_pictograph()
        self.propbox.drag = None
        self.ghost_prop.arrow = None
        self.reset_drag_state()
        self.previous_drag_location = None

    ### HELPERS ###

    def is_over_pictograph(self, event_pos: QPoint) -> bool:
        pos_in_main_window = self.propbox.view.mapToGlobal(event_pos)
        local_pos_in_pictograph = self.pictograph.view.mapFromGlobal(pos_in_main_window)
        return self.pictograph.view.rect().contains(local_pos_in_pictograph)

    def create_pixmap_with_rotation(self, angle: RotationAngles) -> QPixmap:
        # Generate a new pixmap based on target prop and apply the rotation
        new_svg_data = self.target_prop.set_svg_color(self.color)
        renderer = QSvgRenderer()
        renderer.load(new_svg_data)

        scaled_size = renderer.defaultSize() * self.pictograph.view.view_scale
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)

        renderer.render(painter)
        painter.end()
        rotate_transform = QTransform().rotate(angle)
        rotated_pixmap = pixmap.transformed(rotate_transform)

        return rotated_pixmap

    def _get_prop_drag_rotation_angle(
        self, staff: Prop | ObjectBoxDrag
    ) -> RotationAngles:
        """
        Get the rotation angle for the given staff specifically for use with the PropBoxDrag.

        Args:
            staff (Union[Prop, ObjectBoxDrag]): The staff for which to retrieve the rotation angle.

        Returns:
            RotationAngles: The rotation angle for the staff.

        """
        angle_map: Dict[
            Tuple[Layers, Orientations], Dict[Locations, RotationAngles]
        ] = {
            (1, IN): {NORTH: 90, SOUTH: 270, WEST: 0, EAST: 180},
            (1, OUT): {NORTH: 270, SOUTH: 90, WEST: 180, EAST: 0},
            (2, CLOCKWISE): {NORTH: 0, SOUTH: 180, WEST: 270, EAST: 90},
            (2, COUNTER_CLOCKWISE): {NORTH: 180, SOUTH: 0, WEST: 90, EAST: 270},
        }
        key = (staff.layer, staff.orientation)
        return angle_map.get(key, {}).get(staff.prop_location, 0)

    def _create_static_arrow(self) -> None:
        static_arrow_dict = {
            COLOR: self.color,
            MOTION_TYPE: STATIC,
            ROTATION_DIRECTION: "None",
            ARROW_LOCATION: self.prop_location,
            START_LOCATION: self.prop_location,
            END_LOCATION: self.prop_location,
            TURNS: 0,
        }

        self.static_arrow = StaticArrow(self.pictograph, static_arrow_dict)
        for arrow in self.pictograph.arrows[:]:
            if arrow.color == self.color:
                self.pictograph.removeItem(arrow)
                self.pictograph.arrows.remove(arrow)
        self.pictograph.addItem(self.static_arrow)
        self.pictograph.arrows.append(self.static_arrow)
        self.static_arrow.prop = self.ghost_prop
        self.static_arrow.prop.arrow = self.static_arrow

        if self.static_arrow not in self.pictograph.items():
            self.pictograph.addItem(self.static_arrow)

    def _update_static_arrow(self) -> None:
        self.static_arrow.color = self.color
        self.static_arrow.arrow_location = self.prop_location
        self.static_arrow.motion.start_location = self.prop_location
        self.static_arrow.motion.end_location = self.prop_location
        self.static_arrow.prop = self.ghost_prop
        self.static_arrow.prop.arrow = self.static_arrow
        self.static_arrow.update_appearance()
        self.pictograph.update_pictograph()