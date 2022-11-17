####################
# 
# Galina Bovykina
# November 16 2022
#
# This generates a dungeon floor or final boss room
# Code adopted from TStand90 rogueliketutorials.com
#
####################
from __future__ import annotations
import random
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING
import tcod
import numpy as np
import entity_factories
from game_map import GameMap
import tile_types

import tcod

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

#####  This part was specifically modified by me  #####
# Because my version has different difficulties - there are
# three different sets of item and monster distribution
# These will be edited with more playtesting

################################################################### EASY
max_items_by_floor_1 = [
    (1,1),
    (4,2),
    (8,3),
]

max_monsters_by_floor_1 = [
    (1,1),
    (2,2),
    (3,4),
    (4,5),
]

item_chances_1: Dict[int, List[Tuple[Entity, int]]] = {
    0: [
        (entity_factories.energy_drink, 40),
        (entity_factories.nice_note, 20),
        (entity_factories.meal_plan, 40),
        (entity_factories.stolen_chipotle, 20)
    ],
    2: [
        (entity_factories.deadline_list, 20),
        (entity_factories.complicated_math_equation, 20),
        (entity_factories.ink_bottle, 20),
        (entity_factories.parent_phone, 20),
        (entity_factories.magic_mood_ring, 20),
        (entity_factories.strength_mood_ring, 20),
        (entity_factories.armorclass_mood_ring, 20),
    ],
    3: [
        (entity_factories.stink_bomb, 20),
        (entity_factories.computer_mouse, 20),
        (entity_factories.face_mask, 20),
        (entity_factories.emergency_towel, 20),
        (entity_factories.wand, 20),
        (entity_factories.sunglasses, 20),
        (entity_factories.partyhat, 20),
    ],
    4: [
        (entity_factories.keyboard, 15),
        (entity_factories.hoodie, 15),
        (entity_factories.pepper_spray, 15),
        (entity_factories.platforms, 15),
        (entity_factories.costume, 15),
        (entity_factories.nerf_blaster, 15),
    ],
    8: [(entity_factories.the_one_ring, 10)],
}

enemy_chances_1: Dics[int, List[Tuple[Entity, int]]] ={
    1: [
        (entity_factories.small_evil_snake, 20),
        (entity_factories.spider, 60),
        (entity_factories.worm, 20),
    ],
    3: [
        (entity_factories.big_evil_snake, 30),
        (entity_factories.duck, 10),
        (entity_factories.golden_duck, 1),
    ],
    5: [(entity_factories.professor, 20), (entity_factories.anim_student, 20)],
    7: [(entity_factories.renderfarm_animal, 30)],
    9: [(entity_factories.paulla_wallace, 1)],
}

################################################################# MEDIUM
max_items_by_floor_2 = [
    (1,1),
    (3,2),
    (5,3),
    
]

max_monsters_by_floor_2 = [
    (1,2),
    (4,3),
    (6,5),
]

item_chances_2: Dict[int, List[Tuple[Entity, int]]] = {
    0: [
        (entity_factories.energy_drink, 20),
        (entity_factories.nice_note, 20),
        (entity_factories.meal_plan, 20),
        (entity_factories.stolen_chipotle, 20),
    ],
    2: [
        (entity_factories.deadline_list, 25),
        (entity_factories.complicated_math_equation, 25),
        (entity_factories.ink_bottle, 20),
        (entity_factories.parent_phone, 20),
        (entity_factories.magic_mood_ring, 20),
        (entity_factories.strength_mood_ring, 20),
        (entity_factories.armorclass_mood_ring, 20),
    ],
    4: [
        (entity_factories.stink_bomb, 25),
        (entity_factories.computer_mouse, 15),
        (entity_factories.face_mask, 15),
        (entity_factories.emergency_towel, 15),
        (entity_factories.wand, 15),
        (entity_factories.sunglasses, 15),
        (entity_factories.partyhat, 15),
    ],
    6: [
        (entity_factories.keyboard, 15),
        (entity_factories.hoodie, 15),
        (entity_factories.pepper_spray, 15),
        (entity_factories.platforms, 15),
        (entity_factories.costume, 15),
        (entity_factories.nerf_blaster, 15),
    ],
    8: [(entity_factories.the_one_ring, 1)],
}

enemy_chances_2: Dics[int, List[Tuple[Entity, int]]] ={
    1: [
        (entity_factories.small_evil_snake, 70),
        (entity_factories.big_evil_snake, 20),
        (entity_factories.spider, 30),
        (entity_factories.worm, 30),
    ],
    3: [
        (entity_factories.big_evil_snake, 30),
        (entity_factories.duck, 10),
        (entity_factories.golden_duck, 1),
    ],
    5: [(entity_factories.professor, 40), (entity_factories.anim_student, 40)],
    7: [(entity_factories.renderfarm_animal, 40)],
    9: [(entity_factories.paulla_wallace, 10)],
}

################################################################### HARD
max_items_by_floor_3 = [
    (1,1),
    (5,2),
]

max_monsters_by_floor_3 = [
    (1,2),
    (2,3),
    (4,5),
    (6,7),
]

item_chances_3: Dict[int, List[Tuple[Entity, int]]] = {
    0: [
        (entity_factories.energy_drink, 10),
        (entity_factories.nice_note, 10),
        (entity_factories.meal_plan, 10),
        (entity_factories.stolen_chipotle, 10),
    ],
    2: [
        (entity_factories.deadline_list, 15),
        (entity_factories.complicated_math_equation, 15),
        (entity_factories.ink_bottle, 15),
        (entity_factories.parent_phone, 15),
        (entity_factories.magic_mood_ring, 15),
        (entity_factories.strength_mood_ring, 15),
        (entity_factories.armorclass_mood_ring, 15),
    ],
    4: [
        (entity_factories.stink_bomb, 25),
        (entity_factories.computer_mouse, 15),
        (entity_factories.face_mask, 15),
        (entity_factories.emergency_towel, 15),
        (entity_factories.wand, 15),
        (entity_factories.sunglasses, 15),
        (entity_factories.partyhat, 15),
    ],
    6: [
        (entity_factories.keyboard, 10),
        (entity_factories.hoodie, 10),
        (entity_factories.pepper_spray, 10),
        (entity_factories.platforms, 10),
        (entity_factories.costume, 10),
        (entity_factories.nerf_blaster, 10),
    ],
    8: [(entity_factories.the_one_ring, 1)],
}

enemy_chances_3: Dics[int, List[Tuple[Entity, int]]] ={
    1: [
        (entity_factories.small_evil_snake, 70),
        (entity_factories.big_evil_snake, 40),
        (entity_factories.spider, 20),
        (entity_factories.worm, 20),
    ],
    3: [
        (entity_factories.big_evil_snake, 40),
        (entity_factories.duck, 10),
        (entity_factories.golden_duck, 1),
    ],
    4: [(entity_factories.professor, 50), (entity_factories.anim_student, 50)],
    5: [(entity_factories.renderfarm_animal, 50)],
    9: [(entity_factories.paulla_wallace, 20)],
}


# This uses the previous lists the create a weighted chance of spawning
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
                

# This is a class that creates a room, ready to be placed into the game
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

    #####  This part was specifically modified by me  #####
    #  I added an outer layer to create walls as a seperate tile
    @property
    def outer(self) -> Tuple[slice,slice]:
        return slice(self.x1, self.x2+1), slice(self.y1, self.y2 +1)

    #  For my extra type of tunnels I created a random side choice
    #  for a new way to conncect rooms
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
    room: RectangularRoom,
    dungeon: GameMap,
    floor_number: int,
    difficulty: int,
) -> None:
    #####  This part was specifically modified by me  #####
    #  These pull from different lists to place entities
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

            if not any(entity.x == x and entity.y == y
                       for entity in dungeon.entities):
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

            if not any(entity.x == x and entity.y == y
                       for entity in dungeon.entities):
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

            if not any(entity.x == x and entity.y == y
                       for entity in dungeon.entities):
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


# This makes rooms and connects them with corridors
# as well as putting entities throughout
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

        #####  This part was specifically modified by me  #####
        #  Besides creating more tunnes and different types of tunnes
        #  (from side or from center) this also tracks what tiles it
        #  is replacing and acts accoringly
        elif len(rooms) == 1:
            for x, y in tunnel_between (rooms[-1].center, new_room.center):
                #  It will make the floor types stays floors
                if dungeon.tiles[x,y] == tile_types.floor:
                    dungeon.tiles[x,y] == tile_types.floor
                    types_used.append(tile_types.floor)
                    continue
                #  If the tile type is wall it will check if
                #  the previous floor type was wall as well
                #  and will break
                #  This prevents from walls that are made out of doors
                elif dungeon.tiles[x,y] == tile_types.wall:
                    if types_used[-1] == tile_types.wall:
                        break
                    #  if the previous tile is not wall it will make a door
                    else:
                        dungeon.tiles[x,y] = tile_types.door
                        #  and in 60% it will also make it a closed door
                        #  by spawning a closed door entity
                        if random.random() < 0.6:
                            entity_factories.closed_door.spawn(dungeon, x, y)
                        types_used.append(tile_types.wall)
                    
                #  And if the tile type is tunnel it will keep it
                else:
                    dungeon.tiles[x,y] = tile_types.tunnel
                    types_used.append(tile_types.tunnel)
            #  This logic proceeds to generate at least two tunnes from
            #  each room - one from center and one from side
                    
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

        #  This drops entities, places stairs and adds the room to list        
        place_entities(
            new_room,
            dungeon,
            engine.game_world.current_floor,
            difficulty,
        )
        dungeon.tiles[center_of_last_room] = tile_types.down_stairs
        dungeon.downstairs_location = center_of_last_room

        rooms.append(new_room)

    return dungeon


# This sets up the boss room
def boss_room(
        map_width: int,
        map_height: int,
        engine: Engine,
) -> GameMap:
    player = engine.player

    dungeon = GameMap(engine, map_width, map_height, entities=[player])
    dungeon.tiles = np.full(
        (map_width, map_height),
        fill_value=tile_types.nice_space,
        order="F",
    )
    dungeon.tiles[39,26:48] = tile_types.tunnel
    player.place(x=39,y=48)
    entity_factories.epilouge.spawn(dungeon, 39, 27)
    return dungeon
