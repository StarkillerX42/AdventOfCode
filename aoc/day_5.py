#!/usr/bin/env python3

import re
import asyncio
import copy

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
    for i, line in enumerate(inputs):
        try:
            n_lines = np.array(line.split()).astype(int).shape[0]
            i_lines = i
            break
        except ValueError:
            pass

    stacks = []
    for i in range(n_lines):
        rack = []
        for j in range(i_lines):
            if inputs[j][i * 4 + 1] != " ":
                rack.append(inputs[j][i * 4 + 1])
        stacks.append(rack)

    stacks_1 = copy.deepcopy(stacks)
    stacks_2 = copy.deepcopy(stacks)

    for i in range(i_lines + 2, len(inputs)):
        count, src, dest = np.array(inputs[i].split()[1::2]).astype(int)
        tmp = []
        for j in range(count):
            stacks_1[dest - 1].insert(0, stacks_1[src - 1].pop(0))
            tmp.append(stacks_2[src - 1].pop(0))
        for x in reversed(tmp):
            stacks_2[dest - 1].insert(0, x)
    part_1 = ""
    for stack in stacks_1:
        part_1 += stack[0]

    print(f"Part 1: {part_1}")

    part_2 = ""
    for stack in stacks_2:
        part_2 += stack[0]
    print(f"Part 2: {part_2}")

    return 0


if __name__ == "__main__":
    asyncio.run(main())
