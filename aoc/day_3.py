#!/usr/bin/env python3

import re
import asyncio

import numpy as np
import asyncclick as click

from pathlib import Path
from typing import Union


def find_duplicate(sack: str, verbose: int = 0) -> str:
    candidates = set(sack)
    lhs = sack[:len(sack)//2]
    rhs = sack[len(sack)//2:]
    cross_median = 0
    crosser = ""
    for j, char2 in enumerate(candidates):
        if lhs.count(char2) > 0 and rhs.count(char2) > 0:
            cross_median += 1
            crosser = char2

    return crosser


def get_priority(char: str) -> int:
    v = ord(char)
    if v >= 97:
        return v - 96
    else:
        return v - 64 + 26


def find_badge(bundle: list) -> str:
    candidates = set(bundle[0])
    for sack in bundle[1:]:
        removable = []
        for candidate in candidates:
            if sack.count(candidate) == 0:
                removable.append(candidate)
        for char in removable:
            candidates.remove(char)
    return candidates.pop()


async def aoc_from_file(file_name: Union[str, Path], format, inp):
    in_file = Path(file_name) if isinstance(file_name, str) else file_name

    format = "strings"
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
                case "strings":
                    inputs = lines
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
                    inputs = lines

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

    inputs = await asyncio.create_task(aoc_from_file(in_file, format, inp))

    part_1 = 0
    for sack in inputs:
        dup = find_duplicate(sack, verbose)
        v = get_priority(dup)
        part_1 += v
        if verbose:
            print(f"Found {dup} in {sack}, valued {v}")
    print(f"Part 1: {part_1}")
    part_2 = 0
    for i_bundle in range(0, len(inputs), 3):
        bundle = inputs[i_bundle:i_bundle + 3]
        badge = find_badge(bundle)
        part_2 += get_priority(badge)
    print(f"Part 2: {part_2}")

    return 0


if __name__ == "__main__":
    asyncio.run(main())
