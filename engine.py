####################
# 
# Galina Bovykina
# November 16 2022
#
# This is a library of action the user or npc's
# can perform within the game.
# Code adopted from TStand90 rogueliketutorials.com
#
####################

from __future__ import annotations
import lzma
import pickle
from typing import TYPE_CHECKING
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
import color
import entity_factories 
import exceptions
from message_log import MessageLog
import render_functions

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld
    from input_handlers import EndgameEventHandler

    
# The engine connects the main visual and turn components of the game
class Engine:
    #  This determines how most of the events in the game happen
    game_map: GameMap
    game_world: GameWorld
    
    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.mouse_location = (0,0)
        self.player=player
        
    def handle_enemy_turns(self) -> None:
        #  Lets the ai determine it's actions like the player
        for entity in set(self.game_map.actors) - {self.player} :
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass
            
    def update_fov(self) -> None:
        #  Lights up an area of the map depending on its location
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        self.game_map.explored |= self.game_map.visible


        
    def render(self, console: Console) -> None:
        #  This is responsible for what happens on the screen
        self.game_map.render(console)
        #####  This part was specifically modified by me  #####
        #  it makes sure the game is finate by creating a boss room
        if self.game_world.current_floor <= self.game_world.total_floors:

            self.message_log.render(
                console=console,
                x= 21,
                y = 52,
                width=40,
                height=7,
            )

            render_functions.render_bar(
                console=console,
                current_value=self.player.fighter.hp,
                maximum_value=self.player.fighter.max_hp,
                total_width=20,
            )
            render_functions.render_dungeon_level(
                console=console,
                dungeon_level=self.game_world.current_floor,
                location=(0, 49),
            )

            render_functions.render_names_at_mouse_location(
                console=console, x=63, y=51, engine=self
            )
        elif self.game_world.current_floor -1 == self.game_world.total_floors:

            render_functions.boss_print(
                console=console
            )
            self.message_log.render(
                console=console,
                x=21, y=52,
                width=40,
                height=7,
            )

        else:
            pass

    def save_as(self, filename: str) -> None:
        #  This saves the game
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
        
