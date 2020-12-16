#!/usr/bin/env python3

import pprint

import numpy as np

from pathlib import Path


data_file = Path('dat/day_12.txt')

directions = []
with data_file.open('r') as fil:
    for line in fil:
        line = line.strip()
        directions.append([line[0], int(line[1:])])


orientations = ['N', 'E', 'S', 'W']
verbose = True


class Ship:
    def __init__(self):
        self.waypoint = np.array([1, 10])
        self.position = np.array([0, 0])
        self.orientation = 'E'

    def move_1(self, bearing, magnitude):

        if bearing == 'F':
            bearing = self.orientation

        if bearing == 'N':
            self.position[0] += magnitude
        elif bearing == 'E':
            self.position[1] += magnitude
        elif bearing == 'S':
            self.position[0] -= magnitude
        elif bearing == 'W':
            self.position[1] -= magnitude
        elif bearing == 'R':
            curr_index = orientations.index(self.orientation)
            rot = magnitude // 90
            self.orientation = orientations[curr_index
                                            - len(orientations) + rot]
        elif bearing == 'L':
            curr_index = orientations.index(self.orientation)
            rot = magnitude // 90
            self.orientation = orientations[curr_index - rot]

        else:
            raise ValueError(f'Invalid bearing {bearing}')

    def move_2(self, bearing, magnitude):

        if bearing == 'F':
            self.move_1('N', self.waypoint[0] * magnitude)
            self.move_1('E', self.waypoint[1] * magnitude)

        elif bearing == 'N':
            self.waypoint[0] += magnitude
        elif bearing == 'E':
            self.waypoint[1] += magnitude
        elif bearing == 'S':
            self.waypoint[0] -= magnitude
        elif bearing == 'W':
            self.waypoint[1] -= magnitude

        elif bearing == 'R':
            rot = magnitude // 90
            if rot % 2 == 0:
                self.waypoint = - self.waypoint
            else:
                self.waypoint = self.waypoint[::-1]
                self.waypoint[rot // 2] *= -1
        elif bearing == 'L':
            rot = magnitude // 90
            if rot % 2 == 0:
                self.waypoint = - self.waypoint
            else:
                self.waypoint = self.waypoint[::-1]
                self.waypoint[-rot // 2] *= -1


ship1 = Ship()
ship2 = Ship()
for direction in directions:
    ship1.move_1(*direction)
    ship2.move_2(*direction)
    if verbose:
        print(direction, ship2.position, ship2.waypoint)

print(f'Part 1: {np.sum(np.abs(ship1.position))}')
print(f'Part 1: {np.sum(np.abs(ship2.position))}')
