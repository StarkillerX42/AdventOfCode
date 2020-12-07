import numpy as np

from pathlib import Path

tree_file = Path('../dat/day_3.txt')

trees_text = tree_file.open('r').read()
if trees_text[-1] == '\n':
    trees_text = trees_text[:-1]
lines = trees_text.split('\n')
arr = np.array([list(line) for line in lines])
print(arr)
trees = (arr == '#')

tree_hits = 0
loc = 0
for row in trees:
    if row[loc]:
        tree_hits += 1
    loc += 3
    if loc >= trees.shape[1]:
        loc -= trees.shape[1]

print(f'Part 1 hits: {tree_hits}\n')

print('Part 2')
print('Down 1')
prod = 1
for i in range(1, 8, 2):
    print(f'    Over {i}')
    tree_hits = 0
    loc = 0
    for row in trees:
        if row[loc]:
            tree_hits += 1
        loc += i
        if loc >= trees.shape[1]:
            loc -= trees.shape[1]
    prod *= tree_hits
    print(f'    Hit {tree_hits}')

print('Down 2')
print('    Over 2')
tree_hits = 0
loc = 0
for row in trees[::2]:
    if row[loc]:
        tree_hits += 1
    loc += 1
    if loc >= trees.shape[1]:
        loc -= trees.shape[1]
prod *= tree_hits
print(f'    Hit {tree_hits}')

print(f'Final product: {prod}')
