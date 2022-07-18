import click
import tqdm

import numpy as np

from pathlib import Path


def cup_round(cups, i, verbose=False):
    while i >= len(cups):
        i -= len(cups)
    i_val = cups[i]
    if verbose:
        print(f"Pointer at {i_val}")
    stack = []
    for _ in range(3):
        popper = i + 1 if i + 1 < len(cups) else 0
        stack.append(cups.pop(popper))
    if verbose:
        print(f"Stack is {stack}")

    insert_val = i_val - 1
    while insert_val not in cups:
        insert_val -= 1
        if insert_val <= 0:
            insert_val = max(cups)
    if verbose:
        print(f"Destination is {insert_val}")

    insert_i = cups.index(insert_val)
    for j, val in enumerate(stack):
        cups.insert(insert_i + j + 1, val)

    return cups.index(i_val) + 1


def cup_round_dict(cups, ptr, verbose=False):
    if verbose:
        print(f"Pointer is at {ptr}")
    stack = []
    stack.append(cups[ptr])
    for j in range(2):
        stack.append(cups.pop(stack[j]))
    cups[ptr] = cups[stack[-1]]
    cups.pop(stack[-1])
    if verbose:
        print(f"Stack is {stack}")

    dest = ptr - 1
    if dest not in cups.keys():
        while dest not in cups.keys():
            dest -= 1
            if dest < 0:
                dest = max(cups.keys())
    if verbose:
        print(f"Destination at {dest}")
    end = cups[dest]
    for j, v in enumerate(stack):
        cups[dest] = v
        dest = v
    cups[dest] = end

    return cups[ptr]


def gen_final_dict_desult(cups):
    out = f"{cups[1]:.0f}"
    ptr = cups[1]

    while cups[ptr] != 1:
        out += f"{cups[ptr]:.0f}"
        ptr = cups[ptr]
    return out


def gen_final_result(cups):
    cups = cups.copy()
    i_1 = cups.index(1)
    print(cups)
    cups = cups[i_1 + 1:] + cups[0:i_1]
    print(cups)
    result = "".join([f"{x:.0f}" for x in cups])
    return result


@click.command()
@click.option("-v", "--verbose", count=True)
@click.option("-t", "--testing", is_flag=True)
def main(verbose=False, testing=False):
    date = __file__.split("day_")[-1].rstrip(".py")

    cups_str = "476138259" if not testing else "389125467"
    cups = list(cups_str)
    cups = [int(x) for x in cups]

    # print(cups)
    i = 0
    count = 0
    # limit = 10  # Demo
    limit = 100  # Part 1
    ticker = tqdm.tqdm(total=limit)
    while count < limit:
        if verbose:
            print(f"Round {count + 1}:  {cups}")
        while i >= len(cups):
            i -= len(cups)
        i = cup_round(cups, i, verbose)
        count += 1
        ticker.update()

    print(cups)
    part_1 = gen_final_result(cups)

    print(f"Part 1: {part_1}")

    cups = [int(x) for x in list(cups_str)]
    cups_dict = {}
    for i, cup in enumerate(cups[:-1]):
        cups_dict[cup] = cups[i + 1]
    cups_dict[cups[-1]] = max(cups) + 1
    for i in range(max(cups) + 2, 1000001):
        cups_dict[i - 1] = i
    cups_dict[i] = cups[0]
    limit = 10000000
    count = 0
    ticker = tqdm.tqdm(total=limit)
    i = cups[0]
    while count < limit:
        if verbose:
            print(f"Round {count + 1}:  {cups_dict}")
        i = cup_round_dict(cups_dict, i, verbose)
        count += 1
        ticker.update()
    ticker.close()
    part_2 = cups_dict[1] * cups_dict[cups_dict[1]]
    print()
    print(f"Part 2: {part_2}")


if __name__ == "__main__":
    main()
