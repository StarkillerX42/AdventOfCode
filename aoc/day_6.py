#!/usr/bin/env python3

import re
import asyncio

import numpy as np
import asyncclick as click

from pathlib import Path
from typing import Union


async def aoc_from_file(file_name: Union[str, Path], form, inp):
    in_file = Path(file_name) if isinstance(file_name, str) else file_name

    with in_file.open('r') as fil:
        lines = fil.read().splitlines()  # there is no "\n" in these
        if len(lines) == 1:
            inputs = lines[0]
        else:
            match form:
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

    form = "unknown"
    inputs = await asyncio.create_task(aoc_from_file(in_file, form, inp))
    part_1 = 0
    part_2 = 0
    for i, char in enumerate(inputs):
        low = max(0, i - 3)
        low_2 = max(0, i - 13)
        subset = inputs[low: i + 1]
        subset_2 = inputs[low_2: i + 1]
        # print(subset)
        is_match_1 = True
        is_match_2 = True
        for char2 in subset:
            if subset.count(char2) > 1 or len(subset) != 4:
                is_match_1 = False
        for char2 in subset_2:
            if subset_2.count(char2) > 1 or len(subset_2) != 14:
                is_match_2 = False
        if is_match_1 and part_1 == 0:
            part_1 = i + 1
        if is_match_2 and part_2 == 0:
            part_2 = i + 1

    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")

    return 0


if __name__ == "__main__":
    asyncio.run(main())
