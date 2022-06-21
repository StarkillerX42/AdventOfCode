import click
import tqdm

import numpy as np

from typing import Tuple, List, Union
from pathlib import Path


orientations = []
for i in range(8):
    x = bin(i)[2:]
    while len(x) < 3:
        x = '0' + x
    orientations.append(np.array(list(x)).astype(int))
orientations = np.array(orientations).astype(bool)


def display_image(image):
    for row in image:
        line = ""
        for x in row:
            if x:
                line += "\u25A0"
            else:
                line += "\u25A1"
        print(line)

def get_orientation(tile, transformation: iter):
    t = tile
    if transformation[0]:
        t = np.flipud(t)
    if transformation[1]:
        t = np.fliplr(t)
    if transformation[2]:
        t = np.rot90(t)
    return t


class Tile(object):
    def __init__(self, tile, tile_id):
        self.tile = np.array(tile)
        self.tile_id = tile_id
        self.orientation = np.array([0, 0, 0])
        self.coordinates = np.array([np.nan, np.nan])
        self.is_solved = False
    
    def set_solution(self, orientation, coordinates):
        self.orientation = orientation
        self.coordinates = coordinates
        self.is_solved = True
        
    def get_tile(self):
        return self.get_orientation(self.tile, self.orientation)
        
    def __eq__(self, val) -> bool:
        return val == self.tile_id
    
    def __str__(self) -> str:
        return str(self.tile)
    
    def get_orientation(self, transformation: iter):
        t = self.tile
        if transformation[0]:
            t = np.flipud(t)
        if transformation[1]:
            t = np.fliplr(t)
        if transformation[2]:
            t = np.rot90(t)

        return t
    
    def check_neighbor(self, tile_2: np.ndarray):
        tile_1 = self.get_orientation(self.orientation)
        if np.all(tile_1[0] == tile_2[-1]):
            return np.array((0, -1))
        elif np.all(tile_1[-1] == tile_2[0]):
            return np.array((0, 1))
        elif np.all(tile_1[:, 0] == tile_2[:, -1]):
            return np.array((-1, 0))
        elif np.all(tile_1[:, -1] == tile_2[:, 0]):
            return np.array((1, 0))
        else:
            return np.array((0, 0))   


class TileSet:
    # TODO Have an algorithm that will count how many sides of a tile are unique
    # and unmatchable. If there is one side, it is a side piece, if there are
    # two sides, they must be a corner.
    def __init__(self, tiles, solved_tiles: list,
                 verbose=0):
        self.tiles = tiles
        self.n_tiles = len(tiles)
        self.solved_tiles = solved_tiles
        self.verbose = verbose
        self.count_neighbors()
        self.corner_set = self.n_neighbors == 2
        self.edge_set = self.n_neighbors == 3
        self.middle_set = self.n_neighbors == 4
        # if verbose >= 1:
            # print(self.solution_map)
            # print(f"TileSet born of solution {is_solved.sum()}")
    
    def count_neighbors(self) -> np.ndarray:
        self.n_neighbors = np.zeros(self.n_tiles, dtype=int)
        for i, tile in tqdm.tqdm(enumerate(self), total=self.n_tiles):
            n = 0
            for j, tile_2 in enumerate(self):
                if i != j:
                    for orientation in orientations:
                        tmp_tile = tile_2.get_orientation(orientation)
                        neighbor = tile.check_neighbor(tmp_tile)
                        if np.any(neighbor):
                            n += 1
                            break
            self.n_neighbors[i] = n
        return self.n_neighbors

    def add_tile(self, tile, coordinates, orientation) -> None:
        coordinates = np.array(coordinates, dtype=int)
        orientation = np.array(orientation, dtype=bool)
        self.solved_tiles.append(tile)
        self.solved_tiles[-1].set_solution(orientation, coordinates)

    def __iter__(self):
        return iter(self.tiles)
    
    def __getitem__(self, x):
        return self.tiles[x]
    
    def __len__(self):
        return self.is_solved.sum()
    
    def get_limits(self):
        low_x = 0
        low_y = 0
        high_x = 0
        high_y = 0
        for tile in self.solved_tiles:
            low_x = min(tile.coordinates[0], low_x)
            low_y = min(tile.coordinates[1], low_y)
            high_x = max(tile.coordinates[0], high_x)
            high_y = max(tile.coordinates[1], high_y)
        
        return low_x, low_y, high_x, high_y
    
    def check_solution(self)-> Tuple[bool, bool]:
        """Returns two booleans, the first is whether or not it is a valid
        solution, and the second is whether or not you can create a solution. If
        the second is False, you should abandon it"""
        low_x, low_y, high_x, high_y = self.get_limits()
        if high_x - low_x >= np.sqrt(self.n_tiles):
            return False, False
        if high_y - low_y >= np.sqrt(self.n_tiles):
            return False, False
        if self.n_tiles != len(self.solved_tiles):
            return False, True
        for i, tile in enumerate(self.tiles):
            for j, tile_2 in enumerate(self.tiles):
                if i != j and tile.coordinates == tile_2.coordinates:
                    return False, False
        return True, True
    
    def check_tile_loc(self, location):
        """True if the location is a safe place to put a tile"""
        return np.all([np.any(location != x.coordinates)
                       for x in self.solved_tiles])
    
    def get_tile(self, tile_id):
        for tile in self:
            if tile.tile_id == tile_id:
                return tile
    
    def solve_perimeter(self):
        side_length = np.sqrt(self.n_tiles).astype(int)
        current_tiles = [self.solved_tiles[0],
                         self.solved_tiles[0]]
        for i in range(side_length - 2):
            for j, tile_1 in enumerate(current_tiles):
                if self.verbose >= 2:
                    print(f"Checking against: {tile_1.tile_id}")
                for k, tile_2 in enumerate(self):
                    if tile_2.is_solved or ~self.edge_set[k]:
                        continue
                    for orientation in orientations:
                        test_tile = tile_2.get_orientation(orientation)
                        neighbor = tile_1.check_neighbor(test_tile)
                        if np.any(neighbor):
                            if self.verbose >= 2:
                                print(f"Matched {tile_1.tile_id} with"
                                      f" {tile_2.tile_id}")
                            neighbor_coord = tile_1.coordinates + neighbor
                            if not self.check_tile_loc(neighbor_coord):
                                continue
                            elif (neighbor_coord[0] != 0
                                  and neighbor_coord[1] != 0):
                                continue
                            self.add_tile(tile_2, neighbor_coord, orientation)
                            current_tiles.pop(j)
                            current_tiles.append(tile_2)
                            break
        if self.verbose:
            self.display()
            print(f"Checking corners against {current_tiles[0].tile_id} and"
                  f" {current_tiles[1].tile_id}")
        for i in range(2):
            for j, tile_1 in enumerate(current_tiles):
                if self.verbose >= 2:
                    print(f"Checking against: {tile_1.tile_id}")
                for k, tile_2 in enumerate(self):
                    if tile_2.is_solved or ~self.corner_set[k]:
                        continue
                    for orientation in orientations:
                        test_tile = tile_2.get_orientation(orientation)
                        neighbor = tile_1.check_neighbor(test_tile)
                        if np.any(neighbor):
                            if self.verbose >= 2:
                                print(f"Matched {tile_1.tile_id} with"
                                      f" {tile_2.tile_id}")
                            neighbor_coord = (tile_1.coordinates + neighbor)
                            if not self.check_tile_loc(neighbor_coord):
                                continue
                            elif (neighbor_coord[0] != 0
                                  and neighbor_coord[1] != 0):
                                continue
                            self.add_tile(tile_2, neighbor_coord, orientation)
                            current_tiles.pop(j)
                            current_tiles.append(tile_2)
                            break
        minx, miny, maxx, maxy = self.get_limits()
        if self.verbose:
            self.display()
            print(f"Matching remaining sides against {current_tiles[0].tile_id}"
                  f" and {current_tiles[1].tile_id}")
        for i in range(side_length - 1):
            for j, tile_1 in enumerate(current_tiles):
                if self.verbose >= 2:
                    print(f"Checking against: {tile_1.tile_id}")
                for k, tile_2 in enumerate(self):
                    if tile_2.is_solved or ~self.edge_set[k]:
                        continue
                    for orientation in orientations:
                        test_tile = tile_2.get_orientation(orientation)
                        neighbor = tile_1.check_neighbor(test_tile)
                        if np.any(neighbor):
                            if self.verbose >= 2:
                                print(f"Matched {tile_1.tile_id} with"
                                      f" {tile_2.tile_id}")
                            neighbor_coord = tile_1.coordinates + neighbor
                            if not self.check_tile_loc(neighbor_coord):
                                continue
                            elif np.any(neighbor_coord == 0):
                                continue
                            self.add_tile(tile_2, neighbor_coord, orientation)
                            current_tiles.pop(j)
                            current_tiles.append(tile_2)
                            break
        corners = self.tiles[self.corner_set]
        for corner in corners:
            if corner in self.solved_tiles:
                continue
            for orientation in orientations:
                test_tile = corner.get_orientation(orientation)
                neighbor = current_tiles[0].check_neighbor(test_tile)
                if np.any(neighbor):
                    if self.verbose >= 2:
                        print(f"Matched final corner {corner.tile_id}")
                    neighbor_coord = current_tiles[0].coordinates + neighbor
                    if not self.check_tile_loc(neighbor_coord):
                        continue
                    elif np.any(neighbor_coord == 0):
                        continue
                    self.add_tile(corner, neighbor_coord, orientation)
                    return
    
    def get_neighbors(self, loc: np.ndarray):
        neighbors = []
        for i, ref in enumerate(self):
            if not ref.is_solved:
                continue
            if (loc - ref.coordinates).sum() == 1:
                neighbors.append(ref)
        return neighbors

    def solve_field(self):
        low_x, low_y, high_x, high_y = self.get_limits()
        for i in tqdm.tqdm(range(low_x, high_x)):
            for j in range(low_y, high_y):
                loc = np.array([i, j])
                if not self.check_tile_loc(loc):
                    continue
                for tile in self:
                    solved = False
                    if tile.is_solved:
                        continue
                    for orientation in orientations:
                        if solved:
                            continue
                        test_tile = tile.get_orientation(orientation)
                        neighbor_tiles = self.get_neighbors(loc)
                        if self.verbose >= 2:
                            print(f"Checking Tile {tile.tile_id} against\n"
                                  f"{neighbor_tiles}")
                        for neighbor in neighbor_tiles:
                            neighbor_rel = neighbor.check_neighbor(test_tile)
                            if np.any(neighbor_rel):
                                if np.all(neighbor.coordinates + neighbor_rel == loc):
                                    self.add_tile(tile, loc, orientation)
                                    solved = True
    
    def display(self):
        low_x, low_y, highx, highy = self.get_limits()
        grid = np.zeros((highx - low_x + 1, highy - low_y + 1))
        for i, tile in enumerate(self.solved_tiles):
            grid[tile.coordinates[0] - low_x,
                 tile.coordinates[1] - low_y] = tile.tile_id
        
        print(np.flipud(grid.T))
    
    def final_image(self):
        for tile in self:
            if not tile.is_solved:
                raise ValueError("Image grid is not fully solved, cannot image")
        low_x, low_y, highx, highy = self.get_limits()
        grid = np.zeros((highx - low_x + 1, highy - low_y + 1))
        image = np.zeros((np.sqrt(self.n_tiles).astype(int) * 8,
                          np.sqrt(self.n_tiles).astype(int) * 8), dtype=bool)
        for i, tile in enumerate(self.solved_tiles):
            grid[tile.coordinates[0] - low_x,
                 tile.coordinates[1] - low_y] = tile.tile_id
        for i, row in enumerate(grid):
            for j, tile_slot in enumerate(row):
                for tile in self:
                    if np.all(np.abs(tile.coordinates) == np.array([i, j])):
                        image[
                              j * 8: (j + 1) * 8,
                              i * 8: (i + 1) * 8] = np.flipud(tile.get_orientation(tile.orientation)[1: -1, 1: -1]) == "#"
        return image
        

@click.command()
@click.option("-v", "--verbose", count=True)
@click.option("-t", "--testing", is_flag=True)
def main(verbose=False, testing=False):
    date = __file__.split("day_")[-1].rstrip(".py")
    test_path = "_test" if testing else ""
    here = Path(__file__).parent.parent
    data_file = here / f"dat/day_{date}{test_path}.txt"

    tiles = []
    tile_ids = []
    tile = []
    with data_file.open('r') as fil:
        for line in fil:
            if "Tile" in line:
                num = int(line.split()[-1].rstrip(":\n"))
                if verbose >= 3:
                    print(f"Tile Number: {num}")
                tile_ids.append(num)
            elif line == "\n":
                if verbose >= 3:
                    print(f"Appending tile:\n{tile}")
                tiles.append(Tile(tile, num))
                tile = []
            else:
                tile.append(list(line.rstrip("\n")))
    tiles.append(Tile(tile, num))
    tiles = np.array(tiles)

    print(f"There are {len(tiles)} tiles")

    if verbose >= 3:
        print(tiles)
    if testing and verbose >= 2:
        # Check that each orientation is unique
        test_tile = tiles[0]
        for orient in orientations[1:]:
            new_tile = test_tile.get_orientation(orient)
            assert np.any(
                new_tile != test_tile), f"{test_tile}\n and\n {new_tile}\n"\
                    " match, which violates uniqueness!"

    tile_set = TileSet(tiles, [], verbose)
    part_1 = np.prod([t.tile_id for t in tile_set[tile_set.corner_set]])
    print(f"Part 1 {part_1}")
    tile_set.add_tile(tile_set[tile_set.corner_set][0], [0, 0], [0, 0, 0])
    if verbose:
        tile_set.display()
    tile_set.solve_perimeter()
    if verbose:
        tile_set.display()
    tile_set.solve_field()
    if verbose:
        tile_set.display()
    image = tile_set.final_image()
    if verbose:
        display_image(image)
    
    
    sea_monster_str = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
    
    sea_monster = [list(row) for row in sea_monster_str.splitlines()]
    sea_monster = np.array(sea_monster) == "#"
    
    
    part_2 = image.sum()
    for orientation in orientations:
        im = get_orientation(image, orientation)
        for i in range(im.shape[0] - sea_monster.shape[0] + 1):
            for j in range(im.shape[1] - sea_monster.shape[1] + 1):
                if np.all(im[i: i + sea_monster.shape[0],
                                j: j + sea_monster.shape[1]][sea_monster]):
                    if verbose:
                        print(f"Found sea monster at {i}, {j}")
                    im[i: i + sea_monster.shape[0],
                                j: j + sea_monster.shape[1]][sea_monster] = False
        part_2 = min(part_2, im.sum())
    print(f"Part 2: {part_2}")

    

if __name__ == "__main__":
    main()
