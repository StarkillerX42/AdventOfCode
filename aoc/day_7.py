#!/usr/bin/env python3

import re
import asyncio

import numpy as np
import asyncclick as click

from pathlib import Path
from typing import Union
from pprint import pprint


class File:
    def __init__(self, path, name: str, size: int = np.nan, parent=None):
        self.path = path
        self.parent = parent
        self.size = size
        self.name = name

    def display(self, indent=0):
        print("    " * indent + f"{self.size:8.0f} {self.name}")


class Directory:
    def __init__(self, path: list, name, parent=None):
        self.path = path
        self.name = name
        self.parent = parent
        self.contents = []
        self.sizes = []
        self.size = np.nan

    def add_directory(self, dir_name):
        dir = Directory(path=self.path + [self.name], name=dir_name,
                        parent=self)
        self.contents.append(dir)
        self.sizes.append(np.nan)

    def add_file(self, file_name, file_size: int = np.nan):
        file = File(path=self.path + [file_name], name=file_name,
                    size=int(file_size), parent=self)
        self.contents.append(file)

    def find_size(self, sizes, verbose=0):
        size = 0
        for content in self.contents:
            if content.size == 0 or np.isnan(content.size):
                if verbose >= 2:
                    print(f"Finding size of {content.name}")
                size += content.find_size(sizes)
            else:
                size += content.size
            if isinstance(content, Directory) and content.size <= 100000:
                sizes.append(content.size)

        self.size = size
        return size

    def get_path(self):
        return self.path + self.name

    def __str__(self):
        newline = '\n'
        return f"Directory {newline.join(self.path + [self.name])}"

    def get_recursive_sizes(self, out_sizes=[]):
        out_sizes.append(self.size)
        for c in self.contents:
            if isinstance(c, Directory):
                out_sizes.append(c.size)
                c.get_recursive_sizes(out_sizes)

    def display(self, indent=0):
        # print("/".join(path))
        if indent == 0:
            print(f"{self.size:<8.0f} --- {self.name}")
        for c in self.contents:
            end = "/" if isinstance(c, Directory) else ""
            print("    " * indent + f"{c.size:>8.0f}", c.name + end)
            if isinstance(c, Directory):
                c.display(indent=indent + 1)

    def __iter__(self):
        for f in self.contents:
            yield f


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
                    inputs = inputs == "1"
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

    rootfs = Directory([], "/")
    loc = rootfs
    new_path_re = re.compile(r"(?<=\$ cd )[A-Za-z\/]+")
    dir_re = re.compile(r"(?<=dir )[A-Za-z]+")
    file_size_re = re.compile(r"(?=\d+ [A-Za-z\.]+)\d+")
    file_name_re = re.compile(r"(?<=\d )[A-Za-z\.]+")
    for line in inputs[1:]:
        if "dir " in line:
            loc.add_directory(dir_re.search(line).group())
        elif "$ cd" in line:
            if ".." in line:
                loc = loc.parent
            else:
                new_loc = new_path_re.search(line).group()
                for f in loc.contents:
                    if isinstance(f, Directory):
                        if f.name == new_loc:
                            loc = f
        elif "$ ls" in line:
            continue
        else:
            loc.add_file(file_name_re.search(line).group(),
                         int(file_size_re.search(line).group()))

    if verbose >= 2:
        rootfs.display()
    sizes = []
    rootfs.find_size(sizes)
    print(f"root size: {rootfs.size}")
    if verbose >= 2:
        rootfs.display()
    part_1 = np.sum(sizes)

    print(f"Part 1: {part_1}")
    part_2_sizes = []
    rootfs.get_recursive_sizes(part_2_sizes)
    needed_size = rootfs.size - (70000000 - 30000000)

    if verbose:
        print(f"Needed size: {needed_size}")
    s = np.array(part_2_sizes)
    s = s[s >= needed_size]
    s.sort()
    part_2 = s[0]
    print(rootfs.size - part_2)
    print(f"Part 2: {part_2}")

    return 0


if __name__ == "__main__":
    asyncio.run(main())
