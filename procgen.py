#
#
#
#
from __future__ import annotations
import random
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING
import tcod

import entity_factories
from game_map import GameMap
import tile_types

import tcod

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
#################################### easy difficulty
max_items_by_floor_1 = [
    (1,1),
    (4,2),
]

max_monsters_by_floor_1 = [
    (1,2),
    (4,3),
    (6,5),
]

item_chances_1: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.energy_drink, 40), (entity_factories.nice_note, 20), (entity_factories.mood_ring, 40)],
    2: [(entity_factories.deadline_list, 90), (entity_factories.complicated_math_equation, 90)],
    4: [(entity_factories.stink_bomb, 90), (entity_factories.computer_mouse, 15),(entity_factories.face_mask, 15)],
    6: [(entity_factories.keyboard, 15), (entity_factories.hoodie, 15)],
    8: [(entity_factories.the_one_ring, 1)],
}

enemy_chances_1: Dics[int, List[Tuple[Entity, int]]] ={
    1: [(entity_factories.small_evil_snake, 40),(entity_factories.big_evil_snake, 70)],
    3: [((entity_factories.big_evil_snake, 30))],
    5: [((entity_factories.worm, 20))],
    7: [((entity_factories.duck, 20))],
    9: [((entity_factories.golden_duck, 1))],
}

#################################### medium difficulty
max_items_by_floor_2 = [
    (1,0),
    (4,2),
]

max_monsters_by_floor_2 = [
    (1,0),
    (4,3),
    (6,5),
]

item_chances_2: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.energy_drink, 40), (entity_factories.nice_note, 20), (entity_factories.mood_ring, 40)],
    2: [(entity_factories.deadline_list, 90), (entity_factories.complicated_math_equation, 90)],
    4: [(entity_factories.stink_bomb, 90), (entity_factories.computer_mouse, 15),(entity_factories.face_mask, 15)],
    6: [(entity_factories.keyboard, 15), (entity_factories.hoodie, 15)],
    8: [(entity_factories.the_one_ring, 1)],
}

enemy_chances_2: Dics[int, List[Tuple[Entity, int]]] ={
    1: [(entity_factories.small_evil_snake, 40),(entity_factories.big_evil_snake, 70)],
    3: [((entity_factories.big_evil_snake, 30))],
    5: [((entity_factories.worm, 20))],
    7: [((entity_factories.duck, 20))],
    9: [((entity_factories.golden_duck, 1))],
}

#################################### hard difficulty
max_items_by_floor_3 = [
    (1,1),
    (4,2),
]

max_monsters_by_floor_3 = [
    (1,2),
    (4,3),
    (6,5),
]

item_chances_3: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.energy_drink, 40), (entity_factories.nice_note, 20), (entity_factories.mood_ring, 40)],
    2: [(entity_factories.deadline_list, 90), (entity_factories.complicated_math_equation, 90)],
    4: [(entity_factories.stink_bomb, 90), (entity_factories.computer_mouse, 15),(entity_factories.face_mask, 15)],
    6: [(entity_factories.keyboard, 15), (entity_factories.hoodie, 15)],
    8: [(entity_factories.the_one_ring, 1)],
}

enemy_chances_3: Dics[int, List[Tuple[Entity, int]]] ={
    1: [(entity_factories.small_evil_snake, 40),(entity_factories.big_evil_snake, 70)],
    3: [((entity_factories.big_evil_snake, 30))],
    5: [((entity_factories.worm, 20))],
    7: [((entity_factories.duck, 20))],
    9: [((entity_factories.golden_duck, 1))],
}

def get_max_value_for_floor(
    weighted_chances_by_floor: List[Tuple[int, int]], floor: int
) -> int:
    current_value = 0

    for floor_minimum, value in weighted_chances_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value
    return current_value

def get_entities_at_random(
    weighted_chances_by_floor: Dict[int, List[Tuple[Entity,int]]],
    number_of_entities: int,
    floor: int,
) -> List[Entity]:
    entity_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]

                entity_weighted_chances[entity] = weighted_chance

    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_values = list(entity_weighted_chances.values())

    chosen_entities = random.choices(
        entities, weights=entity_weighted_chance_values, k=number_of_entities
    )

    return chosen_entities
                





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

#maybe try doing console draw frame instead of doing the X tiles?
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
    room: RectangularRoom, dungeon: GameMap, floor_number: int, difficulty: int) -> None:
    if difficulty == 1:
        number_of_monsters = random.randint(
            0, get_max_value_for_floor(max_monsters_by_floor_1, floor_number)
        )
        number_of_items = random.randint(
            0, get_max_value_for_floor(max_items_by_floor_1, floor_number)
        )
        monsters: List[Entity] = get_entities_at_random(
            enemy_chances_1, number_of_monsters, floor_number
        )
        items: List[Entity] = get_entities_at_random(
            item_chances_1, number_of_items, floor_number
        )
        for entity in monsters + items:
            x = random.randint(room.x1 + 2, room.x2 - 2)
            y = random.randint(room.y1 + 2, room.y2 - 2)
            item_chance = random.random()

            if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
                entity.spawn(dungeon, x,y)
    elif difficulty == 2:
        number_of_monsters = random.randint(
            0, get_max_value_for_floor(max_monsters_by_floor_2, floor_number)
        )
        number_of_items = random.randint(
            0, get_max_value_for_floor(max_items_by_floor_2, floor_number)
        )
        monsters: List[Entity] = get_entities_at_random(
            enemy_chances_2, number_of_monsters, floor_number
        )
        items: List[Entity] = get_entities_at_random(
            item_chances_2, number_of_items, floor_number
        )
        for entity in monsters + items:
            x = random.randint(room.x1 + 2, room.x2 - 2)
            y = random.randint(room.y1 + 2, room.y2 - 2)
            item_chance = random.random()

            if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
                entity.spawn(dungeon, x,y)
    else:
        number_of_monsters = random.randint(
            0, get_max_value_for_floor(max_monsters_by_floor_3, floor_number)
        )
        number_of_items = random.randint(
            0, get_max_value_for_floor(max_items_by_floor_3, floor_number)
        )
        monsters: List[Entity] = get_entities_at_random(
            enemy_chances_3, number_of_monsters, floor_number
        )
        items: List[Entity] = get_entities_at_random(
            item_chances_3, number_of_items, floor_number
        )
        for entity in monsters + items:
            x = random.randint(room.x1 + 2, room.x2 - 2)
            y = random.randint(room.y1 + 2, room.y2 - 2)
            item_chance = random.random()

            if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
                entity.spawn(dungeon, x,y)
                   
                       

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
    difficulty: int,
    engine: Engine,
) -> GameMap:
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])
    rooms: List[RectangularRoom] = []

    center_of_last_room = (0,0)

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
            player.place(*new_room.center, dungeon)

        elif len(rooms) == 1:
            for x, y in tunnel_between (rooms[-1].center, new_room.center):
                if dungeon.tiles[x,y] == tile_types.floor:
                    dungeon.tiles[x,y] == tile_types.floor
                    types_used.append(tile_types.floor)
                    continue
                    
                elif dungeon.tiles[x,y] == tile_types.wall:
                    if types_used[-1] == tile_types.wall:
                        break
                    else:
                        dungeon.tiles[x,y] = tile_types.door
                        if random.random() < 0.6:
                            entity_factories.closed_door.spawn(dungeon, x, y)
                        types_used.append(tile_types.wall)
                    

                else:
                    dungeon.tiles[x,y] = tile_types.tunnel
                    types_used.append(tile_types.tunnel)
                    
            for x, y in tunnel_between (rooms[-1].side, new_room.side):
                if dungeon.tiles[x,y] == tile_types.floor:
                    dungeon.tiles[x,y] == tile_types.floor
                    types_used.append(tile_types.floor)
                    continue
                    
                elif dungeon.tiles[x,y] == tile_types.wall:
                    if types_used[-1] == tile_types.wall:
                        break
                    else:
                        dungeon.tiles[x,y] = tile_types.door
                        if random.random() < 0.6:
                            entity_factories.closed_door.spawn(dungeon, x, y)
                        types_used.append(tile_types.wall)
                else:
                    dungeon.tiles[x,y] = tile_types.tunnel
                    types_used.append(tile_types.tunnel)


                    
        else:
            for x, y in tunnel_between (rooms[-1].center, new_room.center):
                if dungeon.tiles[x,y] == tile_types.floor:
                    dungeon.tiles[x,y] == tile_types.floor
                    types_used.append(tile_types.floor)
                    continue
                elif dungeon.tiles[x,y] == tile_types.wall:
                    if types_used[-1] == tile_types.wall:
                        break
                    else:
                        dungeon.tiles[x,y] = tile_types.door
                        if random.random() < 0.6:
                            entity_factories.closed_door.spawn(dungeon, x, y)
                        types_used.append(tile_types.wall)
            

                else:
                    dungeon.tiles[x,y] = tile_types.tunnel
                    types_used.append(tile_types.tunnel)
            center_of_last_room = new_room.center
                    
            for x, y in tunnel_between (random.choice(rooms).side, new_room.side):
                if dungeon.tiles[x,y] == tile_types.floor:
                    dungeon.tiles[x,y] == tile_types.floor
                    types_used.append(tile_types.floor)
                    continue
                elif dungeon.tiles[x,y] == tile_types.wall:
                    if types_used[-1] == tile_types.wall:
                        break
                    else:
                        dungeon.tiles[x,y] = tile_types.door
                        if random.random() < 0.6:
                            entity_factories.closed_door.spawn(dungeon, x, y)
                        types_used.append(tile_types.wall)

                else:
                    dungeon.tiles[x,y] = tile_types.tunnel
                    types_used.append(tile_types.tunnel)
            center_of_last_room = new_room.center

                
        place_entities(new_room, dungeon, engine.game_world.current_floor, difficulty)
        dungeon.tiles[center_of_last_room] = tile_types.down_stairs
        dungeon.downstairs_location = center_of_last_room

        rooms.append(new_room)

    return dungeon



####################### my precious little safe

##    for i in range(number_of_monsters):
##        x = random.randint(room.x1 + 2, room.x2 - 2)
##        y = random.randint(room.y1 + 2, room.y2 - 2)
##
##        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
##            if random.random() < 0.5:
##                entity_factories.small_evil_snake.spawn(dungeon, x, y)# small evil snake
##            elif 0.5 < random.random() < 0.8:
##                entity_factories.big_evil_snake.spawn(dungeon, x, y) # big evil snake
##            elif  0.8 <= random.random() < 0.95:
##                entity_factories.worm.spawn(dungeon, x, y) # worm
##            elif 0.95 <= random.random():
##                entity_factories.golden_duck.spawn(dungeon, x, y) # duck
##            else:
##                entity_factories.duck.spawn(dungeon, x, y) # golden duck
    
#    for i in range(number_of_items):

##            if item_chance < 0.4:
##                entity_factories.energy_drink.spawn(dungeon, x, y)
##            elif 0.4< item_chance < 0.5:
##                entity_factories.deadline_list.spawn(dungeon, x, y)
##            elif 0.5< item_chance < 0.6:
##                entity_factories.complicated_math_equation.spawn(dungeon, x, y)
##            elif 0.6< item_chance < 0.7:
##                entity_factories.stink_bomb.spawn(dungeon, x, y)
##                
##            else:
##                entity_factories.nice_note.spawn(dungeon, x, y)



##    number_of_monsters = random.randint(
##        0, get_max_value_for_floor(max_monsters_by_floor_1, floor_number)
##    )
##    number_of_items = random.randint(
##        0, get_max_value_for_floor(max_items_by_floor_1, floor_number)
##    )
##    monsters: List[Entity] = get_entities_at_random(
##        enemy_chances_1, number_of_monsters, floor_number
##    )
##    items: List[Entity] = get_entities_at_random(
##        item_chances_1, number_of_items, floor_number
##    )
##    for entity in monsters + items:
##        x = random.randint(room.x1 + 2, room.x2 - 2)
##        y = random.randint(room.y1 + 2, room.y2 - 2)
##        item_chance = random.random()
##
##        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
##            entity.spawn(dungeon, x,y)
##            
        





    

