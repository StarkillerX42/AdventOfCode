#!/usr/bin/env python3

import numpy as np

tickets = np.loadtxt('dat/day_5.txt', dtype=str)
# tickets = ['FBFBBFFRLR']
seat_ids = []

for ticket in tickets:
    low_row = 0
    high_row = 127
    low_col = 0
    high_col = 7
    row_range = ticket[0:7]
    col_range = ticket[7:]
    for row_val in row_range:
        rng = high_row - low_row
        if row_val == 'F':
            high_row = low_row + rng // 2
        else:
            low_row = low_row + rng // 2 + 1
    if low_row == high_row:
        row = low_row
    else:
        print(ticket, low_row, high_row)
        row = None

    for col_val, in col_range:
        rng = high_col - low_col
        if col_val == 'L':
            high_col = low_col + rng // 2
        else:
            low_col = low_col + rng // 2 + 1
    if low_col == high_col:
        col = low_col
    else:
        print(ticket, low_col, high_col)
        col = np.nan

    seat_id = row * 8 + col
    seat_ids.append(seat_id)

seat_ids = np.array(seat_ids)
print(f'Part 1: {np.max(seat_ids)}')

all_seats = np.arange(0, 127 * 8 + 7)
missing = np.array([seat_id not in seat_ids for seat_id in all_seats])
missing_ids = np.where(missing)[0]
my_seat = missing_ids[:-1][np.diff(missing_ids) > 1][-1]

print(f'Part 2: {my_seat}')
