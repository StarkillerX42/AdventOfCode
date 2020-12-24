#!/usr/bin/env python3

import pprint
import numpy as np
from pathlib import Path

verbose = False
data_file = Path(__file__).absolute().parent.parent / 'dat/day_16.txt'

limits = {}

# 20 for full input, 3 for test
with data_file.open('r') as f:
    for line in f.readlines()[:20]:
        key, lims = line.strip().split(': ')
        int_lims = []
        for pair in lims.split(' or '):
            low, high = pair.split('-')
            low = int(low)
            high = int(high)
            int_lims.append(low)
            int_lims.append(high)
        limits[key] = int_lims

# 25 for full input, 8 for test
tickets = np.loadtxt(data_file.as_posix(), skiprows=25, delimiter=',',
                     dtype=int)
# 22 for full input, 5 for test
my_ticket = np.loadtxt(data_file.as_posix(), skiprows=22, max_rows=1,
                       delimiter=',', dtype=int)

print(f'My ticket: {my_ticket}')
if verbose:
    pprint.pprint(limits)


def check_valid(ticket, data_limits):
    """Checks whether or not ticket obeys the rules in data_limits
    """
    for val in ticket:

        valid_value = False
        for lim in data_limits.values():
            for lo, hi in zip(lim[::2], lim[1::2]):
                if (val >= lo) and (val <= hi):
                    valid_value = True
        if not valid_value:
            return val
    return -1


part_1 = []
part_2 = []
for ticket in tickets:
    val = check_valid(ticket, limits)
    if val == -1:
        part_2.append(ticket)
    else:
        part_1.append(val)

print(f'Part 1: {np.sum(part_1)}')

part_2 = np.array(part_2)


def check_col(col, data_limits):
    fitting_cols = []
    for key, lim in data_limits.items():
        fit = (((col >= lim[0]) & (col <= lim[1]))
               ^ ((col >= lim[2]) & (col <= lim[3])))
        # print(key, fit)
        if np.sum(~fit) == 0:
            fitting_cols.append(key)
    return fitting_cols


possible_names = []
for i, col in enumerate(part_2.T):
    possible_names.append(check_col(col, limits))

names = [''] * len(limits)
not_solved = True
while_count = 0
while not_solved:
    not_solved = False
    for i, matches in enumerate(possible_names):
        if len(matches) == 1:
            match = matches[0]
            names[i] = match
            not_solved = True
            for j, ms in enumerate(possible_names):
                if match in ms:
                    possible_names[j].remove(match)
    while_count += 1
    if while_count > len(limits):
        break

part_2_soln = 1
for name, val in zip(names, my_ticket):
    if 'departure' in name:
        part_2_soln *= val

print(f'Part 2: {part_2_soln}')
