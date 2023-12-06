"""A place for tools that will be useful across Advent of Code
"""

import numpy as np


def neighbors_window_slice(i: int, j: int, arr: np.ndarray) -> list[list[int]]:
    """Given a center i and j, will produce a window of neighboring points

    Args:
        i (int): The first dimension
        j (int): The second dimension
        arr (np.ndarray): The array to slice

    Returns:
        np.ndarray: The sliced array returned
    """
    arr = np.array(arr)
    ilo = max(0, i - 1)
    ihi = min(i + 1, arr.shape[0])
    jlo = max(0, j - 1)
    jhi = min(j + 1, arr.shape[1])
    neighbors = arr[ilo : ihi + 1, jlo : jhi + 1]
    return neighbors
