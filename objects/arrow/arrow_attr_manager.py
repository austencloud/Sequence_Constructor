from typing import Union

from constants import *

from utilities.TypeChecking.TypeChecking import (
    Colors,
    Locations,
    MotionTypes,
    Turns,
    TYPE_CHECKING,
    Dict,
)


if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowAttrManager:
    def __init__(self, arrow: "Arrow") -> None:
        self.arrow = arrow

    def update_attributes(
        self, arrow_dict: Dict[str, Union[Colors, Locations, MotionTypes, Turns]]
    ) -> None:
        arrow_attributes = [COLOR, LOC, MOTION_TYPE, TURNS]
        for attr in arrow_attributes:
            value = arrow_dict.get(attr)
            if value is not None:
                setattr(self.arrow, attr, value)
                
    def clear_attributes(self) -> None:
        arrow_attributes = [COLOR, LOC, MOTION_TYPE, TURNS]
        for attr in arrow_attributes:
            setattr(self.arrow, attr, None)
