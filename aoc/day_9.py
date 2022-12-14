#!/usr/bin/env python3

import re
import asyncio
import tqdm

import numpy as np
import asyncclick as click

from pathlib import Path
from typing import Union


class Rope:
    def __init__(self, length: int) -> None:
        assert length > 1, "Length must be greater than 1 for a head and a tail"
        self.body = np.array([[0, 0]] * length)
        self.history = []

    def move_head(self, command: str) -> None:
        # a for axis, d for direction
        match command[0]:
            case "U":
                a = 1
                d = 1
            case "D":
                a = 1
                d = -1
            case "L":
                a = 0
                d = -1
            case "R":
                a = 0
                d = 1
        self.body[0][a] += d

    def update_body(self) -> None:
        for i, link in enumerate(self.body[1:]):
            self.update_link(i, i + 1)

        self.history.append(self.body.copy())

    def update_link(self, i: int, j: int) -> None:
        diff = self.body[i] - self.body[j]

        for k, d in enumerate(diff):
            match (np.abs(d)):
                case 2:
                    self.body[j, k] += d // 2
                case 1:
                    if np.abs(diff[k - 1]) == 2:
                        self.body[j, k] += d
                case 0:
                    pass
                case _:
                    raise ValueError(f"Impossible rope state given,"
                                     f" {self.body[i]} and {self.body[j]} are"
                                     " too far away.")

    def count_unique_points(self, i):
        """A possibly unfinished visualization"""
        hist = np.array(self.history)[:, i]
        uniques = [hist[0]]
        for point in hist:
            if not np.any(np.all(point == uniques, axis=1)):
                uniques.append(point)
        return len(uniques)

    def draw_link_path(self, i: int):
        """A definitely unfinished visualization"""
        hist2 = np.array(self.hist)[:, i]
        xmin = hist2[:, 0].min()
        xmax = hist2[:, 0].max()
        ymin = hist2[:, 1].min()
        ymax = hist2[:, 1].max()
        sgrid = [""] * (ymax - ymin + 1)
        for i, y in enumerate(range(ymax, ymin - 1, -1)):
            for x in range(xmin, xmax + 1):
                if x == 0 and y == 0:
                    sgrid[i] += 's'
                elif (x, y) in hist2:
                    sgrid[i] += '#'
                else:
                    sgrid[i] += '.'
        print('\n'.join(sgrid))

    def draw_rope(self):
        xmin = min(self.body[:, 0].min(), 0)
        xmax = max(self.body[:, 0].max(), 0)
        ymin = min(self.body[:, 1].min(), 0)
        ymax = max(self.body[:, 1].max(), 0)
        sgrid = np.ones((xmax - xmin, ymax - ymin),
                        dtype=str)
        sgrid[sgrid == '1'] = '.'

        print('\n'.join(sgrid))


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
    rope_1 = Rope(2)
    rope_2 = Rope(10)

    for movement in tqdm.tqdm(inputs):
        for _ in range(int(movement[1])):
            rope_1.move_head(movement[0])
            rope_1.update_body()

            rope_2.move_head(movement[0])
            rope_2.update_body()

    if verbose >= 2:
        rope_2.draw_link_path(-1)
    part_1 = rope_1.count_unique_points(-1)
    print(f"Part 1: {part_1}")
    part_2 = rope_2.count_unique_points(-1)
    print(f"Part 2: {part_2}")

    return 0


if __name__ == "__main__":
    asyncio.run(main())
