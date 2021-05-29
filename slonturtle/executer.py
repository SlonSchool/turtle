from typing import NamedTuple, Sequence, List, Set

from slonturtle.parser import Go, Paint, Times, End, Command


class Coord(NamedTuple):
    x: int
    y: int


def execute(program: Sequence[Command]) -> Set[Coord]:
    field = set()
    current_command_idx = 0
    loop_depth = 0
    iterations_left: List[int] = []
    current_step = 0

    x = 0
    y = 0

    while current_command_idx < len(program):
        current_step += 1
        if current_step > 1000:
            break

        command = program[current_command_idx]

        if isinstance(command, Go):
            if command == Go.LEFT:
                x -= 1
            elif command == Go.RIGHT:
                x += 1
            elif command == Go.UP:
                y -= 1
            elif command == Go.DOWN:
                y += 1
            else:
                raise RuntimeError(f'unexpected Go command: {command}')

        elif isinstance(command, Paint):
            field.add(Coord(x, y))

        elif isinstance(command, Times):
            # Мы в первый раз попали на начало этого цикла
            if loop_depth == len(iterations_left):
                iterations_left.append(command.count)
                loop_depth += 1

        elif isinstance(command, End):
            iterations_left[-1] -= 1
            if iterations_left[-1] == 0:
                iterations_left.pop()
                loop_depth -= 1
            else:
                current_command_idx = command.times_idx

        else:
            raise RuntimeError(f'unknown command {command}')

        current_command_idx += 1

    return field
