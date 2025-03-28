from enum import Enum
from dataclasses import dataclass, replace


@dataclass
class RGBAColor:
    red: int
    green: int
    blue: int
    alpha: float = 1.0

    def __str__(self) -> str:
        return f'rgba({self.red}, {self.green}, {self.blue}, {self.alpha})'

    def shadow(self) -> 'RGBAColor':
        return replace(self, alpha=0.3)


class Color(Enum):
    BLUE = RGBAColor(red=80, green=116, blue=220)
