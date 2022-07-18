import click
import tqdm

import numpy as np
from pathlib import Path


def coord_from_directions(direction: str):
    ew_component = (direction.count("e") - direction.count("w")
         - direction.count("se") - direction.count("ne")
         + direction.count("nw") + direction.count("sw"))
    diag_component = 0
    curr_y = 0
    for diag in ["nw", "ne", "sw", "se"]:
        is_odd = curr_y % 2 == 1
        is_right = 'e' in diag
        if is_odd == is_right:
            movement = (direction.count(diag) + 1) // 2
        else:
            movement = direction.count(diag) // 2
        if 'e' in diag:
            diag_component += movement
        else:
            diag_component -= movement
        curr_y += direction.count(diag) if 's' in diag else -direction.count(diag)
    x = ew_component + diag_component
    y = direction.count("s") - direction.count("n")
    return (x, y)


def get_adjacent_tiles(loc: tuple):
    tiles = [(loc[0] - 1, loc[1]),
             (loc[0] + 1, loc[1]),
             (loc[0], loc[1] - 1),
             (loc[0], loc[1] + 1),
             (loc[0] + 1, loc[1] - 1) if loc[1] % 2 == 1
             else (loc[0] - 1, loc[1] - 1),
             (loc[0] + 1, loc[1] + 1) if loc[1] % 2 == 1
             else (loc[0] - 1, loc[1] + 1),
             ]
    return tiles


def visualize_state(tiles, verbose=0):
    # tiles = {(1, 0), (0, 1), (-1, 0), (-1, 1), (0, -1)}
    # tiles = {(1, 0), (-1, 0), (0, 1), (-1, 1), (0, -1), (-3, -2)}
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0
    for tile in tiles:
        minx = min(tile[0], minx)
        maxx = max(tile[0], maxx)
        miny = min(tile[1], miny)
        maxy = max(tile[1], maxy)
    # print(tiles)
    if verbose:
        print(f"{minx}-{maxx} x {miny}-{maxy}")
    array = np.zeros((maxx - minx + 1, (maxy - miny) + 1), dtype=str)
    array[:, :] = "\u25A0"
    for tile in tiles:
        array[tile[0] - minx, tile[1] - miny] = "\u25A1"
    if array[-minx, -miny] == "\u25A1":
        array[-minx, -miny] = "\u25A5"
    else:
        array[-minx, -miny] = "\u25A4"
    # array[0, 1 - miny] = "\u25A5"
    even_pad = "" if miny % 2 == 0 else "  "
    odd_pad = "  " if miny % 2 == 0 else ""
    for i, row in enumerate(array.T):
        if i % 2 == 0:
            print(even_pad + "   ".join(row))
        else:
            print(odd_pad + "   ".join(row))


def count_neighbors(loc: tuple, tiles: set):
    neighbors = 0
    for lo in get_adjacent_tiles(loc):
        if lo in tiles:
            neighbors += 1
    return neighbors


def new_day(tiles, verbose=False):
    new_tiles = set()
    for tile in tiles:
        neighbors = count_neighbors(tile, tiles)
        if verbose >= 2:
            print(f"    Tile {tile}, {neighbors} neighbors")
        if neighbors == 1 or neighbors == 2:
            new_tiles.add(tile)
            if verbose >= 2:
                print("        Survived")
        for neighbor in get_adjacent_tiles(tile):
            if (neighbor not in tiles
                and neighbor not in new_tiles
                and count_neighbors(neighbor, tiles) == 2):
                if verbose >= 2:
                    print(f"        New tile at {neighbor}")
                new_tiles.add(neighbor)
    return new_tiles


@click.command()
@click.option("-v", "--verbose", count=True)
@click.option("-t", "--testing", is_flag=True)
def main(verbose=False, testing=False):
    date = __file__.split("day_")[-1].rstrip(".py")
    test_path = "_test" if testing else ""
    here = Path(__file__).parent.parent
    data_file = here / f"dat/day_{date}{test_path}.txt"
    with data_file.open('r') as fil:
        directions = fil.readlines()
    print(f"Verbose: {verbose}, testing: {testing}")
    if verbose:
        print(f"There are {len(directions)} Tile Flips")
    flip_events = []

    for direction in directions:
        flip_events.append(coord_from_directions(direction))

    tile_flips = {}
    tiles = set()
    for location in flip_events:
        if flip_events.count(location) % 2 == 1:
            tiles.add(location)
        if location not in tile_flips.keys():
            tile_flips[location] = flip_events.count(location)
    if verbose:
        print(f"{len(tiles)} tiles were flipped")

    # tiles = {(2, -2), (0, -3), (-1, -1), (-1, -2), (0, 0), (-1, 1), (-2, 1), (0, 3), (2, 0), (-2, 0)}
    part_1 = len(tiles)
    print(f"Part 1: {part_1}")
    if verbose >= 1:
        visualize_state(tiles, verbose)

    for i in tqdm.tqdm(range(100)):
        if verbose >= 1:
            print(f"Day {i:3.0f}, {len(tiles):4.0f} tiles")
            if verbose >= 2:
                visualize_state(tiles, verbose)
        tiles = new_day(tiles, verbose)
    part_2 = len(tiles)
    print(f"Part 2: {part_2}")


if __name__ == "__main__":
    main()
