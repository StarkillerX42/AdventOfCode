#!/usr/bin/env python3

import re
import tqdm
import asyncio

import numpy as np
import asyncclick as click

from pathlib import Path
from typing import Union
from pprint import pprint


def get_neighbors(point: np.ndarray, grid: np.ndarray, explored: np.ndarray,
                  frontier) -> np.ndarray:
    neighbors = point + np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
    is_good = np.ones((4), dtype=bool)
    for i, neighbor in enumerate(neighbors):
        if (np.any(neighbor < 0)
            or neighbor[0] >= grid.shape[0]
                or neighbor[1] >= grid.shape[1]):
            is_good[i] = False
        else:
            delta_h = grid[*neighbor] - grid[*point]
            if (delta_h > 1 or delta_h < -3
                    or explored[*neighbor]):
                is_good[i] = False

    return neighbors[is_good]


async def aoc_from_file(file_name: Union[str, Path], form, inp):
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
    grid = np.zeros((len(inputs[0]), len(inputs)), dtype=int)
    efforts = np.ones(grid.shape, dtype=int) * np.inf
    for i, line in enumerate(inputs):
        for j, char in enumerate(line):
            grid[j, i] = ord(char) - ord('a') + 1

    grid[grid == ord('S') - ord('a') + 1] = 0
    grid[grid == ord('E') - ord('a') + 1] = ord('z') - ord('a') + 2
    efforts[grid == 0] = 0
    explored = efforts == 0
    start = np.where(grid == 0)
    start = np.array([start[0][0], start[1][0]])
    dest = np.where(grid == ord('z') - ord('a') + 2)
    dest = np.array([dest[0][0], dest[1][0]])
    if verbose:
        print(f"Starting at {start}, looking for {dest}")
    frontier = [start]
    pbar = tqdm.tqdm(total=grid.size)
    count = 0
    points = []
    while np.isinf(efforts[*dest]) and count < 100000:
        point = frontier.pop(0)
        points.append(explored[*point])
        neighbors = get_neighbors(point, grid, explored, frontier)
        for neighbor in neighbors:
            if explored[*neighbor]:
                continue
            if efforts[*neighbor] > efforts[*point] + 1:
                print("updating effort")
                efforts[*neighbor] = efforts[*point] + 1
            if not explored[*neighbor]:
                frontier.append(neighbor)
        explored[*point] = True
        pbar.update()
        count += 1

    efforts = efforts.astype(int)
    points.sort()
    # print(frontier, len(frontier))
    part_1 = efforts[*dest]

    print(f"Part 1: {part_1}")
    part_2 = ""
    print(f"Part 2: {part_2}")

    return 0


if __name__ == "__main__":
    asyncio.run(main())
