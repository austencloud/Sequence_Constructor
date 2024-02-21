from typing import TYPE_CHECKING
from Enums.letters import LetterConditions
from constants import CLOCK, COUNTER, IN, OUT
from objects.arrow.arrow import Arrow

if TYPE_CHECKING:
    from ..special_arrow_positioner import SpecialArrowPositioner


class AttrKeyGenerator:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner

    def get_key(self, arrow: "Arrow") -> str:
        if arrow.pictograph.check.starts_from_mixed_orientation():
            if self.positioner.pictograph.letter in ["S", "T"]:
                return f"{arrow.color.value}_{arrow.motion.lead_state}"
            elif arrow.pictograph.check.starts_from_mixed_orientation():
                if arrow.pictograph.check.has_hybrid_motions():
                    if arrow.motion.start_ori in [IN, OUT]:
                        return f"{arrow.motion.motion_type}_from_layer1"
                    elif arrow.motion.start_ori in [CLOCK, COUNTER]:
                        return f"{arrow.motion.motion_type}_from_layer2"
                else:
                    return arrow.motion.color.value
            elif (
                self.positioner.pictograph.letter
                in self.positioner.pictograph.letter.get_letters_by_condition(
                    LetterConditions.NON_HYBRID
                )
            ):
                return arrow.color.value
            else:
                return arrow.motion.motion_type

        elif arrow.pictograph.check.starts_from_standard_orientation():
            if arrow.pictograph.letter in ["S", "T"]:
                return f"{arrow.color.value}_{arrow.motion.lead_state}"
            elif arrow.pictograph.check.has_hybrid_motions():
                return arrow.motion.motion_type
            else:
                return arrow.color.value

    def _determine_layer(self, arrow: "Arrow") -> int:
        return 1 if arrow.motion.start_ori in [IN, OUT] else 2
