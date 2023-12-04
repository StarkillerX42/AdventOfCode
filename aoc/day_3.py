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


def neighbors_window_slice(i: int, j: int, arr: np.ndarray) -> list[list[int]]:
    arr = np.array(arr)
    ilo = max(0, i - 1)
    ihi = min(i + 1, arr.shape[0])
    jlo = max(0, j - 1)
    jhi = min(j + 1, arr.shape[1])
    neighbors = arr[ilo : ihi + 1, jlo : jhi + 1]
    return neighbors


def get_window(reMatch: re.Match, lineLength: int, nLines=None) -> np.ndarray[str]:
    if nLines is None:
        nLines = lineLength
    start, stop = reMatch.span()
    istart = start // lineLength
    iend = start // lineLength + 1
    jstart = start % lineLength
    jend = stop % lineLength
    if jend == 0:
        jend = lineLength
    iwstart = max(0, istart - 1)
    jwstart = max(0, jstart - 1)
    iwend = min(nLines, iend + 1)
    jwend = min(lineLength, jend + 1)

    return istart, iend, jstart, jend, iwstart, jwstart, iwend, jwend


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

    numRE = re.compile(r"\d+")

    part_1 = 0
    usedNums = []
    nLines, lineLength = inputs.shape
    lineLength += 1
    for num in numRE.finditer(inputs_raw):
        istart, iend, jstart, jend, iwstart, jwstart, iwend, jwend = get_window(
            num, lineLength=lineLength, nLines=nLines
        )
        # print(num.group(), start, stop, istart, ":", iend, jstart, ":", jend)
        if verbose >= 2:
            print(
                num.group(),
                iwstart,
                ":",
                iwend,
                jwstart,
                ":",
                jwend,
                "\n",
                inputs[iwstart:iwend, jwstart:jwend],
            )
        for c in inputs[iwstart:iwend, jwstart:jwend].flatten():
            if not c.isnumeric() and c != ".":
                # print(c, end=", ")
                n = "".join(inputs[istart, jstart:jend])
                # print(n, num.group())
                usedNums.append(n)
                part_1 += int(n)
                break

    if verbose >= 1:
        p = "\n".join(usedNums)
        print(f"{p}")

    if verbose >= 1:
        print(inputs)
    print(f"Part 1: {part_1}")
    part_2 = 0

    for star in re.finditer(r"\*", inputs_raw):
        istart, iend, jstart, jend, iwstart, jwstart, iwend, jwend = get_window(
            star, lineLength=lineLength, nLines=nLines
        )
        # print(inputs[iwstart:iwend, jwstart:jwend])
        prodParts = []
        for i, line in enumerate(inputs[iwstart:iwend, jwstart:jwend]):
            last = ""
            for j, c in enumerate(line):
                if c.isnumeric() and not last.isnumeric():
                    lineStr = "".join(inputs[i + iwstart])
                    for m in numRE.finditer(lineStr):
                        if j + jwstart >= m.start() and j + jwstart <= m.end():
                            prodParts.append(int(m.group()))
                last = c
        match len(prodParts):
            case 0:
                pass
            case 1:
                pass
            case 2:
                if verbose >= 1:
                    print(prodParts)
                part_2 += np.prod(prodParts)
            case _:
                raise ValueError(f"Found more than 2 gears: {', '.join(prodParts)}")

    print(f"Part 2: {part_2}")

    return 0


if __name__ == "__main__":
    asyncio.run(main())
