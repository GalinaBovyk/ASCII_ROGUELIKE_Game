#
#
#
#
from __future__ import annotations
import random
from typing import Iterator, List, Tuple, TYPE_CHECKING
import tcod

import entity_factories
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
        list_x = [self.x1+1 , self.x2 -1]
        list_y = [self.y1 +1, self.y2-1]
        side_x_hard = int(random.choice(list_x))
        side_y_hard = int(random.choice(list_y))
        side_x_soft = int(random.randint(self.x1+1 , self.x2-1 ))
        side_y_soft = int(random.randint(self.y1+1 , self.y2-1 ))
        list_choice =[side_x_hard, side_x_soft]
        final_choice = random.choice(list_choice)
        if final_choice == side_x_hard:
            return side_x_hard, side_y_soft
        else:
            return side_x_soft, side_y_hard

    def intersects(self, other: RectangularRoom) -> bool:
        return(
            self.x1-1 <= other.x2+2
            and self.x2+2 >= other.x1-1
            and self.y1-1 <= other.y2+2
            and self.y2+2 >= other.y1-1
        )

def place_entities(
    room: RectangularRoom, dungeon: GameMap, maximum_monsters: int,
) -> None:
    number_of_monsters = random.randint(0, maximum_monsters)

    for i in range(number_of_monsters):
        x = random.randint(room.x1 + 2, room.x2 - 2)
        y = random.randint(room.y1 + 2, room.y2 - 2)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random.random() < 0.5:
                entity_factories.small_evil_snake.spawn(dungeon, x, y)# small evil snake
            elif 0.5 < random.random() < 0.8:
                entity_factories.big_evil_snake.spawn(dungeon, x, y) # big evil snake
            elif  0.8 <= random.random() < 0.95:
                entity_factories.worm.spawn(dungeon, x, y) # worm
            elif 0.95 <= random.random():
                entity_factories.golden_duck.spawn(dungeon, x, y) # duck
            else:
                entity_factories.duck.spawn(dungeon, x, y) # golden duck
                       

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
    max_monsters_per_room: int,
    player: Entity,
) -> GameMap:

    dungeon = GameMap(map_width, map_height, entities=[player])
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
        types_used = []


        if len(rooms) == 0:
            player.x, player.y = new_room.center

        elif len(rooms) == 1:
            for x, y in tunnel_between (rooms[-1].side, new_room.side):
                if dungeon.tiles[x,y] == tile_types.floor:
                    types_used.append(tile_types.floor)
                    continue
                    
                elif dungeon.tiles[x,y] == tile_types.wall:
                    if types_used[-1] == tile_types.wall:
                        break
                    else:
                        dungeon.tiles[x,y] = tile_types.door
                        types_used.append(tile_types.wall)
                    

                else:
                    dungeon.tiles[x,y] = tile_types.tunnel
                    types_used.append(tile_types.tunnel)
        else:
            for x, y in tunnel_between (rooms[-1].side, new_room.side):
                if dungeon.tiles[x,y] == tile_types.floor:
                    types_used.append(tile_types.floor)
                    continue
                elif dungeon.tiles[x,y] == tile_types.wall:
                    if types_used[-1] == tile_types.wall:
                        break
                    else:
                        dungeon.tiles[x,y] = tile_types.door
                        types_used.append(tile_types.wall)
            

                else:
                    dungeon.tiles[x,y] = tile_types.tunnel
                    types_used.append(tile_types.tunnel)
                    
            for x, y in tunnel_between (random.choice(rooms).side, new_room.side):
                if dungeon.tiles[x,y] == tile_types.floor:
                    types_used.append(tile_types.floor)
                    continue
                elif dungeon.tiles[x,y] == tile_types.wall:
                    if types_used[-1] == tile_types.wall:
                        break
                    else:
                        dungeon.tiles[x,y] = tile_types.door
                        types_used.append(tile_types.wall)

                else:
                    dungeon.tiles[x,y] = tile_types.tunnel
                    types_used.append(tile_types.tunnel)

                
        place_entities(new_room, dungeon, max_monsters_per_room)

        rooms.append(new_room)

    return dungeon
        









    

