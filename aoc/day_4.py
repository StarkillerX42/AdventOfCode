#!/usr/bin/env python3
"""This is a template for an Advent of Code day
"""

import asyncio
import re
from pathlib import Path
from pprint import pprint

import asyncclick as click
import numpy as np
from rich.progress import track

from aoc import tools


async def aoc_from_file(
    file_name: str | Path, form: str, inp: int, custom_function=None
):
    """Reads an Advent of Code input file according to the given format

    Args:
        file_name (str | Path): The input file path
        form (str): A supported format to be read
        inp (int): In the case where a single int is given as input, returns
            that, useful for preserving overall structure
        custom_function (callable, optional): If form="custom", uses this
            function to process the input text. Defaults to None.

    Raises:
        ValueError: For unsupported outputs

    Returns:
        str | list[str] | list[list[str]] | np.ndarray: A logical output
            datatype for the given input and form
    """
    in_file = Path(file_name) if isinstance(file_name, str) else file_name

    with in_file.open("r") as fil:
        txt = fil.read()
        lines = txt.splitlines()  # there is no "\n" in these
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
                inputs.append(chunk)
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
            case "grid":
                inputs = []
                for line in lines:
                    inputs.append(list(line))
                inputs = np.array(inputs)
            case "single string":
                inputs = lines
            case "int":
                inputs = inp
            case "custom":
                if custom_function is not None:
                    inputs = custom_function(lines)
                else:
                    raise ValueError("Custom function undefined")
            case _:
                inputs = txt

    return inputs

def read_cards(lines) -> np.ndarray[int]:
    lineRE = re.compile(r"([\d\s]+)\|([\d\s]+)")
    wins = []
    yours = []
    for line in lines:
        nums = lineRE.search(line)
        wins.append(nums.group(1).split())
        yours.append(nums.group(2).split())
    return np.array(wins).astype(int), np.array(yours).astype(int)


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

    form = "custom"
    wins, yours = await asyncio.create_task(aoc_from_file(in_file, form, inp, custom_function=read_cards))

    matches = []
    for w, y in zip(wins, yours):
        mtch = np.sum([yi in w for yi in y])
        matches.append(mtch)
    
    matches = np.array(matches)
    part_1 = np.sum(2**(matches[matches != 0] - 1))
    
    print(f"Part 1: {part_1}")

    card_counts = [1] * len(matches) # + [0] * (len(matches) - 1)
    for i, m in enumerate(matches):
        for j in range(m):
            card_counts[i + j + 1] += card_counts[i]

    part_2 = np.sum(card_counts)
    print(f"Part 2: {part_2}")

    return 0


if __name__ == "__main__":
    asyncio.run(main())
