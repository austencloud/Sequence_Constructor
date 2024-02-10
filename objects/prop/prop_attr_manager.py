from typing import TYPE_CHECKING, Union
from Enums import PropAttribute

from constants import *
from utilities.TypeChecking.MotionAttributes import (
    Colors,
    Locations,
    Orientations,
    Turns,
    MotionTypes,
)
from utilities.TypeChecking.TypeChecking import Axes
from utilities.TypeChecking.prop_types import PropTypes


if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropAttrManager:
    def __init__(self, prop: "Prop") -> None:
        self.prop = prop
        self.update_attributes(self.prop.prop_dict)
        self.prop.set_z_value_based_on_color()

    def update_attributes(
        self, prop_dict: dict[str, Union[Colors, Locations, MotionTypes, Turns]]
    ) -> None:
        prop_attributes = [COLOR, LOC, LAYER, ORI, MOTION, PROP_TYPE]
        for attr in prop_attributes:
            value = prop_dict.get(attr)
            if value is not None:
                setattr(self.prop, attr, value)

    def clear_attributes(self) -> None:
        prop_attributes = [COLOR, LOC, LAYER, ORI, MOTION, PROP_TYPE]
        for attr in prop_attributes:
            setattr(self.prop, attr, None)

    def get_axis_from_ori(self) -> None:
        if self.prop.check.is_radial():
            axis: Axes = VERTICAL if self.prop.loc in [NORTH, SOUTH] else HORIZONTAL
        elif self.prop.check.is_nonradial():
            axis: Axes = HORIZONTAL if self.prop.loc in [NORTH, SOUTH] else VERTICAL
        else:
            axis: Axes = None
        return axis

    def swap_ori(self) -> None:
        ori_map = {
            IN: OUT,
            OUT: IN,
            CLOCK: COUNTER,
            COUNTER: CLOCK,
        }
        self.ori = ori_map[self.ori]

    def get_attributes(self) -> dict[str, Union[Colors, Locations, Orientations]]:
        prop_attributes = [attr.value for attr in PropAttribute]
        return {attr: getattr(self.prop, attr) for attr in prop_attributes}
