import click
import tqdm

from pathlib import Path
from numba import njit
import time

# @njit
def keygen(subject_num: int, loops: int) -> int:
    multiplier = subject_num
    for _ in range(loops):
        subject_num *= multiplier
        subject_num %= 20201227
    return subject_num


# @njit
def brute_force_loops(pub_key: int) -> int:
    card_loops = 0
    limit = 100000000
    multiplier = 7
    subject_number = 7
    while subject_number != pub_key and card_loops < limit:
        card_loops += 1
        subject_number *= multiplier
        subject_number %= 20201227
        # card_key_test = keygen(subject_number, card_loops)
    if card_loops == limit:
        card_loops = -1
    return card_loops


@click.command()
@click.option("-v", "--verbose", count=True)
@click.option("-t", "--testing", is_flag=True)
def main(verbose=False, testing=False):
    date = __file__.split("day_")[-1].rstrip(".py")
    
    if testing:
        card_pub_key = 5764801
        door_pub_key = 17807724
    else:
        card_pub_key = 19774466
        door_pub_key = 7290641
    
    start = time.time()
    card_loops = brute_force_loops(card_pub_key)
    door_loops = brute_force_loops(door_pub_key)
    end = time.time()
    
    if verbose >= 1:
        print(f"Completed in {end - start}")
        print(f"Card Loops: {card_loops}, Door Loops: {door_loops}")
    
    private_key_1 = keygen(door_pub_key, card_loops)
    private_key_2 = keygen(card_pub_key, door_loops)

    if private_key_1 == private_key_2:
        part_1 = private_key_1
    else:
        raise KeyError("Encryption keys do not match")
    print(f"Part 1: {part_1}")


if __name__ == "__main__":
    main()
