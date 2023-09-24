from enum import Enum
from components import fs


class ScaleModes(Enum):
    OVERRIDE = 0
    MULTIPLY = 1
    INHERIT = 2

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


settings = fs.load("settings.json")["window"]["scale"]
global_factor = settings["factor"]
default_mode = ScaleModes(settings["default_mode"])


class Scale:
    def __init__(self, mode, factor=1.0):
        self.mode = ScaleModes(mode) if ScaleModes.has_value(mode) else default_mode

        match self.mode:
            case ScaleModes.OVERRIDE:
                self.factor = factor

            case ScaleModes.MULTIPLY:
                self.factor = factor * global_factor

            case ScaleModes.INHERIT:
                self.factor = global_factor

    def apply(self, value):
        return round(self.factor * value)
