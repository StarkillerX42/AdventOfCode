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


def get_neighbors_diag(i: int, j: int, arr: np.ndarray) -> list[list[int]]:
    neighbors = []
    for i2 in range(i - 1, i + 2):
        for j2 in range(j - 1, j + 2):
            if i2 >= 0 and i2 < arr.shape[0] and j2 >= 0 and j2 < arr.shape[1]:
                if i != i2 or j != j2:
                    neighbors.append([i2, j2])
    return np.array(neighbors)

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

    form = "grid"
    inputs = await asyncio.create_task(aoc_from_file(in_file, form, inp))
    inputs_raw = await asyncio.create_task(aoc_from_file(in_file, "none", inp))

    part_1 = 0
    usedNums = []
    for i, row in enumerate(inputs):
        buf = ""
        has_mark = False
        for j, c in enumerate(row):
            if c.isnumeric():
                neighbors = get_neighbors_diag(i, j, inputs)
                ns = list((inputs[*neighbor] for neighbor in neighbors))
                for n in ns:
                    if not n.isnumeric() and n != ".":
                        has_mark = True
                buf += c
            elif not c.isnumeric() and buf != "":
                if has_mark:
                    if verbose >= 1:
                        print(f"Adding {buf}")
                    if buf not in inputs_raw:  # Check that number isn't concatenated
                        raise ValueErorr(f"{buf} not a valid number at {(i, j)}")
                    usedNums.append(buf)
                    part_1 += int(buf)
                buf = ""
                has_mark = False

    usedI = 0
    for n in re.finditer(r"\d+", inputs_raw):
        if n.group() != usedNums[usedI]:
            print(n.group(), " missing")
        else:
            usedI += 1
    print(len(list(re.finditer(r"\d+", inputs_raw))), len(usedNums))
    if verbose >= 1:
        print(inputs)
    print(f"Part 1: {part_1}")
    part_2 = ""
    print(f"Part 2: {part_2}")

    return 0


if __name__ == "__main__":
    asyncio.run(main())
