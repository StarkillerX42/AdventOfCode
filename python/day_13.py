#!/usr/bin/env python3

import numpy as np
from pathlib import Path

input_text = Path('dat/day_13_test.txt').open('r')
t0 = int(input_text.readline().strip())
line2 = input_text.readline().strip().split(',')
buses = np.array([int(i) for i in line2
                  if i != 'x'])
buses.sort()
bus_loc = np.array([line2.index(bus) for bus in buses.astype(str)])


times = np.arange(t0, t0 + np.max(buses))
first_time = t0 + np.max(buses)
result = 0
for bus in buses:
    bus_remainders = times[times % bus == 0]
    result = (bus * (bus_remainders[0] - t0)
              if bus_remainders[0] < first_time else result)
    first_time = (bus_remainders[0]
                  if bus_remainders[0] < first_time else first_time)

print(f'Part 1: {result}')


step_size = np.max(buses)
time = step_size
step_loc = line2.index(str(step_size))
not_found = True
limit = 100000000000000
print_lim = 1000000000
print_count = 0
while not_found:
    not_found = False
    if np.sum((time - (step_loc - bus_loc)) % buses != 0):
        not_found = True

    time += step_size
    if time > limit:
        print("Couldn't find a valid time")
        break
    if print_count > print_lim:
        print('Another billion')
        print_count = 0

print(f'Part 2: {time - step_size - step_loc}')
