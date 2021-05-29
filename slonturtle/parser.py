from typing import Iterable, Union

from enum import Enum, auto
from dataclasses import dataclass


class Go(Enum):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()


@dataclass
class Paint:
    pass


@dataclass
class Times:
    count: int


@dataclass
class End:
    times_idx: int


Command = Union[Go, Paint, Times, End]


class ParseError(Exception):
    pass


def parse(lines: Iterable[str]) -> Iterable[Command]:
    loops = []

    for idx, line in enumerate(lines):
        command, *rest = line.strip().split()

        if command.isdigit() and len(rest) == 1 and rest[0] == 'times':
            yield Times(count=int(command))
            loops.append(idx)
            continue

        if rest:
            raise ParseError('the only command with arguments is times')

        if command == 'left':
            yield Go.LEFT
        elif command == 'right':
            yield Go.RIGHT
        elif command == 'up':
            yield Go.UP
        elif command == 'down':
            yield Go.DOWN
        elif command == 'paint':
            yield Paint()
        elif command == 'end':
            if not loops:
                raise ParseError('unpaired end found')

            loop_location = loops.pop()
            yield End(times_idx=loop_location)
        else:
            raise ParseError(f'unknown command {command!r}')
