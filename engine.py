#
#
#
#

from __future__ import annotations
from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov




from input_handlers import MainGameEventHandler

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler

class Engine:
    game_map: GameMap
    
    def __init__(self, player: Actor, enemy_ss: Actor, enemy_bs: Actor, enemy_w: Actor, duck: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.player = player
        self.enemy_ss = enemy_ss
        self.enemy_bs = enemy_bs
        self.enemy_w = enemy_w
        self.duck = duck


    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player} :
            if entity.ai:
                entity.ai.perform()

            
    def update_fov(self) -> None:
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        self.game_map.explored |= self.game_map.visible

##    def update_fov_bs(self) -> None:
##        self.game_map.visible[:] = compute_fov(
##            self.game_map.tiles["transparent"],
##            (self.enemy_bs.x, self.enemy_bs.y),
##            radius=8,
##        )
##        self.game_map.explored |= self.game_map.visible
##
##    def update_fov_duck(self) -> None:
##        self.game_map.visible[:] = compute_fov(
##            self.game_map.tiles["transparent"],
##            (self.enemy_duck.x, self.enemy_duck.y),
##            radius=8,
##        )
##        self.game_map.explored |= self.game_map.visible

        
    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        console.print(
            x=1,
            y=53,
            string=f"HP:{self.player.fighter.hp}/{self.player.fighter.max_hp}",
        )
            


        context.present(console)

        console.clear()
