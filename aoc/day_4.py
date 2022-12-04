#!/usr/bin/env python3

import re
import asyncio

import numpy as np
import asyncclick as click

from pathlib import Path
from typing import Union


async def aoc_from_file(file_name: Union[str, Path], format, inp):
    in_file = Path(file_name) if isinstance(file_name, str) else file_name

    with in_file.open('r') as fil:
        lines = fil.read().splitlines()  # there is no "\n" in these
        if len(lines) == 1:
            inputs = lines[0]
        else:
            match format:
                case "newline ints":
                    inputs = []
                    for line in lines:
                        inputs.append(int(line))
                    inputs = np.array(inputs)
                case "newline int bundles":
                    inputs = []
                    chunk = []
                    for line in lines:
                        if line == "":
                            inputs.append(chunk)
                            chunk = []
                        else:
                            chunk.append(int(line))
                case "newline strings":
                    inputs = []
                    chunk = []
                    for line in lines:
                        if line == "":
                            inputs.append(chunk)
                            chunk = []
                        else:
                            chunk.append(line)
                case "comma paired lines":
                    inputs = []
                    for line in lines:
                        inputs.append(line.split(","))
                case "comma separated":
                    inputs = line.split(",")
                case "comma grid":
                    inputs = []
                    for line in lines:
                        inputs.append(line.split(","))
                    inputs = np.array(inputs)
                case "hash grid":
                    inputs = []
                    for line in lines:
                        inputs.append(list(line))
                    inputs = inputs == "#"
                case "binary grid":
                    inputs = []
                    for line in lines:
                        inputs.append(list(line))
                    inputs = inputs == "1"
                case "unknown":
                    inputs = lines
                case "int":
                    inputs = inp
                case _:
                    inputs = format

    return inputs


@click.command()
@click.argument("inp", default=0)
@click.option("-v", "--verbose", count=True)
@click.option("-t", "--test", is_flag=True)
async def main(inp, verbose, test) -> int:
    proj = Path(__file__).absolute().parent.parent
    day = re.search(r"\d+", Path(__file__).name)
    day = day.group(0) if day else ""
    day = day if day else ""
    if test:
        in_file = proj / f"dat/day_{day}_test.txt"
    else:
        in_file = proj / f"dat/day_{day}.txt"
    if verbose:
        print(f"Advent of Code Day {day}")

    format = "comma paired lines"
    inputs = await asyncio.create_task(aoc_from_file(in_file, format, inp))
    part_1 = 0
    part_2 = 0
    for line in inputs:
        lhs, rhs = line
        ll, lh = np.array(lhs.split('-')).astype(int)
        rl, rh = np.array(rhs.split('-')).astype(int)
        if (ll <= rl and lh >= rh) or (rl <= ll and rh >= lh):
            part_1 += 1

        if (lh >= rl and ll <= rh) or (rh >= ll and rl <= lh):
            part_2 += 1

    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")

    return 0


if __name__ == "__main__":
    asyncio.run(main())
