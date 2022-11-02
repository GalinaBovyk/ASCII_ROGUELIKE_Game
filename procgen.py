#
#
#
#
from __future__ import annotations
import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from entity import Entity



import tcod

class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 =y + height

    @property
    def center(self) -> Tuple[int,int]:
        center_x = int((self.x1 + self.x2)/2)
        center_y = int((self.y1 + self.y2)/2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice,slice]:
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    @property
    def outer(self) -> Tuple[slice,slice]:
        return slice(self.x1, self.x2+1), slice(self.y1, self.y2 +1)

    @property
    def side(self) -> Tuple[int,int]:
        list_x = [self.x1 +1, self.x2 -1]
        list_y = [self.y1 +1, self.y2-1]
        side_x_hard = int(random.choice(list_x))
        side_y_hard = int(random.choice(list_y))
        side_x_soft = int(random.randint(self.x1 + 2, self.x2 -2))
        side_y_soft = int(random.randint(self.y1 + 2, self.y2 -2))
        list_choice =[side_x_hard, side_x_soft]
        final_choice = random.choice(list_choice)
        if final_choice == side_x_hard:
            return side_x_hard, side_y_soft
        else:
            return side_x_soft, side_y_hard

    def intersects(self, other: RectangularRoom) -> bool:
        return(
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

def tunnel_between(
    start: Tuple[int,int], end: Tuple[int,int]
) -> Iterator[Tuple[int,int]]:

    x1,y1 = start
    x2, y2 = end
    if random.random() < 0.5:
        corner_x, corner_y = x2, y1
    else:
        corner_x, corner_y = x1,y2
    for x,y in tcod.los.bresenham((x1,y1), (corner_x, corner_y)).tolist():
        yield x,y
    for x,y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x,y

def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    player: Entity,
) -> GameMap:

    dungeon = GameMap(map_width, map_height)
    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x,y, room_width, room_height)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue
        dungeon.tiles[new_room.outer] = tile_types.wall
        dungeon.tiles[new_room.inner] = tile_types.floor


        if len(rooms) == 0:
            player.x, player.y = new_room.center

        elif len(rooms) == 1:
            for x, y in tunnel_between (rooms[-1].side, new_room.side):
                if dungeon.tiles[x,y] == tile_types.floor:
                    continue
                elif dungeon.tiles[x,y] == tile_types.wall:
                    dungeon.tiles[x,y] = tile_types.door

                else:
                    dungeon.tiles[x,y] = tile_types.tunnel
        else:
            for x, y in tunnel_between (rooms[-1].side, new_room.side):
                if dungeon.tiles[x,y] == tile_types.floor:
                    continue
                elif dungeon.tiles[x,y] == tile_types.wall:
                    dungeon.tiles[x,y] = tile_types.door

                else:
                    dungeon.tiles[x,y] = tile_types.tunnel
                    
            for x, y in tunnel_between (rooms[-2].side, new_room.side):
                if dungeon.tiles[x,y] == tile_types.floor:
                    continue
                elif dungeon.tiles[x,y] == tile_types.wall:
                    dungeon.tiles[x,y] = tile_types.door

                else:
                    dungeon.tiles[x,y] = tile_types.tunnel
                
                

        dungeon.tiles[new_room.inner] = tile_types.floor

        rooms.append(new_room)

    return dungeon
        









    

