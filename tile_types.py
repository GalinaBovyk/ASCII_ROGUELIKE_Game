#
#
#

from typing import Tuple

import numpy as np

graphic_dt = np.dtype(
    [
        ("ch", np.int32),
        ("fg", "3B"),
        ("bg", "3B"),
    ]
)

tile_dt = np.dtype(
    [
        ("walkable", np.bool),
        ("transparent", np.bool),
        ("dark", graphic_dt),
        ("light", graphic_dt),
    ]
)

def new_tile(
    *,
    walkable:int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int,int,int], Tuple[int,int,int]],
) -> np.ndarray:
    return np.array((walkable, transparent,dark, light), dtype=tile_dt)

SHROUD = np.array((ord(" "), (255,255,255), (0,0,0)), dtype=graphic_dt)

space = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "),(0, 0, 0),(0, 0, 0)),
    light=(ord(" "),(0, 0, 0),(0, 0, 0)),
)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("."),(100, 100, 100),(0, 0, 0)),
    light=(ord("."),(166, 166, 166),(0, 0, 0))
)

tunnel = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("#"),(50, 50, 50),(0, 0, 0)),
    light=(ord("."),(166, 166, 166),(0, 0, 0))
)

door = new_tile(
    walkable=True,
    transparent=False,
    dark=(ord("D"),(41, 30, 14),(0, 0, 0)),
    light=(ord("D"),(120, 87, 42),(0, 0, 0)),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("X"), (166,166,166), (20,20,20)),
    light=(ord("X"), (255,255,255), (20,20,20))
)

down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(">"), (135, 132, 123), (0,0,0)),
    light=(ord(">"), (135, 132, 123), (0,0,0))
)

nice_space = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord(" "),(0, 0, 0),(0, 0, 0)),
    light=(ord(" "),(0, 0, 0),(0, 0, 0)),
)
