#!/usr/bin/env python3
import pprint
from pathlib import Path

data_file = Path('dat/day_6.txt')

verbose = True
groups_1 = []
groups_2 = []
if data_file.exists():
    with data_file.open('r') as fil:
        group_data_1 = []
        group_data_2 = []
        for line in fil:
            line = line.strip('\n')
            if line == '':
                if verbose:
                    print('Making a new user')
                groups_1.append(set(group_data_1))
                groups_2.append(group_data_2)
                group_data_1 = []
                group_data_2 = []
            else:
                group_data_1.extend(line)
                group_data_2.append(line)
else:
    print('Data unavailable')

if verbose:
    pprint.pprint(groups_1)
    pprint.pprint(groups_2)

total_yesses = 0
for group in groups_1:
    total_yesses += len(group)

print(f'Part 1: {total_yesses}')


part_2_totals = 0
for group in groups_2:
    shared = group[0]
    i_len = len(shared)
    if verbose:
        print(shared)
    if len(group) > 1:
        for person in group:
            for item in shared:
                if item not in person:
                    shared = shared.replace(item, '')
    f_len = len(shared)
    if verbose:
        print('Length degreased by {}, {}'.format(i_len - f_len, shared))
    part_2_totals += len(shared)

print(f'Part 2: {part_2_totals}')
