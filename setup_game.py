#
#
#
#

from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod

import color
from engine import Engine
import entity_factories
from game_map import GameWorld
import input_handlers
from procgen import generate_dungeon

background_image = tcod.image.load("color0_copy_9.png")[:,:,:3]

def new_game() -> Engine:
    
    screen_width = 80
    screen_height = 55

    map_width = 80
    map_height = 50
    max_rooms = 30
    room_min_size = 5
    room_max_size = 17

    total_floors = 5
    

    player = copy.deepcopy(entity_factories.player)
    big_evil_snake = copy.deepcopy(entity_factories.big_evil_snake)
    duck = copy.deepcopy(entity_factories.duck)
    small_evil_snake = copy.deepcopy(entity_factories.small_evil_snake)
    worm = copy.deepcopy(entity_factories.worm)
    #engine = Engine(player=player,enemy_ss=small_evil_snake, enemy_bs=big_evil_snake, enemy_w=worm, duck=duck)
    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        total_floors=total_floors
    
    )

    engine.game_world.total_dungeon()
    engine.update_fov()
    #maybe actually print this before the map? after the map? do kind of like a NetHack moment?
    engine.message_log.add_message(
        "After sitting in Monty working on your Python script you finally passed out on your desk... only to suddenly wake up in a dungeon!", color.welcome_text
    )

    #
    #
    # could technically start with equipment but its kinda lame
    ##
    
    return engine

def load_game(filename: str) -> Engine:
    with open(filename, "rb") as  f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine

class MainMenu(input_handlers.BaseEventHandler):

    def on_render(self, console: tcod.Console) -> None:
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width//2,
            console.height//2 - 5,
            "SNAKE STRANGELING EXPERIMENT",
            fg=color.menu_title,
            bg=color.black,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width//2,
            console.height -2,
            "By Galina Bovykina, Fall 2022 VSFX313, Individual Research, Prof. Gray Marshall",
            fg=color.menu_title,
            bg=color.black,
            alignment=tcod.CENTER,
        )
        menu_width = 24
        for i, text in enumerate(
            ["[N] Start a New Game", "[C] Continue last game", "[Q] Quit"]
        ):
            console.print(
                console.width//2,
                console.height//2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )
    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.K_n:
            return input_handlers.MainGameEventHandler(new_game())
        return None



    
