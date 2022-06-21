import click
import tqdm

import numpy as np

from typing import Tuple, List, Union
from pathlib import Path

@click.command()
@click.option("-v", "--verbose", count=True)
@click.option("-t", "--testing", is_flag=True)
def main(verbose=False, testing=False):
    date = __file__.split("day_")[-1].rstrip(".py")
    test_path = "_test" if testing else ""
    here = Path(__file__).parent.parent
    data_file = here / f"dat/day_{date}{test_path}.txt"

    allergens_2d = []
    allergens = set()
    ingredients_2d = []
    ingredients = set()
    with data_file.open('r') as fil:
        for line in fil:
            left, right = line.split(" (contains ")
            ingredients_2d.append(left.split())
            allergens_2d.append(right[:-2].split(", "))
    
    allergies = {}
    ingredients = set()
    for ings, als in zip(ingredients_2d, allergens_2d):  # Popuplate allergy candidates
        for al in als:
            if al not in allergies.keys():
                allergies[al] = set()
            for ing in ings:
                allergies[al].add(ing)
                ingredients.add(ing)
    
    for ings, als in zip(ingredients_2d, allergens_2d):
        for al, ingds in allergies.items():
            if al in als:
                for ing in ingds.copy():
                    if ing not in ings:
                        allergies[al].remove(ing)
    
    hypo_allergenic = set()  # Populate hypo-allergenic ingredients
    for ing in ingredients:
        not_in = True
        for al, ings in allergies.items():
            if ing in ings:
                not_in = False
        if not_in:
            hypo_allergenic.add(ing)
        
        
    if verbose:
        print(f"Hypo-allergenic ingredients include"
              f" {', '.join(hypo_allergenic)}")
    
    part_1 = 0
    for ings in ingredients_2d:
        for ing in ings:
            if ing in hypo_allergenic:
                part_1 += 1
    print(f"Part 1: {part_1}")
    
    for _ in range(len(allergies) - 1):
        for al, ings in allergies.items():
            if len(ings) == 1:
                for al_2, ings_2 in allergies.items():
                    if al != al_2:
                        for ing in ings:
                            if ing in ings_2.copy():
                                ings_2.remove(ing)
    if verbose:
        print(allergies)

    part_2_list = []
    for al in sorted(allergies.keys()):
        if len(allergies[al]) > 1:
            raise Exception("Not finished yet!")
        for x in allergies[al]:
            part_2_list.append(x)
    
    part_2 = ",".join(part_2_list)
    print(f"Part 2: {part_2}")
    
    
if __name__ == "__main__":
    main()
    