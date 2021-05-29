import sys
from typing import Optional

from slonturtle.parser import ParseError, parse
from slonturtle.executer import execute
from slonturtle.painter import draw


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print(
            f'Usage: {sys.argv[0]} <program> [<output image>]',
            file=sys.stderr
        )
        return 1

    program_filename = sys.argv[1]

    output_filename: Optional[str]
    if len(sys.argv) == 3:
        output_filename = sys.argv[2]
    else:
        output_filename = None

    with open(program_filename) as program_file:
        try:
            parsed_program = list(parse(program_file))
        except ParseError as err:
            print(f'Failed to parse program: {err}', file=sys.stderr)
            return 2

    field = execute(parsed_program)
    print(f"There are {len(field)} painted cells")

    if output_filename is not None:
        image = draw(field)
        image.save(output_filename)

    return 0


if __name__ == '__main__':
    sys.exit(main())
