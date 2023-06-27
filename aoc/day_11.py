#!/usr/bin/env python3

import re
import copy
import tqdm
import asyncio

import numpy as np
import asyncclick as click

from pathlib import Path
from typing import Union
from pprint import pprint


class Monkey:
    def __init__(self, number: int, items: list, logic: str, div: int,
                 true_dest: int,
                 false_dest: int, others, verbose=0):
        self.number: int = number
        self.items = items
        self.div = div
        self.logic = logic
        self.true_dest = true_dest
        self.false_dest = false_dest
        self.others = others
        self.n_inspections = 0
        self.verbose = verbose

    def new_worry_level(self, old: int, style=1) -> int:
        new = eval(self.logic)
        if style == 1:
            return new // 3
        else:
            return new % style

    def inspect_item(self, **kwargs) -> None:
        item = self.items.pop(0)
        new_level = self.new_worry_level(item, **kwargs)
        if new_level % self.div == 0:
            if self.verbose >= 2:
                print(f"Throwing {item} to {self.true_dest} as {new_level}")
            self.throw_to(self.true_dest, new_level)
        else:
            if self.verbose >= 2:
                print(f"Throwing {item} to {self.false_dest} as {new_level}")
            self.throw_to(self.false_dest, new_level)
        self.n_inspections += 1

    def throw_to(self, i, item) -> None:
        other = self.others[i]
        other.items.append(item)

    def __str__(self):
        return (f"Monkey {self.number} with {self.items} and inspections"
                f" {self.n_inspections}")

    def __repr__(self):
        return self.__str__()

    def inspect_all(self, **kwargs):
        count = 0
        while len(self.items) != 0 and count < 100:
            self.inspect_item(**kwargs)
            count += 1


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

    form = "newline strings"
    inputs = await asyncio.create_task(aoc_from_file(in_file, form, inp))

    num_re = re.compile(r"\d+")
    monkeys = {}
    divs = []
    for monkey in inputs:
        num = int(num_re.search(monkey[0]).group())
        items = [int(x) for x in monkey[1].split(": ")[-1].split(", ")]
        monkeys[num] = Monkey(num, items,
                              monkey[2].split(" = ")[-1],
                              int(num_re.search(monkey[3]).group()),
                              int(num_re.search(monkey[4]).group()),
                              int(num_re.search(monkey[5]).group()), monkeys,
                              verbose)
        divs.append(int(num_re.search(monkey[3]).group()))

    monkeys_2 = copy.deepcopy(monkeys)
    if verbose:
        pprint(monkeys)

    for _ in range(20):
        for k, monkey in monkeys.items():
            monkey.inspect_all()

    if verbose:
        pprint(monkeys)

    inspections = []
    for k, monkey in monkeys.items():
        inspections.append(monkey.n_inspections)

    inspections.sort()
    part_1 = np.prod(inspections[-2:])

    print(f"Part 1: {part_1}")
    style = np.prod(divs)

    for i in tqdm.tqdm(range(10000)):
        for k, monkey in monkeys_2.items():
            monkey.inspect_all(style=style)
    inspections = []
    for k, monkey in monkeys_2.items():
        inspections.append(monkey.n_inspections)

    if verbose:
        print(inspections)
    inspections.sort()
    part_2 = np.prod(inspections[-2:])

    print(f"Part 2: {part_2}")

    return 0


if __name__ == "__main__":
    asyncio.run(main())
