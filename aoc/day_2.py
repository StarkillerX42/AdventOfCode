#!/usr/bin/env python3

import re
import click

import numpy as np

from pathlib import Path


@click.command()
@click.argument("inp", default=0)
@click.option("-v", "--verbose", count=True)
@click.option("-t", "--test", is_flag=True)
def main(inp, verbose, test) -> int:
    proj = Path(__file__).absolute().parent.parent
    day = re.search(r"\d+", Path(__file__).name)
    day = day.group(0) if day else ""
    day = day if day else ""
    if test:
        in_file = proj / f"dat/day_{day}_test.txt"
    else:
        in_file = proj / f"dat/day_{day}.txt"
    if verbose >= 1:
        print(f"Advent of Code Day {day}")

    with in_file.open('r') as fil:
        lines = fil.read().splitlines()  # There is no "\n" in these
        if len(lines) == 1:
            inputs = lines[0]
        else:
            form = "uk"
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
                case "int":
                    inputs = inp  # From command line arguments
                case _:
                    inputs = lines

    map = {"X": "A", "Y": "B", "Z": "C"}
    values = {"A": 1, "B": 2, "C": 3}
    win = {"A": "C", "B": "A", "C": "B"}
    lose = {"A": "B", "B": "C", "C": "A"}
    rps = []
    for line in inputs:
        rps.append(line.split())

    part_1 = 0
    part_2 = 0
    for pair in rps:
        part_1 += values[map[pair[1]]]
        if win[map[pair[1]]] == pair[0]:  # Player wins
            part_1 += 6
        elif map[pair[1]] == pair[0]:  # Draw
            part_1 += 3
        elif lose[map[pair[1]]] == pair[0]:  # Lose
            part_1 += 0
        else:
            print(f"Undefined part 1 pair: {pair}")

        diff = 0
        match pair[1]:
            case "X":  # Must lose
                diff += values[win[pair[0]]]
            case "Y":  # Must Draw
                diff += values[pair[0]]
                diff += 3
            case "Z":  # Must win
                diff += values[lose[pair[0]]]
                diff += 6
        if verbose >= 1:
            print("-".join(pair), diff)
        part_2 += diff

    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")

    return 0


if __name__ == "__main__":
    main()
