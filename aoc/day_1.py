#!/usr/bin/env python3

import re
import asyncio

import numpy as np
import asyncclick as click

from pathlib import Path
from pprint import pprint
from rich.progress import track


async def aoc_from_file(file_name: str | Path, form, inp):
    in_file = Path(file_name) if isinstance(file_name, str) else file_name

    with in_file.open("r") as fil:
        lines = fil.read().splitlines()  # there is no "\n" in these
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
            case "newline string blocks":
                inputs = []
                chunk = []
                for line in lines:
                    if line == "":
                        inputs.append(chunk)
                        chunk = []
                    else:
                        chunk.append(line)
                inputs.append(chunk)
            case "newline strings":
                inputs = []
                for line in lines:
                    inputs.append(line)
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

    form = "newline strings"
    inputs = await asyncio.create_task(aoc_from_file(in_file, form, inp))

    # part_1 = 0
    nums = re.compile(r"\d")
    # for line in inputs:
    #     line_nums = nums.findall(line)
    #     part_1 += int(line_nums[0] + line_nums[-1])

    # print(f"Part 1: {part_1}")

    num_map = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
    }
    part_2: int = 0
    for line in inputs:
        if verbose >= 1:
            print(line)
        left = False
        right = False
        for i, c in enumerate(line):
            if left or nums.search(c) is not None:
                break
            for n, name in num_map.items():
                if name == line[i : i + len(name)]:
                    left = True
                    if verbose >= 2:
                        print(line)
                    line = line[:i] + f"{n:.0f}" + line[i + len(name) :]
                    if verbose >= 1:
                        print(f"Found name: {name} for left")
                        if verbose >= 2:
                            print(line)
                    break

        for i, c in enumerate(line[::-1]):
            if right:
                break
            for n, name in num_map.items():
                low = -i - 1
                high = min(0, low + len(name))
                if high == 0:
                    slice = line[low:]
                else:
                    slice = line[low:high]
                if name == slice:
                    right = True
                    if verbose >= 2:
                        print(line)
                    line = (
                        line[: len(line) + low] + f"{n:.0f}" + line[len(line) + high :]
                    )
                    if verbose >= 1:
                        print(f"Found name: {name} for right")
                        if verbose >= 2:
                            print(line)
                    break

        line_nums = nums.findall(line)
        res = int(line_nums[0] + line_nums[-1])
        if verbose >= 1:
            print(line)
            print(res)
        part_2 += res

    print(f"Part 2: {part_2:.0f}")

    return 0


if __name__ == "__main__":
    asyncio.run(main())
