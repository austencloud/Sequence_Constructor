from typing import Union, TYPE_CHECKING

from Enums.Enums import Turns
from data.constants import *

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow
from Enums.MotionAttributes import (
    Location,
    MotionType,
)


class ArrowAttrHandler:
    def __init__(self, arrow: "Arrow") -> None:
        self.arrow = arrow
        self.arrow.color = self.arrow.arrow_dict[COLOR]
        self.arrow.turns = self.arrow.arrow_dict[TURNS]

    def update_attributes(
        self, arrow_dict: dict[str, Union[str, Location, MotionType, Turns]]
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

    def get_arrow_attributes(self) -> dict[str, Union[str, Location, MotionType]]:
        arrow_attributes = [COLOR, LOC]
        return {attr: getattr(self.arrow, attr) for attr in arrow_attributes}
