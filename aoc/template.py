#!/usr/bin/env python3

import re
import click

import numpy as np

from pathlib import Path


@click.command()
@click.option("-v", "--verbose", count=True)
@click.option("-t", "--test", is_flag=True)
def main(verbose, test) -> int:
    proj = Path(__file__).absolute().parent.parent
    day = re.search("\d+", Path(__file__).name)
    day = day.group(0) if day else ""
    day = day if day else ""
    if test:
        in_file = proj / f"dat/day_{day}_test.txt"
    else:
        in_file = proj / f"dat/day_{day}.txt"
    if verbose:
        print(f"Advent of Code Day {day}")

    with in_file.open('r') as fil:
        lines = fil.read().splitlines()
        if len(lines) == 1:
            input_text = lines[0]
        else:
            inputs = lines

    part_1 = ""
    print(f"Part 1: {part_1}")
    part_2 = ""
    print(f"Part 2: {part_2}")

    return 0


if __name__ == "__main__":
    main()
