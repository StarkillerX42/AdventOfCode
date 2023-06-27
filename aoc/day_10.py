#!/usr/bin/env python3

import re
import tqdm
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
                case "space paired lines":
                    inputs = []
                    for line in lines:
                        inputs.append(line.split())
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
                    inputs = np.array(inputs) == "1"
                case "int grid":
                    inputs = []
                    for line in lines:
                        inputs.append(list(line))
                    inputs = np.array(inputs)
                case "single string":
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

    form = "space paired lines"
    inputs = await asyncio.create_task(aoc_from_file(in_file, form, inp))

    x = 1
    cycle = 1
    queued = 0
    queue = []
    next_stop = 20
    checkpoints = []
    part_1 = 0
    i = 0
    crt = [""]
    while i < len(inputs) and cycle < 10000:
        if (cycle - 20) % 40 == 0:
            signal = cycle * x
            checkpoints.append(signal)

        if verbose >= 2:
            print(f"Cycle {cycle}, X: {x}")
        if verbose >= 1 and (cycle - 20) % 40 == 0:
            print(f"Signal: {signal}")

        # Image drawing
        if np.abs((x + 1) - (cycle % 40)) <= 1:
            crt[-1] += '#'
        else:
            crt[-1] += ' '
        if cycle % 40 == 0:
            crt[-1] += '|'
            crt.append("")

        # Prep for next cycle
        if len(queue) == 0:
            line = inputs[i]
            i += 1
            match(line[0]):
                case "noop":
                    pass
                case "addx":
                    queue.append(int(line[1]))
        else:
            x += queue.pop(0)
        cycle += 1

    if verbose >= 1:
        print(f"Checkpoints: {checkpoints}")
    part_1 = np.sum(checkpoints)
    print(f"Part 1: {part_1}")
    part_2 = "\n".join(crt)
    print(f"Part 2: \n{part_2}")

    return 0


if __name__ == "__main__":
    asyncio.run(main())
