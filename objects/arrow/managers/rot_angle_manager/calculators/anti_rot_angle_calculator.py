from constants import *
from .base_rot_angle_calculator import BaseRotAngleCalculator


class AntiRotAngleCalculator(BaseRotAngleCalculator):
    def _calculate_angle_impl(self):
        if self.arrow.motion.start_ori in [IN, OUT]:
            direction_map = {
                CLOCKWISE: {
                    NORTHEAST: 270,
                    SOUTHEAST: 180,
                    SOUTHWEST: 90,
                    NORTHWEST: 0,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 90,
                    SOUTHWEST: 180,
                    NORTHWEST: 270,
                },
            }
        elif self.arrow.motion.start_ori in [CLOCK, COUNTER]:

            if self.arrow.turns in [0.5, 1.5, 2.5]:
                direction_map = {
                    CLOCKWISE: {
                        NORTHEAST: 270, 
                        SOUTHEAST: 180,
                        SOUTHWEST: 90,
                        NORTHWEST: 360,  
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: 360, 
                        SOUTHEAST: 90,
                        SOUTHWEST: 180,
                        NORTHWEST: 270,
                    },
                }
            else:
                direction_map = {
                    CLOCKWISE: {
                        NORTHEAST: 270,
                        SOUTHEAST: 180,
                        SOUTHWEST: 90,
                        NORTHWEST: 0,
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: 0,
                        SOUTHEAST: 90,
                        SOUTHWEST: 180,
                        NORTHWEST: 270,
                    },
                }

        prop_rot_dir = self.arrow.motion.prop_rot_dir
        loc = self.arrow.loc
        return direction_map.get(prop_rot_dir, {}).get(loc, 0)

