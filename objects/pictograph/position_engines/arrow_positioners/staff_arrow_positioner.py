from typing import TYPE_CHECKING, Callable, Literal
from PyQt6.QtCore import QPointF
from Enums import (
    AntiradialOrientation,
    Color,
    Direction,
    RadialOrientation,
)
from constants.constants import (
    ANTI,
    BLUE,
    CLOCK,
    COUNTER,
    DOWN,
    EAST,
    IN,
    LEFT,
    NORTH,
    NORTHEAST,
    NORTHWEST,
    OUT,
    PRO,
    RED,
    RIGHT,
    SOUTH,
    SOUTHEAST,
    SOUTHWEST,
    UP,
    WEST, DISTANCE
)
from objects.motion import Motion

from objects.prop.prop import Prop

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from objects.pictograph.position_engines.arrow_positioners.arrow_positioner import (
        ArrowPositioner,
    )



class StaffArrowPositioner:
    def __init__(
        self, pictograph: "Pictograph", arrow_positioner: "ArrowPositioner"
    ) -> None:
        self.pictograph = pictograph
        self.arrow_positioner = arrow_positioner

    def _adjust_arrows_for_staffs(self, current_letter) -> None:
        red_prop = self.pictograph.motions[RED].prop
        blue_prop = self.pictograph.motions[BLUE].prop

        # Mapping the letters to their respective methods
        letter_methods = {
            "K": self._adjust_arrows_for_letter_K,
            "L": self._adjust_arrows_for_letter_L,
            "H": self._adjust_arrows_for_letter_H,
            "I": self._adjust_arrows_for_letter_I,
            "Q": self._adjust_arrows_for_letter_Q,
            "R": self._adjust_arrows_for_letter_R,
            "T": self._adjust_arrows_for_letter_T,
            "V": self._adjust_arrows_for_letter_V,
        }

        # Call the corresponding method
        adjust_method = letter_methods.get(current_letter)
        if adjust_method:
            adjust_method(red_prop, blue_prop)

    # Methods for each letter with specific logic
    def _adjust_arrows_for_letter_K(self, red_prop, blue_prop) -> None:
        if self._are_both_props_radial(red_prop, blue_prop):
            self._apply_adjustment_to_all_arrows(55)

        elif self._is_at_least_one_prop_antiradial(red_prop, blue_prop):
            self._apply_adjustment_to_all_arrows(90)

    def _adjust_arrows_for_letter_L(self, red_prop, blue_prop) -> None:
        self._apply_specific_arrow_adjustment(ANTI, OUT, 55)

        if self._is_at_least_one_prop_antiradial(red_prop, blue_prop):
            self._apply_adjustment_to_arrows_by_type(ANTI, 90)

    def _adjust_arrows_for_letter_H(self, red_prop, blue_prop) -> None:
        if self._is_at_least_one_prop_antiradial(red_prop, blue_prop):
            for arrow in self.pictograph.arrows.values():
                adjustment = self.arrow_positioner._calculate_GH_adjustment(arrow)
                adjusted_x = (
                    adjustment.x() - 30 if adjustment.x() < 0 else adjustment.x() + 30
                )
                adjusted_y = (
                    adjustment.y() - 30 if adjustment.y() < 0 else adjustment.y() + 30
                )
                adjusted_adjustment = QPointF(adjusted_x, adjusted_y)
                self.arrow_positioner._apply_adjustment(arrow, adjusted_adjustment)

    def _adjust_arrows_for_letter_I(self, red_prop, blue_prop) -> None:
        if self._is_at_least_one_prop_antiradial(red_prop, blue_prop):
            for arrow in self.pictograph.arrows.values():
                adjustment = self.arrow_positioner._calculate_I_adjustment(arrow)
                adjusted_x = (
                    adjustment.x() - 30 if adjustment.x() < 0 else adjustment.x() + 30
                )
                adjusted_y = (
                    adjustment.y() - 30 if adjustment.y() < 0 else adjustment.y() + 30
                )
                adjusted_adjustment = QPointF(adjusted_x, adjusted_y)
                self.arrow_positioner._apply_adjustment(arrow, adjusted_adjustment)

    def _adjust_arrows_for_letter_Q(self, red_prop, blue_prop) -> None:
        if self._is_at_least_one_prop_antiradial(red_prop, blue_prop):
            for arrow in self.pictograph.arrows.values():
                adjustment = self.arrow_positioner._calculate_Q_adjustment(arrow)
                adjusted_x = (
                    adjustment.x() - 60 if adjustment.x() < 0 else adjustment.x() + 60
                )
                adjusted_y = (
                    adjustment.y() - 60 if adjustment.y() < 0 else adjustment.y() + 60
                )
                adjusted_adjustment = QPointF(adjusted_x, adjusted_y)
                self.arrow_positioner._apply_adjustment(arrow, adjusted_adjustment)

    def _adjust_arrows_for_letter_R(self, red_prop, blue_prop) -> None:
        if self._is_at_least_one_prop_antiradial(red_prop, blue_prop):
            for arrow in self.pictograph.arrows.values():
                adjustment = self.arrow_positioner._calculate_R_adjustment(arrow)
                adjusted_x = (
                    adjustment.x() - 60 if adjustment.x() < 0 else adjustment.x() + 60
                )
                adjusted_y = (
                    adjustment.y() - 60 if adjustment.y() < 0 else adjustment.y() + 60
                )
                adjusted_adjustment = QPointF(adjusted_x, adjusted_y)
                self.arrow_positioner._apply_adjustment(arrow, adjusted_adjustment)

    def _adjust_arrows_for_letter_T(self, red_prop, blue_prop) -> None:
        if self._is_at_least_one_prop_antiradial(red_prop, blue_prop):
            leading_color: Color = self.determine_leading_motion_for_T(
                self.pictograph.motions[RED].start_location,
                self.pictograph.motions[RED].end_location,
                self.pictograph.motions[BLUE].start_location,
                self.pictograph.motions[BLUE].end_location,
            )
            leader = self.pictograph.motions[leading_color]
            if leading_color == RED:
                follower = self.pictograph.motions[BLUE]
            else:
                follower = self.pictograph.motions[RED]
                
            for arrow in self.pictograph.arrows.values():
                if arrow.motion.prop.is_antiradial():
                    default_pos = self.arrow_positioner._get_default_position(arrow)
                    adjustment = self.arrow_positioner.calculate_adjustment(
                        arrow.location, DISTANCE + -45
                    )
                    new_pos = default_pos + adjustment - arrow.boundingRect().center()
                    arrow.setPos(new_pos)

            if leader.prop.is_antiradial() and follower.prop.is_radial():
                adjustment = self.arrow_positioner.calculate_adjustment(
                    leader.arrow.location, 30
                )
                direction = self.get_anti_leader_adjustment_direction(leader)
                if direction == UP:
                    adjustment += QPointF(0, -40)
                elif direction == DOWN:
                    adjustment += QPointF(0, 40)
                elif direction == LEFT:
                    adjustment += QPointF(-40, 0)
                elif direction == RIGHT:
                    adjustment += QPointF(40, 0)
                self.arrow_positioner._apply_adjustment(leader.arrow, adjustment)

            elif leader.prop.is_radial() and follower.prop.is_antiradial():
                adjustment = self.arrow_positioner.calculate_adjustment(
                    follower.arrow.location, 40
                )
                direction = self.get_anti_leader_adjustment_direction(leader)
                if direction == UP:
                    if leader.end_location == WEST:
                        adjustment += QPointF(-45, -20)
                    elif leader.end_location == EAST:
                        adjustment += QPointF(45, -20)
                elif direction == DOWN:
                    if leader.end_location == WEST:
                        adjustment += QPointF(-45, 20)
                    elif leader.end_location == EAST:
                        adjustment += QPointF(45, 20)
                elif direction == LEFT:
                    if leader.end_location == NORTH:
                        adjustment += QPointF(-20, -45)
                    elif leader.end_location == SOUTH:
                        adjustment += QPointF(-20, 45)
                elif direction == RIGHT:
                    if leader.end_location == NORTH:
                        adjustment += QPointF(20, -45)
                    elif leader.end_location == SOUTH:
                        adjustment += QPointF(20, 45)
                self.arrow_positioner._apply_adjustment(leader.arrow, adjustment)

    def determine_leading_motion_for_T(
        self, red_start, red_end, blue_start, blue_end
    ) -> Literal["red", "blue"] | None:
        """Determines which motion is leading in the rotation sequence."""
        if red_start == blue_end:
            return "red"
        elif blue_start == red_end:
            return "blue"
        return None

    def _adjust_arrows_for_letter_V(self, red_prop, blue_prop) -> None:
        if self._is_at_least_one_prop_antiradial(red_prop, blue_prop):
            anti_motion = (
                self.pictograph.motions[RED]
                if self.pictograph.motions[RED].motion_type == ANTI
                else self.pictograph.motions[BLUE]
            )
            pro_motion = (
                self.pictograph.motions[RED]
                if self.pictograph.motions[RED].motion_type == PRO
                else self.pictograph.motions[BLUE]
            )

            if anti_motion.prop.is_antiradial() and pro_motion.prop.is_radial():
                adjustment = self.arrow_positioner.calculate_adjustment(
                    anti_motion.arrow.location, 30
                )
                direction = self.get_anti_leader_adjustment_direction(anti_motion)
                if direction == UP:
                    adjustment += QPointF(0, -40)
                elif direction == DOWN:
                    adjustment += QPointF(0, 40)
                elif direction == LEFT:
                    adjustment += QPointF(-40, 0)
                elif direction == RIGHT:
                    adjustment += QPointF(40, 0)
                self.arrow_positioner._apply_adjustment(anti_motion.arrow, adjustment)

            elif anti_motion.prop.is_radial() and pro_motion.prop.is_antiradial():
                adjustment = self.arrow_positioner.calculate_adjustment(
                    pro_motion.arrow.location, 40
                )
                direction = self.get_anti_leader_adjustment_direction(anti_motion)
                if direction == UP:
                    if anti_motion.end_location == WEST:
                        adjustment += QPointF(-45, -20)
                    elif anti_motion.end_location == EAST:
                        adjustment += QPointF(45, -20)
                elif direction == DOWN:
                    if anti_motion.end_location == WEST:
                        adjustment += QPointF(-45, 20)
                    elif anti_motion.end_location == EAST:
                        adjustment += QPointF(45, 20)
                elif direction == LEFT:
                    if anti_motion.end_location == NORTH:
                        adjustment += QPointF(-20, -45)
                    elif anti_motion.end_location == SOUTH:
                        adjustment += QPointF(-20, -45)
                elif direction == RIGHT:
                    if anti_motion.end_location == NORTH:
                        adjustment += QPointF(20, -45)
                    elif anti_motion.end_location == SOUTH:
                        adjustment += QPointF(20, 45)
                self.arrow_positioner._apply_adjustment(anti_motion.arrow, adjustment)

    def get_anti_leader_adjustment_direction(self, leader: "Motion") -> str:
        arrow_location = leader.arrow.location
        prop_location = leader.prop.location

        antiradial_mapping = {
            (NORTHEAST, EAST): DOWN,
            (NORTHEAST, NORTH): LEFT,
            (SOUTHEAST, SOUTH): LEFT,
            (SOUTHEAST, EAST): UP,
            (SOUTHWEST, WEST): UP,
            (SOUTHWEST, SOUTH): RIGHT,
            (NORTHWEST, NORTH): RIGHT,
            (NORTHWEST, WEST): DOWN,
        }

        radial_mapping = {
            (NORTHEAST, EAST): DOWN,
            (NORTHEAST, NORTH): LEFT,
            (SOUTHEAST, SOUTH): LEFT,
            (SOUTHEAST, EAST): UP,
            (SOUTHWEST, WEST): UP,
            (SOUTHWEST, SOUTH): RIGHT,
            (NORTHWEST, NORTH): RIGHT,
            (NORTHWEST, WEST): DOWN,
        }

        if leader.prop.is_antiradial():
            return antiradial_mapping.get((arrow_location, prop_location))
        else:
            return radial_mapping.get((arrow_location, prop_location))

    # Helper functions
    def _are_both_props_radial(self, red_prop: Prop, blue_prop: Prop) -> bool:
        return (
            red_prop.orientation in RadialOrientation
            and blue_prop.orientation in RadialOrientation
        )

    def _is_at_least_one_prop_antiradial(self, red_prop: Prop, blue_prop: Prop) -> bool:
        return (
            red_prop.orientation in AntiradialOrientation
            or blue_prop.orientation in AntiradialOrientation
        )

    def _apply_adjustment_to_all_arrows(self, adjustment_value: int) -> None:
        for arrow in self.pictograph.arrows.values():
            if self.arrow_positioner._is_arrow_movable(arrow):
                adjustment = self.arrow_positioner._calculate_adjustment_tuple(
                    arrow.location, adjustment_value
                )
                self.arrow_positioner._apply_adjustment(arrow, adjustment)

    def _apply_specific_arrow_adjustment(
        self, motion_type: str, orientation: str, adjustment_value: int
    ) -> None:
        for arrow in self.pictograph.arrows.values():
            if (
                arrow.motion_type == motion_type
                and arrow.motion.prop.orientation == orientation
            ):
                adjustment = self.arrow_positioner._calculate_adjustment_tuple(
                    arrow.location, adjustment_value
                )
                self.arrow_positioner._apply_adjustment(arrow, adjustment)

    def _apply_adjustment_to_arrows_by_type(
        self, motion_type: str, adjustment_value: int
    ) -> None:
        for arrow in self.pictograph.arrows.values():
            if arrow.motion_type == motion_type:
                adjustment = self.arrow_positioner._calculate_adjustment_tuple(
                    arrow.location, adjustment_value
                )
                self.arrow_positioner._apply_adjustment(arrow, adjustment)
