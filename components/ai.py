#
#
#
#

from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

import numpy as np
import tcod

from actions import Action, MeleeAction, MovementAction, WaitAction


if TYPE_CHECKING:
    from entity import Actor

class BaseAI(Action):
    entity: Actor
    
    def perform(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int,int]]:
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            if entity.blocks_movement and cost[entity.x, entity.y]:
                cost[entity.x, entity.y] += 10

        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))

        path: List[List[int]] = pathfinder.path_to((dest_x,dest_y))[1:].tolist()

        return [(index[0], index[1]) for index in path]


# here is where I would create a different type of ai
class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int,int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
            ).perform()

        return WaitAction(self.entity).perform()


class SnakeEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int,int]] = []

    def perform(self) -> None:
        target = self.engine.player
#        target = self.engine.game_map.entities.GameMap.actors.small_evil_snake
#        target = self.engine.game_map.actors(small_evil_snake)
#        target = self.engine.game_map.dungeon.entities.small_evil_snake
        
 #       print(f"i cat, my target is {target}")
        
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))
        #print(f"its at {target.x} and {target.y} away")

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
     #       print(f"{distance}")
            if distance <= 1:
                #print("i hunger")
                return MeleeAction(self.entity, dx, dy).perform()

            self.path = self.get_path_to(target.x, target.y)
      #      print(f"i am gonna slither to {self.path}")

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
            ).perform()

        return WaitAction(self.entity).perform()

class WormEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int,int]] = []

    def perform(self) -> None:
        target = self.engine.enemy_w
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
            ).perform()

        return WaitAction(self.entity).perform()

class ClosedDoor(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int,int]] = []

    def perform(self) -> None:
        return WaitAction(self.entity).perform()

















    
