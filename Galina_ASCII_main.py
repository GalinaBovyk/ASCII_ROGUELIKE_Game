#
#
#
##
import random
import copy
import traceback
import tcod 
import os
import sys
import glob
##from actions import EscapeAction, MovementAction
from engine import Engine
import entity_factories
from input_handlers import EventHandler
from procgen import generate_dungeon
import color



##
def launch() -> None:
    screen_width = 80
    screen_height = 55

    map_width = 80
    map_height = 50
    max_rooms = 30
    room_min_size = 5
    room_max_size = 17
    max_monsters_per_room = 2
    max_items_per_room = 2


    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32,8, tcod.tileset.CHARMAP_TCOD
        )
    

    player = copy.deepcopy(entity_factories.player)
    big_evil_snake = copy.deepcopy(entity_factories.big_evil_snake)
    duck = copy.deepcopy(entity_factories.duck)
    small_evil_snake = copy.deepcopy(entity_factories.small_evil_snake)
    worm = copy.deepcopy(entity_factories.worm)
    #engine = Engine(player=player,enemy_ss=small_evil_snake, enemy_bs=big_evil_snake, enemy_w=worm, duck=duck)
    engine = Engine(player=player)

    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        max_items_per_room=max_items_per_room,
        engine=engine,
    )
    engine.update_fov()
    #maybe actually print this before the map? after the map? do kind of like a NetHack moment?
    engine.message_log.add_message(
        "After sitting in Monty working on your Python script you finally passed out on your desk... only to suddenly wake up in a dungeon!", color.welcome_text
    )
    


    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title =" GALINA's ROGUELIKE SNAKE KILLING EXPERIMENT",
        vsync = True,
        ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)
            try:
                for event in tcod.event.wait():
                    context.convert_event(event)
                    engine.event_handler.handle_events(event)
            except Exception:
#                pass
                traceback.print_exc()
                engine.message_log.add_message(traceback.format_exc(), color.error)





if __name__ == "__main__":
    #random.seed(123)
    launch()
