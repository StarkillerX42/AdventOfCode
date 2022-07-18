import click
import tqdm

import numpy as np

from typing import Tuple, List, Union
from pathlib import Path


def calculate_score(winner_hand):
    total = 0
    for i, val in enumerate(reversed(winner_hand)):
        total += (i + 1) * val
    return total


def combat(player_1, player_2):
    player_1 = player_1.copy()
    player_2 = player_2.copy()
    count = 0
    while len(player_1) != 0 and len(player_2) != 0 and count < 10000:
        if player_1[0] > player_2[0]:
            player_1.append(player_1.pop(0))
            player_1.append(player_2.pop(0))
        elif player_1[0] < player_2[0]:
            player_2.append(player_2.pop(0))
            player_2.append(player_1.pop(0))
        else:
            raise Exception("Equal value encountered!")
        count += 1

    if len(player_1) == 0:
        winner = player_2
    elif len(player_2) == 0:
        winner = player_1
    else:
        raise Exception("Game ended without a winner!")
    return winner


def recursive_combat_iter(player_1_history, player_2_history, verbose=False):
    player_1_history = player_1_history.copy()
    player_2_history = player_2_history.copy()
    if len(player_1_history[-1]) == 0 or len(player_2_history[-1]) == 0:
        return player_1_history[-1], player_2_history[-1]
    if (any([player_1_history[-1] == x for x in player_1_history[:-1]])
        or any([player_2_history[-1] == x for x in player_2_history[:-1]])):
        # print("Player 1 wins due to infinite loop!")
        return player_1_history[-1], []
    if (player_1_history[-1][0] <= len(player_1_history[-1]) - 1 and
        player_2_history[-1][0] <= len(player_2_history[-1]) - 1):
        if verbose >= 2:
            print(f"Entering Recursive combat with"
                  f" {player_1_history[-1][1:player_1_history[-1][0] + 1]}"
                  f" v {player_2_history[-1][1:player_2_history[-1][0] + 1]}")
        winner, outcome = recursive_combat(player_1_history[:-1]
                                           + [player_1_history[-1][
                                               1:player_1_history[-1][0] + 1]],
                                           player_2_history[:-1]
                                           + [player_2_history[-1][
                                               1:player_2_history[-1][0] + 1]],
                                           verbose)
        if verbose >= 2:
            print(f"Recursive combat won by {winner}")
        if winner == 1:
            return (player_1_history[-1][1:]
                    + [player_1_history[-1][0], player_2_history[-1][0]],
                    player_2_history[-1][1:])
        elif winner == 2:
            return (player_1_history[-1][1:], player_2_history[-1][1:]
                    + [player_2_history[-1][0],
                       player_1_history[-1][0]])
 
    else:
        if player_1_history[-1][0] > player_2_history[-1][0]:
            return (player_1_history[-1][1:]
                    + [player_1_history[-1][0], player_2_history[-1][0]],
                    player_2_history[-1][1:])
        elif player_2_history[-1][0] > player_1_history[-1][0]:
            return (player_1_history[-1][1:], player_2_history[-1][1:]
                    + [player_2_history[-1][0],
                       player_1_history[-1][0]])
        else:
            raise ValueError("Equality found, no valid procedure.")
    return [], []


def recursive_combat(player_1, player_2, verbose=False):
    player_1_history = player_1.copy()
    player_2_history = player_2.copy()
    count = 1
    if verbose:
        print(f"Round {count:.0f}, {player_1[-1]} - {player_2[-1]}")
    while (len(player_1_history[-1]) != 0
           and len(player_2_history[-1]) != 0
           and count < 10000):
        p1, p2 = recursive_combat_iter(player_1_history, player_2_history,
                                       verbose)
        player_1_history.append(p1)
        player_2_history.append(p2)
        count += 1
        if verbose:
            print(f"Round {count:.0f}, {p1} - {p2}")
    
    if len(player_1_history[-1]) == 0:
        return 2, player_2_history[-1]
    elif len(player_2_history[-1]) == 0:
        return 1, player_1_history[-1]
    else:
        raise ValueError("Winner not found in 1000 iterations")

@click.command()
@click.option("-v", "--verbose", count=True)
@click.option("-t", "--testing", is_flag=True)
def main(verbose=False, testing=False):
    date = __file__.split("day_")[-1].rstrip(".py")
    test_path = "_test" if testing else ""
    here = Path(__file__).parent.parent
    data_file = here / f"dat/day_{date}{test_path}.txt"
    player_1 = []
    player_2 = []
    with data_file.open('r') as fil:
        line = fil.readline().strip("\n")
        line = fil.readline().strip("\n")
        while line != "":
            player_1.append(int(line))
            line = fil.readline().strip("\n")
        line = fil.readline().strip("\n")
        line = fil.readline().strip("\n")
        while line != "":
            player_2.append(int(line))
            line = fil.readline().strip("\n")
    
    part_1_winner = combat(player_1, player_2)
    part_1 = calculate_score(part_1_winner)
    print(f"Part 1: {part_1}")

    winner, hand = recursive_combat([player_1], [player_2], verbose)
    if verbose:
        print(f"Player {winner} wins!")
    part_2 = calculate_score(hand)
    print(f"Part 2: {part_2}")
    
    
if __name__ == "__main__":
    main()

