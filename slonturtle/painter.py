from typing import Set
from dataclasses import dataclass

from PIL import Image  # type: ignore

from slonturtle.executer import Coord


@dataclass
class Bounds:
    width: int
    height: int
    shift_x: int
    shift_y: int


def determine_bounds(field: Set[Coord]) -> Bounds:
    min_x, max_x, min_y, max_y = 0, 0, 0, 0

    for x, y in field:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    return Bounds(
        width=max_x - min_x + 1,
        height=max_y - min_y + 1,
        shift_x=-min_x,
        shift_y=-min_y,
    )


def draw(field: Set[Coord]) -> Image.Image:
    bounds = determine_bounds(field)

    result = Image.new('1', (bounds.width, bounds.height), color=1)

    for x, y in field:
        result.putpixel((x + bounds.shift_x, y + bounds.shift_y), 0)

    return result
