#!/usr/bin/env python3

import re
import asyncio

import numpy as np
import asyncclick as click

from pathlib import Path
from typing import Union
from numba import njit, prange


# @njit()
def count_hidden(tree_grid, verbose=0):
    hidden = 0
    for i in prange(len(tree_grid)):
        for j in prange(len(tree_grid[i])):
            above = False
            below = False
            left = False
            right = False
            for ab in prange(j):
                above = above or tree_grid[i, j] <= tree_grid[i, ab]
            for be in prange(j+1, len(tree_grid[0])):
                below = below or tree_grid[i, j] <= tree_grid[i, be]
            for le in prange(i):
                left = left or tree_grid[i, j] <= tree_grid[le, j]
            for ri in prange(i + 1, len(tree_grid)):
                right = right or tree_grid[i, j] <= tree_grid[ri, j]
            is_hidden = above and below and left and right
            hidden += is_hidden
    return hidden


def score_views(tree_grid, verbose=0):
    views = np.ones(tree_grid.shape)
    for i in prange(tree_grid.shape[0]):
        for j in prange(tree_grid.shape[1]):
            if verbose:
                print(i, j, tree_grid[i, j])
            for k in range(j - 1, -1, -1):
                if tree_grid[i, k] >= tree_grid[i, j]:
                    if verbose:
                        print(f"    left: {j - k}, {j} {k}")
                    views[i, j] *= j - k
                    break
            else:
                if verbose:
                    print(f"    left: {j}")
                views[i, j] *= j
            for k in range(j + 1, tree_grid.shape[1], 1):
                if tree_grid[i, k] >= tree_grid[i, j]:
                    if verbose:
                        print(f"    right: {k - j}")
                    views[i, j] *= k - j
                    break
            else:
                views[i, j] *= tree_grid.shape[1] - j - 1
            for k in range(i - 1, -1, -1):
                if tree_grid[k, j] >= tree_grid[i, j]:
                    if verbose:
                        print(f"    above: {i - k}")
                    views[i, j] *= i - k
                    break
            else:
                views[i, j] *= i
            for k in range(i + 1, tree_grid.shape[0], 1):
                if tree_grid[k, j] >= tree_grid[i, j]:
                    if verbose:
                        print(f"    below: {k - i}")
                    views[i, j] *= k - i
                    break
            else:
                views[i, j] *= tree_grid.shape[0] - i - 1
            if verbose:
                print(f"    final: {views[i, j]}")
    return views


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

    form = "int grid"
    inputs = await asyncio.create_task(aoc_from_file(in_file, form, inp))

    hidden = count_hidden(inputs, verbose=verbose)

    part_1 = inputs.size - hidden
    print(f"Part 1: {part_1}")
    views = score_views(inputs, verbose)
    if verbose:
        print(views)
    part_2 = views.max()
    print(f"Part 2: {part_2:.0f}")

    return 0


if __name__ == "__main__":
    asyncio.run(main())
