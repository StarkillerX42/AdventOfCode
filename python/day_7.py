#!/usr/bin/env python3

from pathlib import Path

data_file = Path('dat/day_7.txt')

verbose = False

lines = data_file.open('r').readlines()


class Bag:
    def __init__(self, name):
        adj, col = name.split()
        self.name = ' '.join([adj, col])
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __eq__(self, other):
        return other.name == self.name

    def __str__(self):
        return (f'{self.name}:\n'
                + '\n'.join([
                    f'    - {c.count} {c.name}'
                    for c in self.children])
                )

    def count_children(self, bag_list):
        global child_count_loops
        child_count_loops += 1
        total = 1
        for c in self.children:
            for b in bag_list:
                if b == c:
                    total += c.count * b.count_children(bag_list)
        if verbose:
            print(total, self.name)
        return total


class Child(Bag):
    def __init__(self, count, name):
        super().__init__(name)
        if 'bag' in name:
            name = name.split('bag')[0]
        adj, col = name.split()
        self.name = ' '.join([adj, col])
        self.count = int(count)

    def __str__(self):
        return f'{self.count} {self.name}'


target = None
bags = []
for line in lines:
    line = line.strip('.\n')
    parent, children = line.split('bags contain')
    childs = []

    parent = Bag(parent)
    if parent.name == 'shiny gold':
        target = parent
    if 'no other bags' in children:
        bags.append(parent)
        continue
    for child_str in children.split(','):
        count_str = child_str[1]
        child_name = child_str[2:].strip('bags').strip('.')
        parent.add_child(Child(count_str, child_name))
    if verbose:
        print(parent)
    bags.append(parent)

if target is None:
    raise LookupError('No target found')

possible_parents = []
still_adding = True
while_count = 0
while still_adding:
    still_adding = False
    for bag in bags:
        if bag not in possible_parents:
            for child_str in bag.children:
                if (((child_str in possible_parents) or (child_str == target))
                        and (bag not in possible_parents)):
                    possible_parents.append(bag)
                    still_adding = True
    while_count += 1
    if while_count >= 1000:
        still_adding = False

print(f'Part 1: {len(possible_parents)}, loop while_count: {while_count}')

child_count_loops = 0
child_count = target.count_children(bags)

print(f'Part 1: {child_count - 1}, loop count: {child_count_loops}')
