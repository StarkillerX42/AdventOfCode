#!/usr/bin/env python3

import numpy as np

from pathlib import Path


data_file = Path('dat/day_11.txt')

seats = []
with data_file.open('r') as f:
    for line in f:
        line = line.strip()
        seat_row = list(line)
        seats.append(seat_row)

seats_1 = np.array(seats)
verbose = True
if verbose:
    print(f'Seats shape: {seats_1.shape}')


changing = True
while_count = 0
while changing:
    changing = False
    new_seats = seats_1.copy()
    for i, row in enumerate(seats_1):
        for j, seat in enumerate(row):
            if seat == '#':
                low_row = i - 1 if i > 0 else 0
                high_row = i + 2 if i < seats_1.shape[0] else seats_1.shape[0]
                low_col = j - 1 if j > 0 else 0
                high_col = j + 2 if j < seats_1.shape[1] else seats_1.shape[1]
                neighbor_seats = seats_1[low_row: high_row, low_col: high_col]
                if (neighbor_seats == '#').sum() - 1 >= 4:
                    # if verbose:
                    #     print(f'Emptying ({i}, {j})')
                    new_seats[i, j] = 'L'
                    changing = True

            elif seat == 'L':
                low_row = i - 1 if i > 0 else 0
                high_row = i + 2 if i < seats_1.shape[0] else seats_1.shape[0]
                low_col = j - 1 if j > 0 else 0
                high_col = j + 2 if j < seats_1.shape[1] else seats_1.shape[1]
                neighbor_seats = seats_1[low_row: high_row, low_col: high_col]
                if (neighbor_seats == '#').sum() == 0:
                    # if verbose:
                    #     print(f'Filling ({i}, {j})')
                    new_seats[i, j] = '#'
                    changing = True
            elif seat == '.':
                pass
            else:
                raise ValueError(f'Invalid seat: {seat}')
    seats_1 = new_seats
    while_count += 1
    if while_count > 1000:
        break
    if verbose:
        if while_count % 10 == 0:
            print(f'Loop {while_count}')


print(f'Part 1: {(seats_1 == "#").sum()}, count: {while_count}')


seats_2 = np.array(seats)
directions = np.array([[-1, -1], [-1, 0], [-1, 1], [0, -1],
                       [0, 1], [1, -1], [1, 0], [1, 1]])

changing = True
while_count = 0
while changing:
    changing = False
    new_seats = seats_2.copy()
    for i, row in enumerate(seats_2):
        for j, seat in enumerate(row):
            # print(f'New location {i}, {j}')
            occupied_neighbors = 0
            if seat == '#':
                for d in directions:
                    loc = np.array([i, j]) + d
                    count_2 = 0
                    while True:
                        if np.any(loc < 0):
                            break
                        elif np.any(loc >= seats_2.shape):
                            break
                        elif seats_2[tuple(loc)] == '#':
                            occupied_neighbors += 1
                            # print(f'Found neighbor: {loc[0]}, {loc[1]}')
                            break
                        elif seats_2[tuple(loc)] == 'L':
                            break
                        else:
                            pass
                        loc += d
                        count_2 += 1
                        if count_2 > 100:
                            print(f'Failing to find neighbor at {loc}')
                            exit()
                        # print(f'No neighbor found {i} {j}')
                if occupied_neighbors >= 5:
                    # print(f'Leaving seat {i} {j}')
                    new_seats[i, j] = 'L'
                    changing = True

            elif seat == 'L':
                for d in directions:
                    loc = np.array([i, j]) + d
                    count_2 = 0
                    while True:
                        if np.any(loc < 0):
                            break
                        elif np.any(loc >= seats_2.shape):
                            break
                        elif seats_2[tuple(loc)] == '#':
                            # print(f'Found neighbor: {loc[0]}, {loc[1]}')
                            occupied_neighbors += 1
                            break
                        elif seats_2[tuple(loc)] == 'L':
                            # print(f'Found empty seat: {loc[0], loc[1]}')
                            break
                        else:
                            pass
                        loc += d
                        count_2 += 1
                        if count_2 > 100:
                            print(count_2, loc,)
                            exit()
                        # print(f'No neighbor found {i} {j}')
                if occupied_neighbors == 0:
                    new_seats[i, j] = '#'
                    # print(f'Filling seat {i} {j}')
                    changing = True
            elif seat == '.':
                pass
            else:
                print(f'Invalid seat: {seat}')
    seats_2 = new_seats
    while_count += 1
    if while_count > 1000:
        break
    if verbose:
        if while_count % 10 == 0:
            print(f'Loop {while_count}')

print(f'Part 2: {np.sum(seats_2 == "#")}, Loop count: {while_count}')
