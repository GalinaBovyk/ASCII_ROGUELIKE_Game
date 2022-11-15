#
#
#
#

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
#from input_handlers import MainGameEventHandler
from message_log import MessageLog
import render_functions

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld
    from input_handlers import EndgameEventHandler

class Engine:
    game_map: GameMap
    game_world: GameWorld
    
    def __init__(self, player: Actor):
#    def __init__(self, player: Actor, enemy_ss: Actor, enemy_bs: Actor, enemy_w: Actor, duck: Actor):
        #self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.mouse_location = (0,0)
        self.player = player
        
##        self.enemy_ss = enemy_ss
##        self.enemy_bs = enemy_bs
##        self.enemy_w = enemy_w
##        self.duck = duck
        


    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player} :
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass


            
    def update_fov(self) -> None:
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        self.game_map.explored |= self.game_map.visible


        
    def render(self, console: Console) -> None:
        self.game_map.render(console)
        if self.game_world.current_floor <= self.game_world.total_floors:
            #print(f"{self.game_world.current_floor} bleh bleb blebh {self.game_world.total_floors}")


            self.message_log.render(console=console, x= 21, y = 52, width=40, height=7)

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
            self.message_log.render(console=console, x=21, y=52, width=40, height=7)
            #self.message_log.add_message("As you descend to the bottom of the dungeon you see a looming figure of a huge Python... Monty's Python.", color.welcome_text)

        else:
            print(f"{self.game_world.current_floor} out of {self.game_world.total_floors}")
 #           render_functions.boss_print(
 #               console=console
 #           )



    def save_as(self, filename: str) -> None:
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
        



        
