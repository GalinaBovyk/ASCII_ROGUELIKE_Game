####################
# 
# Galina Bovykina
# November 16 2022
#
# This has the base ai behavior
# Code adopted from TStand90 rogueliketutorials.com
#
####################

from __future__ import annotations
import random
from typing import List, Optional, Tuple, TYPE_CHECKING
import numpy as np
import tcod
from actions import Action, BumpAction, MeleeAction, MovementAction, WaitAction


if TYPE_CHECKING:
    from entity import Actor

# This creates a super class and calculates paths
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


# This creates a condition that any entity can fall under
class ConfusedEnemy(BaseAI):
    def __init__(
        self, entity: Actor, previous_ai: Optional[BaseAI], turns_remaining: int
    ):
        super().__init__(entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def perform(self) -> None:
        if self.turns_remaining <= 0:
            self.engine.message_log.add_message(
                f"The {self.entity.name} snaps out of it's confusion."
            )
            self.entity.ai = self.previous_ai
        else:
            direction_x, direction_y = random.choice(
                [
                    (-1, -1),
                    (0, -1),
                    (1, -1),
                    (-1, 0),
                    (1, 0),
                    (-1, 1),
                    (0, 1),
                    (1, 1),
                ]
            )
            self.turns_remaining -= 1

            return BumpAction(self.entity, direction_x, direction_y,).perform()
        


# This creates basic behavior for the ai
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


#####  This part was specifically modified by me  #####
# This is the behavior of the closed door - which is nothing
class ClosedDoor(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int,int]] = []

    def perform(self) -> None:
        return WaitAction(self.entity).perform()
