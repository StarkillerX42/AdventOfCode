#!/usr/bin/env python3
"""This is a template for an Advent of Code day
"""

import re
import asyncio

import numpy as np
import asyncclick as click

from pathlib import Path
from typing import Union
from pprint import pprint
from rich.progress import track


async def aoc_from_file(file_name: str|Path, form: str, inp: int, custom_function=None):
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

    with in_file.open('r') as fil:
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
            case "int grid":
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
                    raise ValueError(f"Custom function undefined")
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

    form = "single string"
    inputs = await asyncio.create_task(aoc_from_file(in_file, form, inp))

    part_1 = ""
    print(f"Part 1: {part_1}")
    part_2 = ""
    print(f"Part 2: {part_2}")

    return 0


if __name__ == "__main__":
    asyncio.run(main())
